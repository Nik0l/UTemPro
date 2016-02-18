# UTemPr

**Please, read [_wiki_](https://github.com/Nik0l/UTemPr/wiki) for more information**

A framework for prediction of human behavior on the Web. 

The framework is written mostly in Python 2.7.

Dependencies:
scikit-learn, nolearn, NLTK, matplotlib, sqlite3, GeoPy, pyenchant


We give an example of predicting human behavior in the context of Q&A forums. We predict when a user answers a question.

[In progress] The framework provides an API and has been tested on Stack Exchange websites. The framework allows a user to choose a Q&A community/forum (currently 'only' 148 Stack Exchange websites) and then explore it, analyze, choose a prediction task, choose features for prediction, machine learning (ML) algorithm. Then a user can explore the results of the prediction, its accuracy and time performance.

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
