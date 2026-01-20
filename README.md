# 🎤 Interview AI

An AI-powered interview trainer using **Whisper** for audio transcription and **Groq** for evaluation.

---

## Features

- Record answers to 5 common interview questions
- Get detailed evaluation with per-question ratings and improvement suggestions
- Metrics: duration and word count per answer
- Fully compatible with local setup and Hugging Face Spaces

---

## Interview Questions Included

1. Tell me about yourself.
2. Describe a challenging situation you faced. How did you handle it?
3. Why do you want to work for this company?
4. What are your key strengths and weaknesses?
5. Where do you see yourself in 5 years?

---

## Local Setup


1. Clone the repo:
```bash
git clone https://github.com/yourusername/interview-ai.git
cd interview-ai

2. Create a virtual environment:
python -m venv venv
# Activate:
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Add your Groq API key:
# Copy the sample.env file to .env
cp sample.env .env
Then open .env and replace the placeholder with your real API key:
GROQ_API_KEY=your_real_api_key_here

5. Run the app:
python app.py
