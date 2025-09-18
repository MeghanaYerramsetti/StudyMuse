"""
Streamlit Personal Assistant — Fun & Relatable
Single-file Streamlit app implementing:
- Summarize
- Improve Text
- Fun Transform (Shakespeare, Rap, Meme, Sarcastic, Roast, Pirate, Yoda, Cowboy, Poem)
- Motivation / Quote Generator
- Notes Organizer (bullets & mindmap-ish output)
- Q&A Chat (Tutor) with file upload for notes

Requirements (put in requirements.txt):
streamlit
openai
tiktoken (optional for token counting)
python-dotenv
PyPDF2

Usage:
1. pip install -r requirements.txt
2. export OPENAI_API_KEY="sk-..." or use .env
3. streamlit run streamlit_personal_assistant.py

This app uses OpenAI's API by default but is written to allow swapping to other LLM backends.

"""

import streamlit as st
import os
import time
from typing import Tuple, List

# Optional: use dotenv to load API key from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ---- Configuration ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change as needed
API_BACKEND = os.getenv("API_BACKEND", "openai")  # or 'hf' etc.

# Minimal wrapper to call OpenAI (can be swapped with other providers)
def call_openai(prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 400) -> str:
    """Call OpenAI's chat completions. Expects OPENAI_API_KEY env var to be set."""
    try:
        import openai
    except Exception:
        return "Error: openai package not installed. Install with `pip install openai`."

    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY not set."

    openai.api_key = OPENAI_API_KEY
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        # Updated for openai python >=1.0.0
        resp = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"

# ---- Small helpers & prompt templates ----
PROMPTS = {
    "summarize": "Summarize the following text into a short, clear summary (3-6 lines). Keep it simple and friendly: \n\n{input}",
    "improve": "Improve the following text so it sounds polished, professional, and concise. Keep original meaning:\n\n{input}",
    "explain_simple": "Explain the following concept like I'm {age} years old. Use simple language, examples, and a short summary at the end:\n\n{input}",
    "shakespeare": "Turn this into Shakespearean-style language, with poetic phrasing and a touch of humor:\n\n{input}",
    "rap": "Turn this into a short rap verse (4-8 lines), keeping the original message and making it catchy and rhythmic:\n\n{input}",
    "meme": "Turn the input into a short meme-style caption or text suitable for social media (one-liners or 2-sentence punchlines):\n\n{input}",
    "sarcastic": "Turn this into a sarcastic version, with witty and ironic remarks:\n\n{input}",
    "roast": "Turn this into a light-hearted roast, poking fun in a playful way:\n\n{input}",
    "pirate": "Turn this into pirate speak, with 'arr' and nautical terms:\n\n{input}",
    "yoda": "Turn this into Yoda speak, like 'Do or do not, there is no try':\n\n{input}",
    "cowboy": "Turn this into cowboy speak, with 'howdy' and western slang:\n\n{input}",
    "poem": "Turn this into a short poem (4-8 lines), keeping the original message:\n\n{input}",
    "timeline": "Convert the following notes into a chronological timeline of events or key points:\n\n{input}",
    "flashcards": "Create flashcards from the following notes (question: answer format):\n\n{input}",
    "motivation": "Write a short, relatable motivational quote for a student about: {topic}. Keep it friendly and shareable (one or two lines).",
    "creativity_story": "Write a short (200-300 word) story about: {topic}. Keep it engaging and end with a twist.",
    "creativity_joke": "Write a short, wholesome joke about: {topic}.",
    "notes_bullets": "Convert the following lecture notes into concise bullet points capturing the key ideas, terms, and actions to remember:\n\n{input}",
    "mindmap_like": "Given the following notes, return a short hierarchical list that could be turned into a mind map (root -> 3 main branches -> 2 subpoints each):\n\n{input}",
    "qa_tutor": "You are a helpful tutor. Answer the question in a clear and friendly way, include one quick example and a 2-line summary at the end. If the user asks for step-by-step, provide numbered steps. Question:\n\n{input}",
}

# ---- Streamlit UI ----
st.set_page_config(page_title="Fun Personal Assistant", layout="wide")

# Header
col1, col2 = st.columns([8,1])
with col1:
    st.title("🎒 Fun & Relatable Personal Assistant")
    st.markdown("A friendly study buddy and creative text lab — Summarize, simplify, joke, and shine ✨")
with col2:
    st.write("")
    if OPENAI_API_KEY:
        st.success("🔒 API: OpenAI key detected")
    else:
        st.warning("No OPENAI_API_KEY found — demo mode only (local presets)")

# Sidebar: mode selector
st.sidebar.title("Modes")
mode = st.sidebar.radio("Choose a mode:", [
    "Summarize",
    "Improve Text",
    "Fun Transform",
    "Motivation",
    "Notes Organizer",
    "Q&A Chat (Tutor)"
])

# Shared inputs
st.sidebar.markdown("---")
user_tone = st.sidebar.selectbox("Response tone:", ["Friendly", "Formal", "Casual", "Funny"], index=0)
max_tokens = st.sidebar.slider("Max tokens / length", 100, 1200, 400, step=50)
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.2, 0.7, step=0.1)

# Mode-specific sidebar UI
age = None
subject = None
transform = None
topic = None
kind = None
style = None

if mode == "Fun Transform":
    transform = st.sidebar.selectbox("Choose transform:", ["Shakespeare", "Rap", "Meme", "Sarcastic", "Roast", "Pirate", "Yoda", "Cowboy", "Poem"])
