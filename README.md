

# Greek RAG Project

A retrieval-augmented generation (RAG) app for Greek vocabulary.  Greek is considered a low resource language for AI and NLP applications so I thought I would give it a shot. 
The model retrieves dictionary entries from a Wiktionary corpus and uses an OpenAI API to provide concise explanations in Greek.

---

## Features

- Retrieve Greek word/phrase definitions from a local corpus 
(`el-extract.jsonl.gz`)
- BM25-based retrieval for relevant dictionary entries
- GPT-powered explanation and example sentences
- Web interface using FastAPI and Jinja2 templates

## Data Sources

The dictionary data used in this project is sourced from **Wiktionary** raw data dumps, extracted and processed by [kaikki.org](https://kaikki.org/dictionary/rawdata.html).
Currently, we use the Greek language extraction (`el-extract.jsonl.gz`). In the future, we plan to integrate additional sources to enrich the vocabulary coverage.

## Retrieval Method (BM25)

To find relevant dictionary entries for a user's query, we use **BM25 (Best Matching 25)**.
BM25 is a ranking function used by search engines to estimate the relevance of documents to a given search query. It improves upon simple keyword matching (TF-IDF) by:
- **Term Frequency Saturation**: Preventing extremely frequent terms from dominating the score.
- **Document Length Normalization**: Adjusting scores so that shorter documents (which might be more focused) are treated fairly compared to very long ones.

In this app, we index the dictionary definitions and examples using BM25 to retrieve the top-k most relevant entries before passing them to the LLM for synthesis.

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
### Notes: 
In my version, I ask the RAG to provide, one or two definitions and example sentences. This covers words with mutiple semantic meanings. For my BM25 function, every time it queries I use k=5 to retrieve the top 5 most relevant entries. But this can be adjusted, for lower resource languages, maybe a higher k would be better. I also plan to use SLANG.gr as a secondary source to enrich the vocabulary coverage, but this requires thourough web scraping, anyone feel free to try this out!