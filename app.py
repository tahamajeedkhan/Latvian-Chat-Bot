import streamlit as st
import requests
import PyPDF2
from gtts import gTTS
from langdetect import detect
import io
from datetime import datetime
import os


# =======================
# 🔐 CONFIG
# =======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =======================
# 🎨 MINIMAL PROFESSIONAL CSS
# =======================
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Top Navigation Bar */
    .top-nav {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 16px 24px;
        margin: -80px -80px 0 -80px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-brand {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-status {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        color: #6b7280;
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
    }
    
    /* Main Container */
    .main-container {
        max-width: 900px;
        margin: 40px auto;
        padding: 0 24px;
    }
    
    /* Chat Area */
    .chat-area {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        margin-bottom: 16px;
    }
    
    .chat-area::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-area::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 3px;
    }
    
    /* Message Bubbles */
    .message-row {
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
    }
    
    .message-row.user {
        align-items: flex-end;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .message-bubble.user {
        background: #3b82f6;
        color: #ffffff;
    }
    
    .message-bubble.assistant {
        background: #f3f4f6;
        color: #111827;
    }
    
    .message-meta {
        font-size: 12px;
        color: #9ca3af;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 80px 20px;
        color: #9ca3af;
    }
    
    .empty-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.5;
    }
    
    .empty-text {
        font-size: 14px;
        color: #6b7280;
    }
    
    /* Input Area */
    .input-area {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px;
    }
    
    .stTextInput input {
        border: 1px solid #e5e7eb !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        background: #ffffff !important;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stButton button {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: background 0.2s !important;
    }
    
    .stButton button:hover {
        background: #2563eb !important;
    }
    
    /* Upload Area */
    .upload-container {
        max-width: 600px;
        margin: 60px auto;
        text-align: center;
    }
    
    .upload-box {
        background: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        padding: 60px 40px;
        transition: border-color 0.2s;
    }
    
    .upload-box:hover {
        border-color: #3b82f6;
    }
    
    .upload-icon {
        font-size: 48px;
        margin-bottom: 16px;
        color: #6b7280;
    }
    
    .upload-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .upload-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    
    /* Feature Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        margin-top: 48px;
    }
    
    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }
    
    .feature-title {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        font-size: 13px;
        color: #6b7280;
        line-height: 1.5;
    }
    
    /* Audio Player */
    audio {
        width: 100%;
        margin-top: 8px;
        height: 32px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        font-size: 14px;
    }
    
    /* Metrics */
    .stMetric {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 12px;
    }
    
    /* File Uploader */
    section[data-testid="stFileUploadDropzone"] {
        background: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 8px;
    }
    
    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #3b82f6;
    }
    
    /* Alert Messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 6px;
        font-size: 14px;
    }
    
    @media (max-width: 768px) {
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .message-bubble {
            max-width: 85%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# =======================
# 📄 FUNCTIONS
# =======================
def extract_pdf_text(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def ask_groq(document_text, question, lang):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    response_lang = "latviešu" if lang == "lv" else "English"
    
    prompt = f"""
You are a helpful assistant. 
Document is in Latvian. Answer the user's question based on the document content in {response_lang}.

Document:
{document_text[:8000]}

User question:
{question}

Answer in {response_lang}:
"""
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant that answers in {response_lang}."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def create_audio(text, lang):
    gtts_lang = "lv" if lang == "lv" else "en"
    tts = gTTS(text=text, lang=gtts_lang)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# =======================
# 🎯 MAIN APP
# =======================
def main():
    st.set_page_config(
        page_title="PDF Assistant",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_custom_css()
    
    # Initialize session state
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_uploaded' not in st.session_state:
        st.session_state.pdf_uploaded = False
    
    # Top Navigation
    st.markdown("""
    <div class="top-nav">
        <div class="nav-brand">
            <span>📄</span>
            <span>PDF Assistant</span>
        </div>
        <div class="nav-status">
            <div class="status-indicator"></div>
            <span>Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Section
    if not st.session_state.pdf_uploaded:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        st.markdown("""
        <div class="upload-box">
            <div class="upload-icon">📄</div>
            <div class="upload-title">Upload PDF Document</div>
            <div class="upload-subtitle">Support for Latvian and English documents</div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose PDF",
            type=['pdf'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            with st.spinner("Processing document..."):
                try:
                    st.session_state.document_text = extract_pdf_text(uploaded_file)
                    st.session_state.pdf_uploaded = True
                    st.success(f"Successfully loaded: {uploaded_file.name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Features
        st.markdown("""
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Search</div>
                <div class="feature-desc">Extract precise information from your documents</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">Bilingual</div>
                <div class="feature-desc">Works with English and Latvian languages</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎧</div>
                <div class="feature-title">Audio Output</div>
                <div class="feature-desc">Listen to responses with text-to-speech</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Chat Interface
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        #st.markdown('<div class="chat-area">', unsafe_allow_html=True)
        
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">💬</div>
                <div class="empty-text">Ask a question about your document</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display messages
        for chat in st.session_state.chat_history:
            time_str = datetime.now().strftime("%H:%M")
            
            # User message
            st.markdown(f"""
            <div class="message-row user">
                <div class="message-bubble user">{chat['question']}</div>
                <div class="message-meta">{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Assistant message
            st.markdown(f"""
            <div class="message-row">
                <div class="message-bubble assistant">{chat['answer']}</div>
                <div class="message-meta">Assistant • {time_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Audio
            audio_file = create_audio(chat['answer'], chat['lang'])
            st.audio(audio_file, format='audio/mp3')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input Area
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        with st.form(key="msg_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                question = st.text_input(
                    "Message",
                    placeholder="Type your question...",
                    label_visibility="collapsed"
                )
            with cols[1]:
                submit = st.form_submit_button("Send", use_container_width=True)
        
        if submit and question:
            lang = detect(question)
            with st.spinner("Processing..."):
                try:
                    answer = ask_groq(st.session_state.document_text, question, lang)
                    st.session_state.chat_history.append({
                        'question': question,
                        'answer': answer,
                        'lang': lang
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.markdown("### Document Info")
            if st.session_state.document_text:
                st.metric("Characters", f"{len(st.session_state.document_text):,}")
                st.metric("Words", f"{len(st.session_state.document_text.split()):,}")
            
            st.markdown("---")
            
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            
            if st.button("New Document", use_container_width=True):
                st.session_state.pdf_uploaded = False
                st.session_state.document_text = None
                st.session_state.chat_history = []
                st.rerun()

if __name__ == "__main__":
    main()