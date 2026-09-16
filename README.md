# FinChat

FinChat is a small grounded financial Q&A app with a browser chat interface.

## Run locally

From the project root:

```bash
./backend/run.sh
```

Then open http://127.0.0.1:8000/ for the chat interface or http://127.0.0.1:8000/docs for the API docs.

The first run creates `.venv` and installs the Python dependencies. The app can run without an OpenAI key, but answers will use a local fallback. To enable model responses, create `backend/.env`:

```env
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```
