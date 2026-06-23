# SMS Spam Classifier

A machine learning web app that detects spam SMS messages using a Support Vector Machine trained on the UCI SMS Spam Collection dataset.

## Demo
<img width="1920" height="1080" alt="Screenshot (126)" src="https://github.com/user-attachments/assets/2c858dd0-5ff5-4c7d-a642-e6dc9dc6d5ef" />
<img width="1920" height="1080" alt="Screenshot (125)" src="https://github.com/user-attachments/assets/b88a4106-33de-460e-85d1-4ed2cd3a3770" />



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
