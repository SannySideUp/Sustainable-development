class HighScore:
    """Manages persistent high score / statistics JSON file.
    Structure: { player_id: { 'name':..., 'games_played':n, 'wins':n, 'losses':n, 'total_score':n, 'created':date, 'last_played':date } }
    """
    def __init__(self, filename=HIGHSCORE_FILE):
        self.filename = filename
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                print("Warning: could not read highscore file; starting fresh.")
                self.data = {}
        else:
            self.data = {}

    def _save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Warning: could not save highscores:", e)

    def ensure_player(self, player):
        """Ensure a player exists in the store. player is Player object."""
        pid = player.player_id
        if pid not in self.data:
            now = datetime.datetime.utcnow().isoformat()
            self.data[pid] = {
                'name': player.name,
                'games_played': 0,
                'wins': 0,
                'losses': 0,
                'total_score': 0,
                'created': now,
                'last_played': now,
            }
            self._save()
        else:
            # ensure name is up-to-date (but keep history under same id)
            self.data[pid]['name'] = player.name
            self._save()

    def record_game(self, winner_player, loser_player, winner_score, loser_score):
        now = datetime.datetime.utcnow().isoformat()
        for p, won, sc_other in [(winner_player, True, loser_score), (loser_player, False, winner_score)]:
            pid = p.player_id
            if pid not in self.data:
                # create if missing (maybe user changed machines)
                self.data[pid] = {
                    'name': p.name,
                    'games_played': 0,
                    'wins': 0,
                    'losses': 0,
                    'total_score': 0,
                    'created': now,
                    'last_played': now,
                }
            rec = self.data[pid]
            rec['name'] = p.name
            rec['games_played'] = rec.get('games_played', 0) + 1
            if won:
                rec['wins'] = rec.get('wins', 0) + 1
            else:
                rec['losses'] = rec.get('losses', 0) + 1
            rec['total_score'] = rec.get('total_score', 0) + (winner_score if won else loser_score)
            rec['last_played'] = now
        self._save()

    def change_player_name(self, player, new_name):
        pid = player.player_id
        if pid in self.data:
            self.data[pid]['name'] = new_name
            self._save()

    def list_top(self, n=10):
        # Sort by wins then winrate then average score
        def score_key(item):
            pid, rec = item
            wins = rec.get('wins', 0)
            games = rec.get('games_played', 1)
            winrate = wins / games if games else 0
            avg_score = rec.get('total_score', 0) / games if games else 0
            return (wins, winrate, avg_score)
        items = sorted(self.data.items(), key=score_key, reverse=True)
        return items[:n]

    def find_by_name(self, name):
        for pid, rec in self.data.items():
            if rec.get('name', '').lower() == name.lower():
                return pid, rec
        return None, None

    def show_all(self):
        if not self.data:
            print("No players yet.")
            return
        print("\nHigh-score / player stats:")
        rows = []
        for pid, rec in self.data.items():
            games = rec.get('games_played', 0)
            wins = rec.get('wins', 0)
            losses = rec.get('losses', 0)
            winrate = (wins / games * 100) if games else 0
            avg = (rec.get('total_score', 0) / games) if games else 0
            rows.append((rec.get('name','?'), pid, games, wins, losses, f"{winrate:.1f}%", f"{avg:.1f}"))
        rows.sort(key=lambda r: (r[3], float(r[6])), reverse=True)
        print(" Name                        | Games | Wins | Losses | Win%  | Avg score | Player ID")
        print("-"*100)
        for name, pid, games, wins, losses, winp, avg in rows:
            print(f" {name:25} | {games:5} | {wins:4} | {losses:6} | {winp:5} | {avg:9} | {pid[:8]}")
        print()
