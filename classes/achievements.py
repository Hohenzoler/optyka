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

    def unlock_achievement(self, achievement_name, rarity):
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

    def flashlight_achievement(self, flashlight):
        if not self.is_achievement_unlocked("first_flashlight_placed"):
            self.unlock_achievement("first_flashlight_placed", "common")

    def morrir_achievement(self, mirror):
        if not self.is_achievement_unlocked("first_mirror_placed"):
            self.unlock_achievement("first_mirror_placed", "common")