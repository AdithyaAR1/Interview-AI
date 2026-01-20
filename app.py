# Author: Adithya A R
# Interview Trainer AI (Groq-powered, Whisper-based)

import gradio as gr
import time
from faster_whisper import WhisperModel
import os
from groq import Groq

# -----------------------------
# Load Groq API key from HF Secrets
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# Load Whisper Model
# -----------------------------
print("Loading Whisper model...")
whisper = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# -----------------------------
# Helper Functions
# -----------------------------
def transcribe(audio_path):
    if not audio_path:
        return ""
    segments, _ = whisper.transcribe(audio_path)
    return " ".join(segment.text for segment in segments).strip()

def call_groq(prompt, max_tokens=700, temperature=0.4):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a professional interviewer evaluator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

# -----------------------------
# Questions
# -----------------------------
QUESTIONS = [
    "Tell me about yourself.",
    "Describe a challenging situation you faced. How did you handle it?",
    "Why do you want to work for this company?",
    "What are your key strengths and weaknesses?",
    "Where do you see yourself in 5 years?"
]

# -----------------------------
# Main Evaluation Function
# -----------------------------
def evaluate_all(*audio_files):
    status = "⏳ Processing answers. Please wait..."

    answers_text = []
    metrics = []

    for audio in audio_files:
        if not audio:
            answers_text.append("")
            metrics.append({"duration": 0, "words": 0})
            continue

        start = time.time()
        text = transcribe(audio)
        duration = time.time() - start

        answers_text.append(text)
        metrics.append({
            "duration": duration,
            "words": len(text.split())
        })

    prompt = (
        "You are a professional hiring manager.\n\n"
        "For each answer:\n"
        "- Give a rating (1–10) for delivery\n"
        "- Give one improvement suggestion\n\n"
        "Then provide:\n"
        "- Overall summary of the candidate\n"
        "- Final hireability decision: Hired / Borderline / Rejected\n\n"
        "Format clearly.\n\nCandidate Answers:\n"
    )

    for i, ans in enumerate(answers_text):
        prompt += f"Q{i+1}: {ans}\n"

    ai_response = call_groq(prompt)

    metrics_table = "| Question | Duration (sec) | Word Count |\n"
    metrics_table += "|---------|---------------|------------|\n"
    for i, m in enumerate(metrics, 1):
        metrics_table += f"| Q{i} | {m['duration']:.2f} | {m['words']} |\n"

    output = (
        "### 📊 Interview Evaluation\n"
        f"{ai_response}\n\n"
        "### 📈 Answer Metrics\n"
        f"{metrics_table}"
    )

    status = "✅ Evaluation complete"

    return output, status

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Interview Trainer AI")

    audio_inputs = []
    for i, q in enumerate(QUESTIONS):
        gr.Markdown(f"**Q{i+1}: {q}**")
        audio_inputs.append(
            gr.Audio(type="filepath", label=f"Answer Q{i+1}")
        )

    submit_btn = gr.Button("Submit All Answers")

    output_box = gr.Markdown()
    status_box = gr.Textbox(
        label="Status",
        value="Waiting...",
        lines=3,
        interactive=False
    )

    submit_btn.click(
        evaluate_all,
        inputs=audio_inputs,
        outputs=[output_box, status_box]
    )

# -----------------------------
# HF-ready launch
# -----------------------------
if __name__ == "__main__":
    demo.queue()
    demo.launch()
