#-*- coding: utf-8 -*-

from datetime import timedelta
from workalendar.core import LunarCalendar, WesternCalendar, MON


class SouthKoreaCalendar(LunarCalendar):
    "South Korean calendar"
    FIXED_HOLIDAYS = LunarCalendar.FIXED_HOLIDAYS + (
        (3, 1, "Independence Day"),
        (5, 5, "Children's Day"),
        (6, 6, "Memorial Day"),
        (8, 15, "Liberation Day"),
        (10, 3, "National Foundation Day"),
        (10, 9, "Hangul Day"),
        (12, 25, "Christmas Day"),
    )

    def get_variable_days(self, year):
        lunar_first_day = LunarCalendar.lunar(year, 1, 1)
        days = [
            # new year (3 days)
            (lunar_first_day, "Korean New Year's Day"),
            # a day before
            (lunar_first_day - timedelta(days=1), "Korean New Year's Day"),
            # a day after
            (LunarCalendar.lunar(year, 1, 2), "Korean New Year's Day"),
            (LunarCalendar.lunar(year, 4, 8), "Buddha's Birthday"),
            # Midautumn Festival (3 days)
            (LunarCalendar.lunar(year, 8, 14), "Midautumn Festival"),
            (LunarCalendar.lunar(year, 8, 15), "Midautumn Festival"),
            (LunarCalendar.lunar(year, 8, 16), "Midautumn Festival"),
        ]
        return days


class JapanCalendar(WesternCalendar):
    "Japan calendar class"

    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (2, 11, "Foundation Day"),
        (4, 29, "Shōwa Day"),
        (5, 3, "Constitution Memorial Day"),
        (5, 4, "Greenery Day"),
        (5, 5, "Children's Day"),
        (11, 3, "Culture Day"),
        (11, 23, "Labour Thanksgiving Day"),
        (12, 23, "The Emperor's Birthday"),
    )

    def get_variable_days(self, year):
        # usual variable days

        equinoxes = self.calculate_equinoxes(year)

        days = super(JapanCalendar, self).get_variable_days(year)
        days += [
            (WesternCalendar.get_nth_weekday_in_month(year, 1, MON, 2),
                'Coming of Age Day'),

            (WesternCalendar.get_nth_weekday_in_month(year, 7, MON, 3),
                "Marine Day"),

            (equinoxes[0], "Vernal Equinox Day"),

            (WesternCalendar.get_nth_weekday_in_month(year, 9, MON, 3),
                "Respect-for-the-Aged Day"),

            (equinoxes[1], "Autumnal Equinox Day"),

            (WesternCalendar.get_nth_weekday_in_month(year, 10, MON, 2),
                "Health and Sports Day"),
        ]

        return days

    def calculate_equinoxes(self, year):
        """ calculate equinox with time zone """

        import ephem
        import pytz

        tz = pytz.timezone('Asia/Tokyo')

        d1 = ephem.next_equinox(str(year))
        d = ephem.Date(str(d1))
        equinox1 = d.datetime() + tz.utcoffset(d.datetime())

        d2 = ephem.next_equinox(d1)
        d = ephem.Date(str(d2))
        equinox2 = d.datetime() + tz.utcoffset(d.datetime())

        return (equinox1.date(), equinox2.date())
