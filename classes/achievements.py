import sqlite3

class Achievements:
    def __init__(self):
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

        # Define the dictionary of achievements
        self.achievements_dict = {
            "first_flashlight_placed": "common",
            "first_mirror_placed": "common",
            "BIN": "uncommon",
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
            return

        self.unlock_achievement(achievement_name)