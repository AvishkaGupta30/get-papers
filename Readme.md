# get Papers - PubMed Research Fetcher

This is a Python command-line tool to fetch research papers from PubMed, and filter them by author affiliation (e.g., pharmaceutical or biotech companies).

## Features

- Fetch papers from PubMed using a search query
- Detect authors from non-academic institutions
- Save filtered results in a CSV file
- Command-line options:
  - `--query` to enter your topic (e.g., "cancer")
  - `--file` to save output as CSV
  - `--debug` to print debug logs
  - `--help` to show usage instructions

## How to Use

1. Clone the project
   ```bash
   git clone https://github.com/your-username/get-papers.git
   cd get-papers

2. Install dependencies with Poetry
   ```bash
   poetry install

3. Run the tool:
   poetry run python papers/main.py --query "breast-cancer" --file result3.csv

4. Dependencies
   BioPython
   Poetry

5. Output Example
   CSV with columns:
   PubMed ID
   Title
   Publication Date
   Non-academic Author
   Company Affiliation
   Corresponding Author Email


 License
MIT License — anyone can use, share, and modify this code freely.


---

### Next steps:
After replacing and saving your README:

1. Open terminal:
   ```bash
   git add README.md
   git commit -m "Final updated README with instructions and license"
   git push



