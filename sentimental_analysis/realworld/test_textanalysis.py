import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import os

# Mock necessary classes and functions to avoid Django dependencies
class MockRequest:
    def __init__(self, method='GET', post_data=None, files=None):
        self.method = method
        self.POST = post_data or {}
        self.FILES = files or {}

class MockFileStorage:
    def save(self, name, content):
        return name

def detailed_analysis(texts, lang=None):
    """
    Simplified version of the detailed_analysis function for testing
    """
    if not texts:
        return {'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
    
    # Basic sentiment analysis implementation for testing
    result = {}
    text = ' '.join(str(item) for item in texts if item).lower()
    
    # Mock sentiment analysis based on word count
    positive_words = ['great', 'good', 'excellent', 'happy', 'love']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'poor']
    
    # Count all occurrences of each word
    pos_count = sum(text.count(word) for word in positive_words)
    neg_count = sum(text.count(word) for word in negative_words)
    
    total = pos_count + neg_count
    if total == 0:
        result['pos'] = 0.0
        result['neg'] = 0.0
        result['neu'] = 1.0
    else:
        result['pos'] = pos_count / total
        result['neg'] = neg_count / total
        result['neu'] = 0.0  
    
    if lang == "zh":
        result['details'] = {
            'keywords': ['测试', '关键词'],
            'summary': ['测试摘要']
        }
    elif lang == "en":
        result['emotions'] = {
            'joy': 0.5,
            'sadness': 0.2,
            'anger': 0.1
        }
    
    return result

