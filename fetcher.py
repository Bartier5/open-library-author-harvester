import requests
import time
from config import BASE_URL, PAGE_SIZE, REQUEST_DELAY

def fetch_page(subject: str, page: int) -> list[dict]:
    params = {
        "subject":subject,
        "fields": "title,author_name,first_publish_year,isbn",
        "limit": PAGE_SIZE,
        "offset": page * PAGE_SIZE,
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print(f"  [TIMEOUT] Subject: {subject} | Page: {page} — skipping.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP ERROR] {e} — skipping page.")
        return []
    except requests.exceptions.ConnectionError:
        print(f"  [CONNECTION ERROR] Check your internet — skipping page.")
        return []
    records = []
    for doc in data.get("docs", []):
        title = doc.get("title", "").strip()
        if not title:
            continue
        author_list = doc.get("author_name",[])
        author = author_list[0] if author_list else None
        publish_year = doc.get("first_publish_year", None)

        isbn_list = doc.get("isbn", [])
        isbn = isbn_list[0] if isbn_list else None
        records.append({
            "title":        title,
            "author":       author,
            "publish_year": publish_year,
            "subject":      subject,
            "isbn":         isbn,
        })        
    time.sleep(REQUEST_DELAY)
    return records
def fetch_subject_total(subject: str) -> int:
    params = {
        "subject": subject,
        "limit": 1,
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("numFound", 0)
    except Exception:
        return 0