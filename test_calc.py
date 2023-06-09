
from main_calc import calc_point, calculate_semester_options


def test_is_lawyer():
    data = {'is_lawyer': True}
    assert calc_point(data) == "A PMTSZ hatálya a Politikatudományi Műhely nem jogász hallgatóira terjed ki."


def test_semester_intervals():
    test_year = 2020
    test_interval = [(2010, 2011, 1), (2010, 2011, 2), (2011, 2012, 1), (2011, 2012, 2),
                     (2012, 2013, 1), (2012, 2013, 2), (2013, 2014, 1), (2013, 2014, 2),
                     (2014, 2015, 1), (2014, 2015, 2), (2015, 2016, 1), (2015, 2016, 2),
                     (2016, 2017, 1), (2016, 2017, 2), (2017, 2018, 1), (2017, 2018, 2),
                     (2018, 2019, 1), (2018, 2019, 2), (2019, 2020, 1), (2019, 2020, 2),
                     (2020, 2021, 1), (2020, 2021, 2), (2021, 2022, 1), (2021, 2022, 2),
                     (2022, 2023, 1), (2022, 2023, 2), (2023, 2024, 1), (2023, 2024, 2),
                     (2024, 2025, 1), (2024, 2025, 2), (2025, 2026, 1), (2025, 2026, 2),
                     (2026, 2027, 1), (2026, 2027, 2), (2027, 2028, 1), (2027, 2028, 2),
                     (2028, 2029, 1), (2028, 2029, 2), (2029, 2030, 1), (2029, 2030, 2),
                     (2030, 2031, 1), (2030, 2031, 2), (2031, 2032, 1), (2031, 2032, 2)]
    assert calculate_semester_options(test_year) == test_interval
