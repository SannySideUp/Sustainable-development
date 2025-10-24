from collections import Counter
from typing import Dict, Any


class Histogram:
    """Simple ASCII histogram for dice rolls and turn totals."""

    def __init__(self):
        self.counts = Counter()

    def add(self, value: int) -> None:
        """Adds a value to the histogram count."""
        self.counts[value] += 1

    def get_data(self) -> Dict[int, int]:
        """Returns the raw histogram data."""
        return dict(self.counts)

    def get_string(self, title: str = "Histogram") -> str:
        """Generates and returns the ASCII histogram string."""
        output = [f"\n{title}"]
        if not self.counts:
            output.append(f"{title}: (no data)\n")
            return "\n".join(output)

        max_v = max(self.counts.values()) if self.counts else 1  # For scaling the bar

        for k in sorted(self.counts.keys()):
            v = self.counts[k]
            bar_len = (v * 40 // max_v) if max_v > 0 else 0
            bar = "█" * (bar_len + 1)
            output.append(f" {k:>2}: {v:>4} | {bar} ({v})")

        output.append("\n")
        return "\n".join(output)
