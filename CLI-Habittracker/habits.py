from datetime import datetime

# Creating the habit object
class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_time = datetime.now().strftime("%Y-%m-%d")
