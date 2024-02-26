import sqlite3
import time
# from classes import mixer_c

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
            "let there be light": "common",
            "is it... me?": "common",
            "some color in this black and white world": "common",
            "first step to... glasses": "common",
            "a whole new world": "common",
            "kaboom": "uncommon",
            "a new creature": "uncommon",
            "you just found more options": "rare",
            "U are weird...": "rare",
            # "not much time left to live": "rare",
            "epilepsy": "epic",
            # "get a new computer": "epic",
            "so you've chosen death": "epic",
            "white mode": "legendary",
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
        self.game.mixer.achievement_sound()
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
            return
        self.rarity = self.achievements_dict[achievement_name]
        self.game.achievement_popup(achievement_name, self.rarity)
        self.unlock_achievement(achievement_name)

    def fps_achievements(self):
        pass
        # if time.time()>self.start_time+5:
        #     if int(self.game.return_fps()) < 20:
        #         self.handle_achievement_unlocked("not much time left to live")
        #     if time.time() < self.start_time+30:
        #         if int(self.game.return_fps()) < 20:
        #             self.handle_achievement_unlocked("get a new computer")
