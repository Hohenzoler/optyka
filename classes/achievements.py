import sqlite3
from classes import game
import time

class Achievements:
    def __init__(self, game):
        self.conn = sqlite3.connect('achievements.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_name TEXT PRIMARY KEY,
                unlocked INTEGER,
                rarity TEXT
            )
        """)
        self.conn.commit()
        self.game = game
        self.start_time = time.time()


        # Define the dictionary of achievements
        self.achievements_dict = {
            "first_flashlight_placed": "common",
            "first_mirror_placed": "common",
            "BIN": "uncommon",
            "back and forth": "epic",
            "need for nasa": "epic",
            "complex_numbers": "legendary",
        }

    def unlock_achievement(self, achievement_name):
        # Check if the achievement exists in the dictionary
        if achievement_name not in self.achievements_dict:
            print(f"Error: Achievement '{achievement_name}' does not exist.")
            return

        rarity = self.achievements_dict[achievement_name]
        self.cursor.execute("""
            INSERT OR REPLACE INTO achievements VALUES (?, ?, ?)
        """, (achievement_name, 1, rarity))
        self.conn.commit()
        print(f"Achievement Unlocked: {achievement_name}, Rarity: {rarity}")

    def is_achievement_unlocked(self, achievement_name):
        self.cursor.execute("""
            SELECT unlocked FROM achievements WHERE achievement_name = ?
        """, (achievement_name,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def get_achievement_rarity(self, achievement_name):
        self.cursor.execute("""
            SELECT rarity FROM achievements WHERE achievement_name = ?
        """, (achievement_name,))
        result = self.cursor.fetchone()
        return result[0] if result else "unknown"

    def handle_achievement_unlocked(self, achievement_name):
        if self.is_achievement_unlocked(achievement_name):
            print(f"Achievement already unlocked: {achievement_name}")
            game.Game.achievement_popup(game.Game)
            return

        self.unlock_achievement(achievement_name)

    def fps_achievements(self):
        if time.time()>self.start_time+5:
            if int(game.Game.return_fps(self.game)) < 10:
                self.handle_achievement_unlocked("need for nasa")