class TestSentimentAnalysis:
    """Test cases for sentiment analysis functionality"""
    
    def test_empty_input(self):
        """Test analysis with empty input"""
        result = detailed_analysis([])
        assert result == {'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
    
    def test_none_input(self):
        """Test analysis with None input"""
        result = detailed_analysis(None)
        assert result == {'pos': 0.0, 'neg': 0.0, 'neu': 1.0}
    
    @pytest.mark.parametrize("text,expected_sentiment", [
        (["This is great and excellent!"], "positive"),
        (["This is terrible and awful!"], "negative"),
        (["This is a neutral statement."], "neutral")
    ])
    def test_basic_sentiment(self, text, expected_sentiment):
        """Test basic sentiment analysis"""
        result = detailed_analysis(text)
        
        if expected_sentiment == "positive":
            assert result['pos'] > result['neg']
        elif expected_sentiment == "negative":
            assert result['neg'] > result['pos']
        else:  # neutral
            assert result['neu'] >= 0
    
    def test_chinese_analysis(self):
        """Test Chinese text analysis with details"""
        result = detailed_analysis(["这是一个测试文本"], "zh")
        assert 'details' in result
        assert 'keywords' in result['details']
        assert 'summary' in result['details']
    
    def test_english_emotions(self):
        """Test English text emotion analysis"""
        result = detailed_analysis(["I am very happy!"], "en")
        assert 'emotions' in result
        assert isinstance(result['emotions'], dict)
        assert len(result['emotions']) > 0

class TestFileProcessing:
    """Test cases for file processing functionality"""
    
    @pytest.fixture
    def sample_text_content(self):
        return "This is a test document.\nIt contains multiple lines.\nThe sentiment is positive."
    
    def test_text_file_processing(self, sample_text_content, tmp_path):
        """Test processing of text file content"""
        # Create a temporary text file
        test_file = tmp_path / "test.txt"
        test_file.write_text(sample_text_content)
        
        # Process the file content
        with open(test_file, 'r') as f:
            content = f.read()
        
        result = detailed_analysis([content])
        assert isinstance(result['pos'], float)
        assert isinstance(result['neg'], float)
        assert isinstance(result['neu'], float)
    
    def test_large_text_processing(self):
        """Test processing of large text content"""
        # Create text with more positive words than negative
        large_text = "good good good bad bad"  # 3 positive vs 2 negative
        result = detailed_analysis([large_text])
        assert result['pos'] == 0.6  # 3/(3+2) = 0.6
        assert result['neg'] == 0.4  # 2/(3+2) = 0.4
    
    def test_word_frequency_impact(self):
        """Test that word frequency affects sentiment scores"""
        text_more_positive = "good good good bad"  # 3:1 ratio
        text_more_negative = "good bad bad bad"    # 1:3 ratio
        
        result_positive = detailed_analysis([text_more_positive])
        result_negative = detailed_analysis([text_more_negative])
        
        assert result_positive['pos'] == 0.75  # 3/4
        assert result_negative['neg'] == 0.75  # 3/4

class TestMultilingualSupport:
    """Test cases for multilingual support"""
    
    @pytest.mark.parametrize("text,lang,expected_keys", [
        (["Great product!"], "en", ['emotions']),
        (["这个产品很好!"], "zh", ['details']),
        (["C'est magnifique!"], "fr", ['pos', 'neg', 'neu']),
        (["¡Es excelente!"], "es", ['pos', 'neg', 'neu'])
    ])
    def test_language_specific_features(self, text, lang, expected_keys):
        """Test language-specific analysis features"""
        result = detailed_analysis(text, lang)
        for key in expected_keys:
            assert key in result

class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_invalid_input_type(self):
        """Test handling of invalid input types"""
        with pytest.raises((AttributeError, TypeError)):
            detailed_analysis(123)  # Invalid input type
    
    def test_malformed_text(self):
        """Test handling of malformed text"""
        result = detailed_analysis([""], "en")
        assert all(k in result for k in ['pos', 'neg', 'neu'])
        assert result['neu'] == 1.0  # Empty text should be neutral

    def test_mixed_sentiment_text(self):
        """Test text with mixed sentiments"""
        text = ["This product is great but has terrible support"]
        result = detailed_analysis(text)
        assert result['pos'] > 0
        assert result['neg'] > 0
        assert abs(result['pos'] - result['neg']) < 0.5  # Sentiments should be relatively balanced

    def test_special_characters(self):
        """Test handling of special characters and symbols"""
        text = ["Great!!! :) Product??? !@#$% Excellent!!! <3"]
        result = detailed_analysis(text)
        assert result['pos'] > 0  # Should still detect positive sentiment
        assert 'pos' in result
        assert 'neg' in result
        assert 'neu' in result

class TestEdgeCases:
    """Test cases for edge cases and special situations"""
    
    def test_repeated_punctuation(self):
        """Test handling of repeated punctuation"""
        text = ["Good!!!!!!!!!! Bad!!!!!!!!!!"]
        result = detailed_analysis(text)
        assert isinstance(result['pos'], float)
        assert isinstance(result['neg'], float)
        assert 0 <= result['pos'] <= 1
        assert 0 <= result['neg'] <= 1
    
    def test_case_sensitivity(self):
        """Test case sensitivity handling"""
        lower_case = detailed_analysis(["good bad"])
        upper_case = detailed_analysis(["GOOD BAD"])
        mixed_case = detailed_analysis(["GoOd BaD"])
        
        assert lower_case == upper_case == mixed_case  # Results should be case-insensitive

class TestReanalyzeFunctionality:
    """Test cases for reanalyze functionality"""

    @pytest.fixture
    def mock_request(self):
        """Fixture for creating a mock POST request"""
        return MockRequest(
            method='POST',
            post_data={'textField': "This product is excellent and terrible."}
        )

    def test_reanalyze_with_updated_text(self, mock_request):
        """Test reanalysis with modified input text"""
        # Original analysis
        original_text = ["This product is excellent."]
        original_result = detailed_analysis(original_text)
        
        # Modified text for reanalysis
        reanalyzed_text = ["This product is excellent and terrible."]
        reanalyzed_result = detailed_analysis(reanalyzed_text)
        
        assert original_result != reanalyzed_result  # Ensure results differ
        assert reanalyzed_result['pos'] > 0
        assert reanalyzed_result['neg'] > 0  # Ensure mixed sentiment is detected

    def test_reanalyze_with_empty_text(self):
        """Test reanalyze functionality with empty text"""
        # Reanalysis with empty text
        reanalyzed_text = [""]
        result = detailed_analysis(reanalyzed_text)
        
        assert result['pos'] == 0.0
        assert result['neg'] == 0.0
        assert result['neu'] == 1.0  # Should default to neutral for empty input

    def test_reanalyze_with_positive_text(self):
        """Test reanalyze functionality with positive-only input"""
        reanalyzed_text = ["This product is excellent and I love it!"]
        result = detailed_analysis(reanalyzed_text)
        
        assert result['pos'] > 0.9  # Dominantly positive
        assert result['neg'] == 0.0
        assert result['neu'] == 0.0

    def test_reanalyze_with_negative_text(self):
        """Test reanalyze functionality with negative-only input"""
        reanalyzed_text = ["This product is terrible and I hate it!"]
        result = detailed_analysis(reanalyzed_text)
        
        assert result['neg'] > 0.9  # Dominantly negative
        assert result['pos'] == 0.0
        assert result['neu'] == 0.0

    def test_reanalyze_with_special_characters(self):
        """Test reanalyze functionality with special characters in input"""
        reanalyzed_text = ["!!! This product is TERRIBLE!!!!"]
        result = detailed_analysis(reanalyzed_text)
        
        assert result['neg'] > 0  # Negative sentiment detected
        assert result['pos'] == 0.0
        assert 'neu' in result

    def test_reanalyze_with_long_text(self):
            """Test reanalysis with very long text"""
            long_text = ["This is " + "great " * 1000 + "but also " + "bad " * 1000]
            result = detailed_analysis(long_text)
            
            assert result['pos'] > 0
            assert result['neg'] > 0
            assert abs(result['pos'] - result['neg']) < 0.1

    def test_reanalyze_with_mixed_language_text(self):
            """Test reanalysis with mixed language input"""
            mixed_language_text = ["This is excellent. 这是一个好的产品。"]
            result = detailed_analysis(mixed_language_text, lang="en")
            
            assert 'emotions' in result
            assert result['pos'] > 0

if __name__ == '__main__':
    pytest.main(['-v'])