import random

class DiceDifficulty:
    def __init__(self):
        self.modes = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]

    def get_available_difficulties(self):
        return ["noob", "casual", "challenger", "veteran", "elite", "legendary"]

    def get_difficulty_description(self, difficulty):
        desc = {
            "noob": "Low skill, rolls only twice per turn.",
            "casual": "Slightly smarter, rolls four times.",
            "challenger": "Moderate AI, takes a few risks.",
            "veteran": "Experienced AI, rolls carefully.",
            "elite": "Tough AI, rolls aggressively but rarely busts.",
            "legendary": "Almost perfect AI, very risky but rewards high."
        }
        return desc.get(difficulty.lower(), "Unknown difficulty.")

    def _roll_pattern(self, lists):
        return random.choice(random.choice(lists))

    def noob(self):       return self._roll_pattern([[1,2,3,4,5,6]])
    def casual(self):     return self._roll_pattern([[1,2,3,4,5,6],[2,3,4,5,6]])
    def challenger(self): return self._roll_pattern([[1,2,3,4,5,6],[2,3,4,5,6],[3,4,5,6]])
    def veteran(self):    return self._roll_pattern([[1,2,3,4,5,6],[2,3,4,5,6],[3,4,5,6],[4,5,6]])
    def elite(self):      return self._roll_pattern([[1,2,3,4,5,6],[2,3,4,5,6],[3,4,5,6],[4,5,6],[5,6]])
    def legendary(self):  return self._roll_pattern([[1,2,3,4,5,6],[2,3,4,5,6],[3,4,5,6],[4,5,6],[5,6],[6]])

    def roll(self, mode):
        mode = str(mode).strip().lower()

        roll_counts = {
            "noob": 2,
            "casual": 4,
            "challenger": 6,
            "veteran": 8,
            "elite": 10,
            "legendary": 12
        }

        if mode not in roll_counts:
            raise ValueError("Unknown mode. Please try again.")

        total = 0

        for i in range(roll_counts[mode]):

            match mode:
                case "noob":       value = self.noob()
                case "casual":     value = self.casual()
                case "challenger": value = self.challenger()
                case "veteran":    value = self.veteran()
                case "elite":      value = self.elite()
                case "legendary":  value = self.legendary()

            print(f"Roll {i+1}: {value}")

            if value == 1:
                return 1

            total += value
        return total