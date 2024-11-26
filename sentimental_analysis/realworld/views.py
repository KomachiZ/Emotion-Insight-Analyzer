import os
import json
import csv
from io import StringIO
import subprocess
import shutil
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.http import HttpResponse
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import nltk
from pydub import AudioSegment
from .newsScraper import *
from .utilityFunctions import *
from nltk.corpus import stopwords
from .fb_scrap import *
from .twitter_scrap import *
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
from deepface import DeepFace
from langdetect import detect
from spanish_nlp import classifiers
from textblob import TextBlob
from snownlp import SnowNLP
from textblob_fr import PatternTagger, PatternAnalyzer
from nrclex import NRCLex
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from .music_recommendations import MusicRecommender
def pdfparser(data):
    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt", 'r', encoding="utf-8")
    a = ""
    for x in text_file:
        if len(x) > 2:
            b = x.split()
            for i in b:
                a += " "+i
    final_comment = a.split('.')
    return final_comment

def analysis(request):
    return render(request, 'realworld/index.html')

def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.add('rt')
    stop_words.add('')
    newtokens = [item for item in tokens if item not in stop_words]

    textclean = ' '.join(newtokens)
    return textclean

def detailed_analysis(texts, lang=None):
    """
    Multi-language sentiment analysis function
    Args:
        texts: List of text segments to analyze
        lang: Language code (if None, will auto-detect)
    Returns:
        Dictionary containing sentiment scores and optional details
    """
    if not texts:
        return {'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
    
    # Join text segments
    text = ' '.join(str(item) for item in texts if item)
    
    # Auto-detect language if not specified
    if not lang:
        try:
            lang = detect(text)
        except Exception as e:
            print(f"Language detection error: {e}")
            lang = "en"  # Default to English
    
    result = {}
    
    try:
        # English analysis
        if lang == "en":
            # Original English analysis logic
            neg_count = pos_count = neu_count = 0
            
            for item in texts:
                cleantext = get_clean_text(str(item))
                sentiment = sentiment_scores(cleantext)
                pos_count += sentiment['pos']
                neu_count += sentiment['neu']
                neg_count += sentiment['neg']
            
            total = pos_count + neu_count + neg_count
            if total > 0:
                result = {
                    'pos': (pos_count/total),
                    'neu': (neu_count/total),
                    'neg': (neg_count/total)
                }
                result['emotions'] = text_emotion_analysis(text)
                # # 找出主要情感
                # sentiment_type = max(('pos', result['pos']), ('neg', result['neg']), ('neu', result['neu']), key=lambda x: x[1])[0]
                # sentiment_score = result[sentiment_type]

                # print(f"Main sentiment: {sentiment_type}, score: {sentiment_score}")

                # # 将 'neu' 映射为 'neutral'
                # sentiment_mapping = {
                #     'pos': 'positive',
                #     'neg': 'negative',
                #     'neu': 'neutral'
                # }

                # mapped_sentiment = sentiment_mapping[sentiment_type]

                # # 获取音乐推荐
                # recommender = MusicRecommender()
                # recommended_songs = recommender.get_recommendations(mapped_sentiment, sentiment_score * 100)

                # # 添加到结果中
                # result['recommended_songs'] = recommended_songs
                # result['main_sentiment'] = {
                #     'type': mapped_sentiment,  # 使用映射后的类型
                #     'score': sentiment_score * 100
                # }
                # print(result)
                 # 找出主要情感
                sentiment_type = max(('pos', result['pos']), ('neg', result['neg']), ('neu', result['neu']), key=lambda x: x[1])[0]
                sentiment_score = result[sentiment_type]

                print(f"Main sentiment: {sentiment_type}, score: {sentiment_score}")

                # 将 'neu' 映射为 'neutral'
                sentiment_mapping = {
                    'pos': 'positive',
                    'neg': 'negative',
                    'neu': 'neutral'
                }

                mapped_sentiment = sentiment_mapping[sentiment_type]

                # 获取音乐推荐
                recommender = MusicRecommender()
                recommended_songs = recommender.get_recommendations(mapped_sentiment, sentiment_score * 100)
                
                # Debug输出
                print(f"Recommended songs structure: {recommended_songs}")

                # 添加到结果中
                result['recommended_songs'] = recommended_songs  # 现在这是一个字典列表，每个字典包含 name 和 spotify_id
                result['main_sentiment'] = {
                    'type': mapped_sentiment,
                    'score': sentiment_score * 100
                }
                
                print("Final result structure:", result)


                
        # Spanish analysis
        elif lang == "es":
            sc = classifiers.SpanishClassifier(model_name="sentiment_analysis")
            result_classifier = sc.predict(text)
            result = {
                'pos': result_classifier.get('positive', 0.0),
                'neu': result_classifier.get('neutral', 0.0),
                'neg': result_classifier.get('negative', 0.0)
            }
            
        # French analysis
        elif lang == "fr":
            blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
            polarity = blob.sentiment[0]
            
            if polarity > 0.1:
                result = {"pos": polarity, "neg": 0.0, "neu": 1 - polarity}
            elif polarity < -0.1:
                result = {"pos": 0.0, "neg": abs(polarity), "neu": 1 - abs(polarity)}
            else:
                result = {"pos": 0.0, "neg": 0.0, "neu": 1.0}
                
        # Chinese analysis
        elif lang in ["zh", "zh-cn", "zh-tw"]:
            s = SnowNLP(text)
            sentiment_score = s.sentiments
            
            if sentiment_score > 0.6:
                result = {
                    "pos": sentiment_score,
                    "neg": 0.0,
                    "neu": 1 - sentiment_score
                }
            elif sentiment_score < 0.4:
                result = {
                    "pos": 0.0,
                    "neg": 1 - sentiment_score,
                    "neu": sentiment_score
                }
            else:
                result = {
                    "pos": 0.0,
                    "neg": 0.0,
                    "neu": 1.0
                }
            
            try:
                result['details'] = {
                    'keywords': list(set([word for word in s.words if len(word) > 1]))[:10],
                    'summary': s.summary(3)
                }
            except Exception as e:
                print(f"Error in Chinese detailed analysis: {e}")
        
        # Unsupported language
        else:
            result = {'error': f'Language {lang} is not supported yet!'}
            
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        result = {'error': f'Analysis failed: {str(e)}'}
        
    return result

def textanalysis(request):
    """
    View function for text analysis
    """
    if request.method == 'POST':
        text_data = request.POST.get("textField", "")
        final_comment = text_data.split('.')
        result = detailed_analysis(final_comment)
        return render(request, 'realworld/results.html', {
            'sentiment': result, 
            'text': final_comment
        })
    else:
        return render(request, 'realworld/textanalysis.html', {
            'note': "Enter the Text to be analysed!"
        })

def input(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = 'sentimental_analysis/media/'
        extension_name = file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+file.name
        destination_folder = 'sentimental_analysis/media/document/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder+file.name
        result = {}
        finalText = ''
        if extension_name == 'pdf':
            value = pdfparser(useFile)
            result = detailed_analysis(value)
            finalText = result
        elif extension_name == 'txt':
            text_file = open(useFile, 'r', encoding="utf-8")
            a = ""
            for x in text_file:
                if len(x) > 2:
                    b = x.split()
                    for i in b:
                        a += " " + i
            final_comment = a.split('.')
            text_file.close()
            finalText = final_comment
            result = detailed_analysis(final_comment)
        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return render(request, 'realworld/results.html', {'sentiment': result, 'text': finalText})
    else:
        note = "Please Enter the Document you want to analyze"
        return render(request, 'realworld/home.html', {'note': note})

def inputimage(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = 'sentimental_analysis/media/'
        extension_name = file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+file.name
        destination_folder = 'sentimental_analysis/media/document/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder+file.name
        image = cv2.imread(useFile)
        detected_emotion = DeepFace.analyze(image,actions=['emotion'])
        
        emotions_dict = {'happy': 0.0, 'sad': 0.0, 'neutral': 0.0}
        for emotion in detected_emotion:
            emotion_scores = emotion['emotion']
            happy_score = emotion_scores['happy']
            sad_score = emotion_scores['sad']
            neutral_score = emotion_scores['neutral']

            emotions_dict['happy'] += happy_score
            emotions_dict['sad'] += sad_score
            emotions_dict['neutral'] += neutral_score

        total_score = sum(emotions_dict.values())
        if total_score > 0:
            for emotion in emotions_dict:
                emotions_dict[emotion] /= total_score

        print(emotions_dict)
        finalText = max(emotions_dict, key=emotions_dict.get)
        return render(request, 'realworld/resultsimage.html', {'sentiment': emotions_dict, 'text' : finalText, 'analyzed_image_path': useFile})

def productanalysis(request):
    if request.method == 'POST':
        blogname = request.POST.get("blogname", "")

        text_file = open(
            "Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/ProductAnalysis.txt", "w")
        text_file.write(blogname)
        text_file.close()

        spider_path = r'Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/amazon_review.py'
        output_file = r'Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/reviews.json'
        command = f"scrapy runspider \"{spider_path}\" -o \"{output_file}\" "
        result = subprocess.run(command, shell=True)

        if result.returncode == 0:
            print("Scrapy spider executed successfully.")
        else:
            print("Error executing Scrapy spider.")
       
        with open(r'Amazon_Comments_Scrapper/amazon_reviews_scraping/amazon_reviews_scraping/spiders/reviews.json', 'r') as json_file:
            json_data = json.load(json_file)
        reviews = []

        for item in json_data:
            reviews.append(item['Review'])
        finalText = reviews
        result = detailed_analysis(reviews)
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})
    else:
        note = "Please Enter the product blog link for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

def text_emotion_analysis(text):
    emotion_counts = {}
    text_emotion = NRCLex(text)
    for emotion, score in text_emotion.raw_emotion_scores.items():
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + score
    return emotion_counts

def determine_language(texts):
    langs = []
    try:
        for text in texts:
            langs.append(detect(text))
    except Exception as e:
        # Handle potential exceptions when using langdetect
        print(f"Error detecting language: {e}")
        return False
    unique_langs = list(set(langs))
    if len(unique_langs) != 1:
        return False
    return unique_langs[0]

    
def fbanalysis(request):
    if request.method == 'POST':       
        current_directory = os.path.dirname(__file__)
        result = fb_sentiment_score()
       
        csv_file_fb = 'fb_sentiment.csv'
        csv_file_path = os.path.join(current_directory, csv_file_fb)

        # Open the CSV file and read its content
        with open(csv_file_path, 'r') as csv_file:
            # Use DictReader to read CSV data into a list of dictionaries
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        text_dict = {"reviews" : data}
        print("text_dict:",text_dict["reviews"])
        # Convert the list of dictionaries to a JSON array
        json_data = json.dumps(text_dict, indent=2)

        reviews = []

        for item in text_dict["reviews"]:
            #print("item :",item)
            reviews.append(item["FBPost"])
        finalText = reviews

       
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})
    else:
        note = "Please Enter the product blog link for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

