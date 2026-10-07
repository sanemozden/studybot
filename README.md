# 📚 StudyBot

A small AI-powered study helper built with Python, Streamlit and the Google Gemini API.

Enter any topic and StudyBot generates a short summary and **3 multiple-choice questions**. Answer them, check your results and see your score. The interface and the generated content are available in **Turkish, German and English**.

## Features
- Short summary for any topic
- 3 multiple-choice questions with explanations
- Instant answer check and score
- Language switch (Türkçe / Deutsch / English) for both the interface and the content

## Setup
1. Install Python 3.9 or newer.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey).
4. Create a file named `.env` in the project folder with this content:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Start the app:
   ```bash
   python -m streamlit run app.py
   ```

> The `.env` file is listed in `.gitignore`, so your key is never uploaded to GitHub.

## How it works
The topic is sent to the Gemini API together with a system prompt. The model returns the summary and questions as JSON, which Streamlit then displays as an interactive quiz.

## Ideas for next steps
- [ ] Difficulty levels
- [ ] Job-interview mode (questions for a given profession)
- [ ] Upload a PDF and generate questions from it
- [ ] Repeat the questions answered incorrectly
