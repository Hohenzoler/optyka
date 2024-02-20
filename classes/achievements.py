import sqlite3
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
            "here is your first achievement ;)": "common",
            "first_flashlight_placed": "common",
            "first_mirror_placed": "common",
            "first_colored_glass_placed": "common",
            "first_lens_placed": "common",
            "first_prism_placed": "common",
            "BIN": "uncommon",
            "topopisy": "uncommon",
            "parameters": "rare",
            "U are weird...": "rare",
            "back and forth": "epic",
            "need for nasa": "epic",
            "so you've chosen death": "epic",
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
            # self.game.achievement_popup()
            return

        self.unlock_achievement(achievement_name)

    def fps_achievements(self):
        if time.time()>self.start_time+5:
            if int(self.game.return_fps()) < 10:
                self.handle_achievement_unlocked("need for nasa")
