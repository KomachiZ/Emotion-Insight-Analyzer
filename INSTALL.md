
# 🚀 Emotion Insight Analyzer Installation and Setup

## Installation
1. **Clone the Repository**  
   Open a terminal and run:
   ```bash
   git clone https://github.com/Fall24-SE-ASK/Emotion-Insight-Analyzer.git
   ```
---

2. **Using Python 3.11**
   You can get it here: https://www.python.org/downloads/release/python-3115/
   
3. **Installation Details**
   ```
   pip uninstall -y numpy
   pip install numpy==1.26.0
   pip install -r requirements.txt (here you may change requests==2.24.0 to requests>=2.27,<3 in requirements.txt)
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
   pip install scikit-learn
   sudo apt-get update 
   sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
   pip install tf-keras
   pip install spanish_nlp
   pip install textblob
   pip install textblob-fr
   pip install snownlp
   pip install NRCLex
   ```

## Running Emotion Insight Analyzer

```
cd <your_repo_dir>
python ./sentimental_analysis/manage.py runserver
```
Next, open your browser and type in the host:port(eg. localhost:8000) in the search bar to open the user interface of the application.
---


You're all set! Enjoy Emotion Insight Analyzer.
