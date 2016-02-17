# UTemPr

**Please, read [_wiki_](https://github.com/Nik0l/UTemPr/wiki) for more information**

A framework for prediction of temporal user behavior.

The framework is written mostly in Python 2.7.

Dependencies:
scikit-learn, nolearn, NLTK, matplotlib, sqlite3, GeoPy, pyenchant

The goal of the framework is to predict temporal user behavior on the Web. For example, in the context of Q&A forums, to predict when a user answers a question, when a new question will be asked and by whom. The framework provides an API and has been tested on Stack Exchange websites.

The framework allows a user to choose a Q&A community/forum (currently 'only' 148 Stack Exchange websites) and then explore it, analyze, choose a prediction type, choose features for prediction, machine learning (ML) algorithm. Then a user can explore the results of the prediction, its accuracy and time performance.
```
Features:
1. User-related features
2. Question-related features
   a. Textual and text-based features (aka NLP features)
   b. tag-based features
3. Temporal features
   a. Associated with a user
   b. Associated with a question or answer
4. Spatial features
   a. User's location, timezone
```
To be continued...
