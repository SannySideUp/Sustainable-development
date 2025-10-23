from collections import Counter


class Histogram:
    """Simple ASCII histogram for dice rolls and turn totals."""
    def __init__(self):
        self.counts = Counter()

    def add(self, value):
        self.counts[value] += 1

    def show(self, title="Histogram"):
        if not self.counts:
            print(f"{title}: (no data)")
            return
        print(f"\n{title}")
        total = sum(self.counts.values())
        for k in sorted(self.counts.keys()):
            v = self.counts[k]
            bar = '█' * (v * 40 // total + 1)
            print(f" {k:>2}: {v:>4} | {bar} ({v})")
        print()