elif mode == "Motivation":
    topic = st.sidebar.selectbox("Motivation topic:", ["studying", "procrastination", "stress", "success", "friendship"])
elif mode == "Notes Organizer":
    style = st.sidebar.selectbox("Notes output:", ["Bullets", "Mindmap-style", "Timeline", "Flashcards"])

# Example help
if st.sidebar.button("Show example prompts"):
    st.sidebar.info("Examples:\n- Summarize: Paste lecture notes and click Summarize.\n- Homework Helper: 'Explain mitosis like I'm 12'\n- Fun Transform: Paste your caption and choose Rap or Shakespeare.")

# Mode-specific main UI
if mode in ["Summarize", "Improve Text", "Fun Transform", "Motivation", "Notes Organizer", "Q&A Chat (Tutor)"]:
    input_text = st.text_area("Paste text / question here", height=250)
    if mode == "Q&A Chat (Tutor)":
        notes_file = st.file_uploader("Upload notes file (PDF or TXT)", type=["pdf", "txt"])
    run_button = st.button("✨ Run")
else:
    input_text = ""
    run_button = False

output_placeholder = st.empty()

# Safety: minimal profanity filter (client-side simple)
def simple_filter(text: str) -> bool:
    banned = ["bomb", "kill", "suicide"]
    lower = text.lower()
    return not any(b in lower for b in banned)

# Format prompt with tone
def apply_tone(prompt: str, tone: str) -> str:
    if tone == "Friendly":
        return prompt + "\nKeep the tone friendly and encouraging."
    if tone == "Formal":
        return prompt + "\nUse a formal and professional tone."
    if tone == "Casual":
        return prompt + "\nUse a casual, chatty tone with short sentences."
    if tone == "Funny":
        return prompt + "\nAdd light humor where appropriate."
    return prompt

# Run logic
if run_button:
    if not input_text.strip():
        st.warning("Please paste some text or a question first.")
    elif not simple_filter(input_text):
        st.error("Your input triggers the simple safety filter. Please modify and try again.")
    else:
        with st.spinner("Thinking..."):
            if mode == "Summarize":
                prompt = PROMPTS["summarize"].format(input=input_text)
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=temperature, max_tokens=max_tokens)
                output_placeholder.markdown("**Summary:**\n" + resp)

            elif mode == "Improve Text":
                prompt = PROMPTS["improve"].format(input=input_text)
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=temperature, max_tokens=max_tokens)
                st.subheader("Improved text")
                output_placeholder.code(resp)

            elif mode == "Fun Transform":
                key = transform.lower()
                prompt = PROMPTS[key].format(input=input_text)
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=temperature, max_tokens=max_tokens)
                output_placeholder.markdown(f"**{transform} version:**\n{resp}")

            elif mode == "Motivation":
                prompt = PROMPTS["motivation"].format(topic=topic)
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=temperature, max_tokens=80)
                output_placeholder.markdown(f"📝 **Quote:** {resp}")

            elif mode == "Notes Organizer":
                if style == "Bullets":
                    prompt = PROMPTS["notes_bullets"].format(input=input_text)
                elif style == "Mindmap-style":
                    prompt = PROMPTS["mindmap_like"].format(input=input_text)
                elif style == "Timeline":
                    prompt = PROMPTS["timeline"].format(input=input_text)
                elif style == "Flashcards":
                    prompt = PROMPTS["flashcards"].format(input=input_text)
                else:
                    prompt = PROMPTS["notes_bullets"].format(input=input_text)
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=0.3, max_tokens=max_tokens)
                output_placeholder.markdown(resp)

            elif mode == "Q&A Chat (Tutor)":
                # If notes file uploaded, extract text and prepend to prompt
                context_text = ""
                if notes_file is not None:
                    try:
                        import PyPDF2
                    except ImportError:
                        st.error("PyPDF2 module not installed. Please install it to enable PDF file uploads.")
                        context_text = ""
                    else:
                        try:
                            if notes_file.type == "application/pdf":
                                pdf_reader = PyPDF2.PdfReader(notes_file)
                                for page in pdf_reader.pages:
                                    context_text += page.extract_text() + "\n"
                            else:
                                # For txt files
                                context_text = notes_file.getvalue().decode("utf-8")
                        except Exception as e:
                            st.error(f"Error reading notes file: {e}")
                prompt = PROMPTS["qa_tutor"].format(input=input_text)
                if context_text:
                    prompt = f"Use the following notes to answer the question simply and understandably:\n{context_text}\nQuestion:\n{input_text}"
                prompt = apply_tone(prompt, user_tone)
                resp = call_openai(prompt, temperature=temperature, max_tokens=max_tokens)
                output_placeholder.markdown(resp)

            else:
                output_placeholder.text("Mode not implemented yet.")

# Footer: tips and export
st.sidebar.markdown("---")
if st.sidebar.button("Download last output as .txt"):
    try:
        last = output_placeholder
        # Attempt to read last content - Streamlit placeholder objects aren't readable; instruct user how to copy
        st.sidebar.info("Copy the output from the main panel and save it locally. Or use the app code to add a download button.")
    except Exception:
        st.sidebar.error("Could not prepare download in demo mode.")

st.markdown("---")
st.caption("Built for students — keep it friendly. You can hook any LLM backend into the `call_openai` function.")

# End of file
