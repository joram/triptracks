from apps.integrations.yrno_forecast import get_weather, get_icons, get_daily_weather

def test_daily_forecast():
    f = get_daily_weather(-123.3656, 48.4284)
    import pprint
    pprint.pprint(f)
    assert 1==2


# def test_answer():
#     icons = get_icons(-123.3656, 48.4284)
#
#     assert len(icons) == 93