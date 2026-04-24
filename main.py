from config import SUBJECTS, TARGET_RECORDS, OUTPUT_FILE
from storage import (
    initialize_db,
    save_books,
    save_checkpoint,
    mark_subject_complete,
    get_checkpoint,
    get_total_records,
)
from fetcher import fetch_page, fetch_subject_total
from display import HarvesterProgress, print_summary
from exporter import export_to_excel
import math

def main():
    print("Open Library Author Harvester")
    print("=" * 40)
    initialize_db()
    current_count = get_total_records()
    if current_count >= TARGET_RECORDS:
        print(f"Already have {current_count:, } records. Exporting... ")
        export_to_excel()
        return
    progress = HarvesterProgress(
        target = TARGET_RECORDS,
        initial=current_count)
    subjects_done = []
    skipped_total = 0
    for subject in SUBJECTS:
        if get_total_records() >= TARGET_RECORDS:
            break

        checkpoint = get_checkpoint(subject)

        if checkpoint == -1:
            subjects_done.append(subject)
            continue

        start_page = checkpoint
        total_available = fetch_subject_total(subject)

        if total_available == 0:
            continue

        total_pages = math.ceil(total_available / 100)
        progress.set_subject(subject)

        for page in range(start_page, total_pages):
            if get_total_records() >= TARGET_RECORDS:
                break

            records = fetch_page(subject, page)

            if not records:
                save_checkpoint(subject, page)
                continue

            before = get_total_records()
            save_books(records)
            after = get_total_records()

            new_records = after - before
            skipped = len(records) - new_records
            skipped_total += skipped

            save_checkpoint(subject, page + 1)
            progress.update(new_records)
            progress.set_postfix(
                saved=after,
                skipped=skipped_total
            )

        else:
            mark_subject_complete(subject)
            subjects_done.append(subject)

    
    progress.close()

    final_count = get_total_records()
    export_to_excel()
    print_summary(subjects_done, final_count, OUTPUT_FILE)


if __name__ == "__main__":
    main()
    