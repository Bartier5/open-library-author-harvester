from tqdm import tqdm

class HarvesterProgress:
    def __init__(self, target: int, initial: int = 0):
        self.bar = tqdm(
            total=target,
            initial=initial,
            desc="Harvesting records",
            unit=" records",
            colour="green",
            dynamic_ncols=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )
        self.current_subject = ""
    def update(self, count: int):
        self.bar.update(count)
    def set_subject(self, subject: str):
        self.current_subject = subject
        self.bar.set_description(f"Subject: {subject:<12}")

    def set_postfix(self, **kwargs):
        self.bar.set_postfix(**kwargs)

    def close(self):
        self.bar.close()


def print_summary(subjects_done: list[str], total_records: int, output_file: str):
    width = 40
    print("\n" + "=" * width)
    print(" HARVEST COMPLETE ".center(width))
    print("=" * width)
    print(f"  Total records collected : {total_records:,}")
    print(f"  Subjects completed      : {len(subjects_done)}")
    print(f"  Output file             : {output_file}")
    print("-" * width)
    print("  Subjects scraped:")
    for subject in subjects_done:
        print(f"    ✓ {subject}")
    print("=" * width + "\n")