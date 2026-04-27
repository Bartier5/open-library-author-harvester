
A production-grade Python scraper that builds a database of 10,000+ book
and author records from the Open Library API, with resumable checkpointing
and formatted Excel output.

Built as a portfolio project demonstrating large-scale data harvesting,
fault-tolerant scraping, and professional data delivery.

---

## Features

- Harvests 10,000+ records across multiple book subjects
- Resumable — crashes or interruptions resume from last saved page
- Duplicate-safe — INSERT OR IGNORE prevents double entries
- Clean Excel output — formatted two-sheet .xlsx with frozen headers,
  alternating row colors, and a subject summary sheet
- Respectful scraping — 1 second delay between requests

---

## Tech Stack

| Tool       | Purpose                        |
|------------|--------------------------------|
| requests   | HTTP requests to Open Library  |
| sqlite3    | Local database + checkpointing |
| openpyxl   | Excel file generation          |
| tqdm       | Terminal progress bar          |

---

## Project Structure
open-library-author-harvester/
├── main.py          # Orchestration and harvest loop
├── fetcher.py       # Open Library API pagination
├── storage.py       # SQLite checkpointing and CRUD
├── exporter.py      # Excel output with openpyxl
├── display.py       # tqdm progress bar and summary
├── config.py        # Settings and constants
└── requirements.txt

---

## Setup

```bash
git clone https://github.com/Bartier5/open-library-author-harvester
cd open-library-author-harvester
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

The script will:
1. Initialize the SQLite database
2. Loop through configured subjects (fiction, history, science, etc.)
3. Fetch pages of 100 records at a time from Open Library
4. Save progress after every page — safe to interrupt and resume
5. Stop when TARGET_RECORDS is reached
6. Export `author_database.xlsx` with two sheets

---

## Output

**Books sheet** — all records with columns:
`#` | `Title` | `Author` | `Publish Year` | `Subject` | `ISBN`

**Summary sheet** — record count per subject

---

## Configuration

Edit `config.py` to adjust:

```python
TARGET_RECORDS = 10000   # How many records to collect
PAGE_SIZE = 100          # Records per API request
REQUEST_DELAY = 1        # Seconds between requests
SUBJECTS = [...]         # Which subjects to harvest
```

---

## Resume Behaviour

If the script is interrupted mid-run, simply run `python main.py` again.
The checkpoint system reads the last saved page per subject from SQLite
and continues from exactly where it left off. No duplicate records,
no wasted requests.

---

## Skills Demonstrated

- Paginated API consumption at scale
- Fault-tolerant resumable scraping with SQLite checkpointing
- Bulk database inserts with duplicate handling
- Professional Excel deliverable generation
- Clean modular project structure