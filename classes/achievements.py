class Achievements:
    def __init__(self):
        self.achievements = {
            "first_flashlight_placed": False,
            "first_mirror_placed": False,
        }

    def unlock_achievement(self, achievement_name):
        if achievement_name in self.achievements:
            self.achievements[achievement_name] = True
            print(f"Achievement Unlocked: {achievement_name}")
        else:
            print(f"No such achievement: {achievement_name}")

    def is_achievement_unlocked(self, achievement_name):
        return self.achievements.get(achievement_name, False)

    def flashlight_achievement(self, flashlight):
        if not self.is_achievement_unlocked("first_flashlight_placed"):
            self.unlock_achievement("first_flashlight_placed")

    def morrir_achievement(self, mirror):
        if not self.is_achievement_unlocked("first_mirror_placed"):
            self.unlock_achievement("first_mirror_placed")