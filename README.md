

# Greek RAG Project

A retrieval-augmented generation (RAG) app for Greek vocabulary.  
It retrieves dictionary entries from a corpus and uses OpenAI’s GPT models 
to provide concise explanations in Greek.

---

## Features

- Retrieve Greek word/phrase definitions from a local corpus 
(`el-extract.jsonl.gz`)
- BM25-based retrieval for relevant dictionary entries
- GPT-powered explanation and example sentences
- Web interface using FastAPI and Jinja2 templates

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/anna-christina-mikr/greek-rag.git
cd greek-rag
```

### 2. Create and activate your environment
```bash 
conda env create -f env.yml
conda activate greekapp
```
or using pip 
```bash 
python -m venv greekapp
source greekapp/bin/activate  # macOS/Linux
greekapp\Scripts\activate     # Windows
pip install -r requirements.txt
```
### 3. Set up your Open AI API Key 
export OPENAI_API_KEY = "your_api_key_here"

Note: Never commit your API key to GitHub. It’s read from the environment.


##Running the App Locally
```bash
uvicorn app:app --reload
 
-Navigate to http://localhost:8000/ in your browser.

-Enter a Greek word/phrase to search.

-The app will return dictionary entries and generate a concise 
explanation.
## Project Structure
greek-rag/
│
├─ app.py             # Main FastAPI app
├─ retrieval.py       # BM25 corpus loading and search
├─ templates/         # Jinja2 HTML templates
├─ static/            # CSS, JS, images
├─ el-extract.jsonl.gz # Greek corpus (required for BM25)
├─ env.yml            # Conda environment (ignored in GitHub)
├─ requirements.txt   # Pip dependencies
└─ README.md