def twitteranalysis(request):
    if request.method == 'POST':       
        current_directory = os.path.dirname(__file__)
        result = twitter_sentiment_score()
       
        csv_file_fb = 'twitt.csv'
        csv_file_path = os.path.join(current_directory, csv_file_fb)

        # Open the CSV file and read its content
        with open(csv_file_path, 'r') as csv_file:
            # Use DictReader to read CSV data into a list of dictionaries
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        text_dict = {"reviews" : data}
        print("text_dict:",text_dict["reviews"])
        # Convert the list of dictionaries to a JSON array
        json_data = json.dumps(text_dict, indent=2)

        reviews = []

        for item in text_dict["reviews"]:
            #print("item :",item)
            reviews.append(item["review"])
        finalText = reviews

       
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})
    else:
        note = "Please Enter the product blog link for analysis"
        return render(request, 'realworld/productanalysis.html', {'note': note})

def audioanalysis(request):
    if request.method == 'POST':
        file = request.FILES['audioFile']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = "sentimental_analysis/media/"
        extension_name = file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+file.name
        result = {}
        destination_folder = 'sentimental_analysis/media/audio/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder+file.name
        text = speech_to_text(useFile)
        finalText = text
        result = detailed_analysis(text)

        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})
    else:
        note = "Please Enter the audio file you want to analyze"
        return render(request, 'realworld/audio.html', {'note': note})


