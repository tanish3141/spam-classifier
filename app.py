import streamlit as st
import re
import string
import joblib

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="🛡️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Page background */
.stApp {
    background: #0f1117;
}

/* Hide default Streamlit header decoration */
header[data-testid="stHeader"] { background: transparent; }

/* ── Hero card ── */
.hero {
    background: linear-gradient(135deg, #1a1d2e 0%, #12151f 100%);
    border: 1px solid #2a2d3e;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 99px;
    border: 1px solid rgba(99, 102, 241, 0.3);
    margin-bottom: 1rem;
}
.hero h1 {
    color: #f1f5f9;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.4rem;
    line-height: 1.2;
}
.hero p {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Stat pills ── */
.stats-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 1.4rem;
}
.stat-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid #2a2d3e;
    border-radius: 10px;
    padding: 10px 18px;
    text-align: center;
}
.stat-pill .num { color: #818cf8; font-size: 1.2rem; font-weight: 700; }
.stat-pill .lbl { color: #64748b; font-size: 0.7rem; letter-spacing: 0.06em; }

/* ── Input card ── */
.input-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 14px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
}
.input-card label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* Style the textarea */
textarea {
    background: #0f1117 !important;
    border: 1px solid #2a2d3e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.97rem !important;
    caret-color: #818cf8 !important;
}
textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}

/* ── Result boxes ── */
.result-spam {
    background: linear-gradient(135deg, rgba(239,68,68,0.12) 0%, rgba(185,28,28,0.08) 100%);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    animation: fadeIn 0.35s ease;
}
.result-ham {
    background: linear-gradient(135deg, rgba(34,197,94,0.12) 0%, rgba(21,128,61,0.08) 100%);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    animation: fadeIn 0.35s ease;
}
.result-icon { font-size: 2.4rem; line-height: 1; }
.result-title-spam { color: #f87171; font-size: 1.25rem; font-weight: 700; margin: 0 0 3px; }
.result-title-ham  { color: #4ade80; font-size: 1.25rem; font-weight: 700; margin: 0 0 3px; }
.result-sub { color: #94a3b8; font-size: 0.84rem; margin: 0; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Analyze button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white !important;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: opacity 0.2s;
    letter-spacing: 0.02em;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88;
}


/* ── Footer ── */
.footer {
    text-align: center;
    color: #334155;
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text


@st.cache_resource
def load_model():
    return joblib.load("spam_classifier_model.pkl")


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🛡️ &nbsp; ML · NLP · SVM</div>
  <h1>SMS Spam Detector</h1>
  <p>TF-IDF features · Support Vector Machine · UCI SMS dataset</p>
  <div class="stats-row">
    <div class="stat-pill"><div class="num">98.8%</div><div class="lbl">Recall</div></div>
    <div class="stat-pill"><div class="num">5,574</div><div class="lbl">Training msgs</div></div>
    <div class="stat-pill"><div class="num">SVM</div><div class="lbl">Classifier</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
sms_input = st.text_area(
    "Paste or type an SMS message",
    height=130,
    placeholder="e.g.  Congratulations! You've won a free iPhone. Click the link to claim…",
)

analyze_clicked = st.button("Analyze Message")

# ── Prediction ────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not sms_input.strip():
        st.warning("Please enter a message before analyzing.")
    else:
        try:
            model = load_model()
            cleaned = clean_text(sms_input)
            prediction = model.predict([cleaned])[0]

            if prediction == 1:
                st.markdown("""
                <div class="result-spam">
                  <div class="result-icon">🚨</div>
                  <div>
                    <p class="result-title-spam">Spam Detected</p>
                    <p class="result-sub">This message shows characteristics of unsolicited or malicious content.</p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-ham">
                  <div class="result-icon">✅</div>
                  <div>
                    <p class="result-title-ham">Looks Safe (Ham)</p>
                    <p class="result-sub">No spam signals detected — this appears to be a legitimate message.</p>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("Model file `spam_classifier_model.pkl` not found. Place it in the same directory as `app.py`.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with Scikit-learn · NLTK · Streamlit &nbsp;|&nbsp; UCI SMS Spam Collection dataset
</div>
""", unsafe_allow_html=True)