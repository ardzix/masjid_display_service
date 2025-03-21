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
    

def bulk_create_prayer_times(mosque_id, shalat_times):
    """
    Bulk create PrayerTime records from the shalat_times list.

    :param mosque_id: The ID of the mosque.
    :param shalat_times: A list of dictionaries containing prayer times.
    """
    from api.models import Mosque, PrayerTime
    from datetime import datetime
    mosque = Mosque.objects.get(id=mosque_id)  # Fetch the mosque instance

    prayer_times_objects = [
        PrayerTime(
            mosque=mosque,
            date=datetime.strptime(day["date"], "%Y-%m-%d").date(),
            imsak=datetime.strptime(day["fajr"], "%H:%M").time(),  # Using Fajr as Imsak
            fajr=datetime.strptime(day["fajr"], "%H:%M").time(),
            sunrise=datetime.strptime(day["sunrise"], "%H:%M").time(),
            dhuhr=datetime.strptime(day["dhuhr"], "%H:%M").time(),
            asr=datetime.strptime(day["asr"], "%H:%M").time(),
            sunset=datetime.strptime(day["maghrib"], "%H:%M").time(),  # Assuming sunset is the same as Maghrib
            maghrib=datetime.strptime(day["maghrib"], "%H:%M").time(),
            isha=datetime.strptime(day["isha"], "%H:%M").time(),
            midnight=datetime.strptime(day["isha"], "%H:%M").time()  # Assuming Midnight is the same as Isha
        )
        for day in shalat_times
    ]

    # Bulk create prayer times
    PrayerTime.objects.bulk_create(prayer_times_objects)

    print(f"✅ Successfully inserted {len(prayer_times_objects)} prayer times for mosque {mosque.name}")



def run(mosque_id, months=1):
    from api.models import Mosque, PrayerTime
    mosque = Mosque.objects.get(pk=mosque_id)
    schedule = ShalatSchedule(mosque.latitude, mosque.longitude)
    schedule_data = schedule.get_schedule(months, 7)
    bulk_create_prayer_times(mosque_id, schedule_data)