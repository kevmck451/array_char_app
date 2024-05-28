
import time

# TIME CLASS TO GIVE STATS ABOUT HOW LONG FUNCTION TAKES
class time_class:
    def __init__(self, name):
        self.start_time = time.time()
        self.name = name

    def stats(self):
        total_time = round((time.time() - self.start_time), 1)
        mins = int(total_time // 60)  # Get the full minutes
        secs = int(total_time % 60)  # Get the remaining seconds

        # Formatting for two digits
        mins_str = f'{mins:02d}'
        secs_str = f'{secs:02d}'

        # Combine minutes and seconds in the format "00:00"
        formatted_time = f'{mins_str}:{secs_str}'

        return formatted_time

    def reaction_time(self):
        reaction_time = round((time.time() - self.start_time), 2)
        # print(reaction_time)
        return reaction_time