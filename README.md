# StudyMuse

# Fun & Relatable Personal Assistant

A friendly, AI-powered personal assistant built with Streamlit and OpenAI's GPT models. Designed for students and everyday users, this app helps with text summarization, improvement, creative transformations, motivation, note organization, and Q&A tutoring with file upload support.

## Features

- **Summarize**: Condense long texts into short, clear summaries.
- **Improve Text**: Polish and refine your writing for professionalism and clarity.
- **Fun Transform**: Transform text into various styles like Shakespearean, rap, meme, sarcastic, roast, pirate, Yoda, cowboy, or poem.
- **Motivation**: Generate relatable motivational quotes on topics like studying, procrastination, stress, success, or friendship.
- **Notes Organizer**: Convert notes into bullets, mindmap-style hierarchies, timelines, or flashcards.
- **Q&A Chat (Tutor)**: Ask questions and get helpful answers, with optional PDF or TXT file upload for context (e.g., lecture notes).

## Requirements

- Python 3.7+
- OpenAI API key (for full functionality)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   - Create a `.env` file in the project directory and add:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Or export it as an environment variable:
     ```
     export OPENAI_API_KEY="your_openai_api_key_here"
     ```

## Usage

Run the app with:
```
streamlit run streamlit_personal_assistant.py
```

Open the provided local URL in your browser. Select a mode from the sidebar, input your text or question, and click "Run" to get results.

### Modes Explained

- **Summarize**: Paste text and get a concise summary.
- **Improve Text**: Input draft text for polishing.
- **Fun Transform**: Choose a style and transform your text creatively.
- **Motivation**: Select a topic and generate a quote.
- **Notes Organizer**: Paste notes and choose output format (bullets, mindmap, timeline, flashcards).
- **Q&A Chat (Tutor)**: Ask a question; optionally upload a PDF or TXT file for additional context.

### Customization

- Adjust response tone: Friendly, Formal, Casual, or Funny.
- Control output length with the max tokens slider.
- Set creativity level with the temperature slider.

## Configuration

The app uses the following environment variables (optional):

- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_MODEL`: Model to use (default: gpt-4o-mini). Change to gpt-3.5-turbo or others as needed.
- `API_BACKEND`: Currently set to "openai"; can be extended for other LLM providers.

## Safety and Limitations

- Includes a basic profanity filter to prevent certain harmful inputs.
- Relies on OpenAI's API; ensure you have credits and comply with their usage policies.
- For production use, consider adding more robust error handling and security measures.

## Contributing

Feel free to fork this repo and submit pull requests. Ideas for new features or improvements are welcome!

## License

This project is open-source. Use at your own risk.

## Built With

- [Streamlit](https://streamlit.io/) - For the web UI
- [OpenAI API](https://openai.com/api/) - For AI-powered text processing
- [PyPDF2](https://pypi.org/project/PyPDF2/) - For PDF text extraction
- [python-dotenv](https://pypi.org/project/python-dotenv/) - For environment variable loading

Enjoy your fun personal assistant! 🎒✨
