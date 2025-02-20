from praytimes import PrayTimes
from datetime import datetime, timedelta
from typing import List, Dict

class ShalatSchedule:
    def __init__(self, lat: float, lon: float, method: str = 'UmmAlQura'):
        """
        Initialize the prayer times calculator.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param method: Calculation method (default: UmmAlQura).
        """
        self.lat = lat
        self.lon = lon
        self.method = method
        self.pray_times = PrayTimes(self.method)  # Create a PrayTimes instance

    def adjust_method(self, fajr_angle: float, isha_angle: float):
        """
        Adjust the angles for Fajr and Isha calculation (optional).

        :param fajr_angle: Fajr angle in degrees.
        :param isha_angle: Isha angle in degrees.
        """
        self.pray_times.adjust({'fajr': fajr_angle, 'isha': isha_angle})

    def get_schedule(self, months: int, timezone: int = 0) -> List[Dict[str, str]]:
        """
        Generate a prayer time schedule for a specific time range.

        :param months: Number of months from today.
        :param timezone: Timezone offset (default: 0 for UTC).
        :return: A list of dictionaries with prayer times for each day.
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days=months * 30)  # Approximate 30 days per month
        schedule = []

        current_date = start_date
        while current_date <= end_date:
            # Convert date to tuple format required by praytimes (YYYY, MM, DD)
            date_tuple = (current_date.year, current_date.month, current_date.day)

            # Get prayer times
            times = self.pray_times.getTimes(date_tuple, (self.lat, self.lon), timezone)

            # Append to schedule
            schedule.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'imsak': times['imsak'],
                'fajr': times['fajr'],
                'sunrise': times['sunrise'],
                'dhuhr': times['dhuhr'],
                'asr': times['asr'],
                'sunset': times['sunset'],
                'maghrib': times['maghrib'],
                'isha': times['isha'],
                'midnight': times['midnight']
            })

            # Move to the next day
            current_date += timedelta(days=1)

        return schedule
