
class DayNightCycle():
    def __init__(self, time=0):
        self.initial_time = time
        self.time = 0
        self.minutes = self.get_minutes()
        self.hours = self.get_hours()
        self.day = self.get_day()
        self.am_or_pm = self.get_am_or_pm()
        self.times_of_day = self.get_times_of_day()


    def get_time(self):
        return self.time

    def update_time(self, increment):
        self.time = self.initial_time + increment
        self.minutes = self.get_minutes()
        self.hours = self.get_hours()
        self.day = self.get_day()
        self.am_or_pm = self.get_am_or_pm()
        self.times_of_day = self.get_times_of_day()

    def get_minutes(self):
        return self.time % 60

    def get_hours(self):
        return int(self.time/60)

    def get_am_or_pm(self ):
        remainder = self.hours % 24
        if 12 <= remainder < 24:
            return 'PM'
        elif remainder == 24 or remainder < 12:
            return 'AM'
        return None

    def get_times_of_day(self):
        remainder = self.hours % 24
        if remainder >= 22 or remainder <= 2:
            return 'NIGHT'
        elif remainder >= 2 and remainder < 12:
            return 'MORNING'
        elif remainder > 12 and remainder < 17:
            return 'AFTERNOON'
        elif remainder >= 17:
            return 'EVENING'
        else:
            return 'NOON'

    def get_day(self):
        return int(self.hours / 24)



    def render_time(self):
        hour = 12 if self.hours % 12 == 0 else self.hours % 12
        return f'{hour:02d}:{self.minutes:02d} {self.am_or_pm} {self.times_of_day}'







