# SMS Spam Classifier

A machine learning web app that detects spam SMS messages using a Support Vector Machine trained on the UCI SMS Spam Collection dataset.

## Demo

![App Screenshot](screenshot.png)

## How it works

1. Raw SMS text is cleaned — lowercased, punctuation removed, links and numbers stripped
2. Text is transformed into numerical features using TF-IDF vectorization
3. A trained SVM model classifies the message as **Spam** or **Ham**

## Tech Stack

- **Model:** Support Vector Machine (Scikit-learn)
- **Features:** TF-IDF Vectorizer + NLTK text preprocessing
- **Dataset:** [UCI SMS Spam Collection](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) — 5,574 messages
- **UI:** Streamlit
- **Model serialization:** Joblib

## Performance

| Metric | Score |
|--------|-------|
| Recall | 98.8% |
| Classifier | Linear SVM |
| Training set | ~4,459 messages |
| Test set | ~1,115 messages |

## Project Structure

```
├── app.py                     # Streamlit app
├── train.ipynb                # Training notebook
├── spam_classifier_model.pkl  # Saved model pipeline
└── README.md
```

## Setup & Run

```bash
pip install streamlit scikit-learn nltk joblib
streamlit run app.py
```

Make sure `spam_classifier_model.pkl` is in the same directory as `app.py`.