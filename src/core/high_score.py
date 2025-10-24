import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Any

HIGHSCORE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "pig_highscore.json"
)


class HighScore:
    """Manages persistent high score / statistics JSON file."""

    def __init__(self, filename=HIGHSCORE_FILE):
        self.filename = filename
        self.data: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        """Loads high score data from the JSON file."""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    content = f.read()
                    self.data = json.loads(content) if content else {}
            except json.JSONDecodeError:
                print(
                    f"Warning: HighScore file '{self.filename}' is corrupted. Starting with empty data."
                )
                self.data = {}
            except Exception as e:
                print(f"Error loading HighScore file: {e}. Starting with empty data.")
                self.data = {}
        else:
            self.data = {}

    def _save(self):
        """Saves the current high score data to the JSON file."""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        try:
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving HighScore file: {e}")

    def _ensure_player(self, player_id: str, player_name: str) -> None:
        """Ensures a player record exists, initializing it if necessary."""
        if player_id not in self.data:
            now_utc = datetime.now(timezone.utc).isoformat()
            self.data[player_id] = {
                "name": player_name,
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "total_score": 0,
                "created": now_utc,
                "last_played": now_utc,
                "best_score": 0,
            }

    def record_game(
        self, winner: Any, loser: Any, winner_score: int, loser_score: int
    ) -> None:
        """
        Records the results of a single game. This method was missing and caused the crash.

        Args:
            winner, loser: Objects expected to have 'player_id' and 'name'.
            winner_score, loser_score: Final scores.
        """
        now_utc = datetime.now(timezone.utc).isoformat()

        self._ensure_player(winner.player_id, winner.name)
        w_rec = self.data[winner.player_id]

        w_rec["games_played"] += 1
        w_rec["wins"] += 1
        w_rec["total_score"] += winner_score
        w_rec["last_played"] = now_utc
        if winner_score > w_rec.get("best_score", 0):
            w_rec["best_score"] = winner_score

        self._ensure_player(loser.player_id, loser.name)
        l_rec = self.data[loser.player_id]

        l_rec["games_played"] += 1
        l_rec["losses"] += 1
        l_rec["total_score"] += loser_score
        l_rec["last_played"] = now_utc
        if loser_score > l_rec.get("best_score", 0):
            l_rec["best_score"] = loser_score

        self._save()

    def list_top(self, n: int = 10) -> List[Tuple[str, Dict[str, Any]]]:
        def score_key(item):
            pid, rec = item
            wins = rec.get("wins", 0)
            games = rec.get("games_played", 1)
            winrate = wins / games if games else 0
            avg_score = rec.get("total_score", 0) / games if games else 0
            return (wins, winrate, avg_score)

        items = sorted(self.data.items(), key=score_key, reverse=True)
        return items[:n]

    def get_scores_string(self) -> str:
        if not self.data:
            return "No players yet."

        output = ["\n=== HIGH SCORES / PLAYER STATS ==="]
        rows = []
        for pid, rec in self.data.items():
            games = rec.get("games_played", 0)
            wins = rec.get("wins", 0)
            losses = rec.get("losses", 0)
            winrate = (wins / games * 100) if games else 0
            avg = (rec.get("total_score", 0) / games) if games else 0
            rows.append(
                (
                    rec.get("name", "?"),
                    pid,
                    games,
                    wins,
                    losses,
                    f"{winrate:.1f}%",
                    f"{avg:.1f}",
                )
            )

        rows.sort(key=lambda r: (r[3], float(r[6])), reverse=True)

        header = " Name                        | Games | Wins | Losses | Win%  | Avg score | Player ID"
        output.append(header)
        output.append("-" * len(header))

        for name, pid, games, wins, losses, winp, avg in rows:
            output.append(
                f" {name:25} | {games:5} | {wins:4} | {losses:6} | {winp:5} | {avg:9} | {pid[:8]}"
            )

        output.append("\n")
        return "\n".join(output)

    def get_top_players_string(self, n: int = 10) -> str:
        top_players = self.list_top(n)

        if not top_players:
            return "No player scores available."

        result = "Top Player Scores (Ranked by Wins, Win%, Avg Score):\n"
        result += "=" * 70 + "\n"

        for i, (pid, rec) in enumerate(top_players, 1):
            name = rec.get("name", "Unknown")
            wins = rec.get("wins", 0)
            games = rec.get("games_played", 0)
            winrate = (wins / games * 100) if games else 0
            avg_score = rec.get("total_score", 0) / games if games else 0

            result += f"{i:2}. {name:20} | Wins: {wins:3} | Games: {games:3} | Win%: {winrate:5.1f}% | Avg: {avg_score:6.1f}\n"

        return result

    def clear_high_scores(self) -> str:
        """Clears high scores and returns a status message."""
        self.data = {}
        self._save()
        return "High scores cleared successfully."
