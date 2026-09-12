# Multi-Agent Research System

A LangChain and Streamlit research assistant that coordinates specialized agents
to search the web, extract source content, write a report, and critique the
result.

## Features

- Search Agent finds recent information with Tavily.
- Reader Agent selects a relevant result and extracts readable page content.
- Writer Chain creates a structured report with findings, conclusions, and
  sources.
- Critic Chain scores the report and lists strengths and improvements.
- Streamlit UI shows pipeline progress, raw research, the final report, and a
  Markdown download.

## Architecture

```text
User topic
	 |
	 v
Search Agent (Tavily web search)
	 |
	 v
Reader Agent (URL selection + scraping)
	 |
	 v
Writer Chain (research report)
	 |
	 v
Critic Chain (score + feedback)
```

The implementation is organized as follows:

```text
app.py                  Streamlit application
main.py                 Command-line pipeline entry point
requirements.txt        Python dependencies
src/agents/agents.py    LangChain agents and writer/critic chains
src/pipeline/pipeline.py
								Sequential CLI pipeline orchestration
src/tools/tools.py      Tavily search and web-page extraction tools
```

## Requirements

- Python 3.11 or newer
- An OpenAI API key
- A Tavily API key
- Internet access for model calls, search, and page extraction

The configured chat model is `gpt-5-nano`. Change the `ChatOpenAI` model in
`src/agents/agents.py` if your account uses a different available model.

## Installation

Run these commands from the `Multi-Agent-Research-System` directory:

```powershell
conda create -n langagent python=3.11 -y
conda activate langagent
python -m pip install -r requirements.txt
```

Alternatively, with `uv`:

```powershell
uv venv --python 3.11
uv pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root. Do not commit it.

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Both `src/agents/agents.py` and `src/tools/tools.py` load these values with
`python-dotenv`.

## Run the Streamlit application

From the project root, run:

```powershell
streamlit run app.py
```

If using `uv`, run:

```powershell
uv run streamlit run app.py
```

The browser UI accepts a topic and runs all four stages. After completion, it
displays the raw search and scraped content, the generated report, critic
feedback, and a button to download the report as Markdown.

## Run the command-line pipeline

```powershell
python main.py
```

`main.py` currently uses the example topic defined in the file and prints each
stage's output. To research another topic, update the `topic` value before
running it.

## Pipeline details

1. `web_search` calls Tavily and returns up to five result titles, URLs, and
	snippets.
2. The Search Agent reviews those results and the Reader Agent chooses a URL
	for deeper extraction.
3. `scrape_url` fetches the page and tries Trafilatura, Readability, then a
	BeautifulSoup fallback. Extracted content is limited to 5,000 characters.
4. The Writer Chain combines search results and extracted content into a
	report with an introduction, at least three key findings, a conclusion, and
	sources.
5. The Critic Chain returns a score, strengths, areas to improve, and a
	one-line verdict.

## Troubleshooting

### `File does not exist: app.py`

The command must be run from the project root, where `app.py` exists:

```powershell
Set-Location path\to\Multi-Agent-Research-System
uv run streamlit run app.py
```

You can verify the location with `Get-Location` and confirm the file with
`Test-Path .\app.py`.

### Missing API key errors

Confirm that `.env` is in the project root and contains both keys. Restart the
Streamlit process after changing environment variables.

### Scraping failures

Some websites block automated requests or require JavaScript. Try another
topic or source; the scraper reports timeout, HTTP, and extraction failures in
its returned text.

## Git and secrets

Local `.env` files, Python caches, virtual environments, and generated reports
are excluded by `.gitignore`. Only commit source code, dependency metadata, and
documentation. Rotate a key immediately if it is ever exposed.