def livespeechanalysis(request):
    if request.method == 'POST':
        my_file_handle = open(
            'sentimental_analysis/realworld/recordedAudio.txt')
        audioFile = my_file_handle.read()
        result = {}
        text = speech_to_text(audioFile)

        finalText = text
        result = detailed_analysis(text)
        folder_path = 'sentimental_analysis/media/recordedAudio/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})


@csrf_exempt
def recordaudio(request):
    if request.method == 'POST':
        audio_file = request.FILES['liveaudioFile']
        fs = FileSystemStorage()
        fs.save(audio_file.name, audio_file)
        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)

        pathname = "sentimental_analysis/media/"
        extension_name = audio_file.name
        extension_name = extension_name[len(extension_name)-3:]
        path = pathname+audio_file.name
        audioName = audio_file.name
        destination_folder = 'sentimental_analysis/media/recordedAudio/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder+audioName
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        audio = AudioSegment.from_file(useFile)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(44100)
        audio = audio.set_channels(1)
        audio.export(useFile, format='wav')

        text_file = open("sentimental_analysis/realworld/recordedAudio.txt", "w")
        text_file.write(useFile)
        text_file.close()
        response = HttpResponse('Success! This is a 200 response.', content_type='text/plain', status=200)
        return response

def newsanalysis(request):
    if request.method == 'POST':
        topicname = request.POST.get("topicname", "")
        scrapNews(topicname)

        with open(r'sentimental_analysis/realworld/news.json', 'r') as json_file:
            json_data = json.load(json_file)
        news = []
        for item in json_data:
            news.append(item['Summary'])
        finalText = news
        result = detailed_analysis(news)
        return render(request, 'realworld/results.html', {'sentiment': result, 'text' : finalText})
    else:
        return render(request, 'realworld/index.html')

def speech_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score


# @register.filter(name='get_item')
# def get_item(dictionary, key):
#     return dictionary.get(key, 0)
# 修改模板过滤器，以支持获取推荐列表
@register.filter(name='get_item')
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, [])
    return []