from django.shortcuts import render
import json
import urllib.parse
import urllib.request


CITIES = {
    "bishkek": {"name": "Бишкек", "lat": 42.8746, "lon": 74.5698},
    "osh": {"name": "Ош", "lat": 40.5283, "lon": 72.7985},
    "naryn": {"name": "Нарын", "lat": 41.4287, "lon": 75.9911},
    "talas": {"name": "Талас", "lat": 42.5228, "lon": 72.2427},
    "karakol": {"name": "Каракол", "lat": 42.4923, "lon": 78.3936},
    "jalalabad": {"name": "Джалал-Абад", "lat": 40.9333, "lon": 73.0},
}

WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Иней",
    51: "Морось слабая",
    53: "Морось умеренная",
    55: "Морось сильная",
    56: "Ледяная морось слабая",
    57: "Ледяная морось сильная",
    61: "Дождь слабый",
    63: "Дождь умеренный",
    65: "Дождь сильный",
    66: "Ледяной дождь слабый",
    67: "Ледяной дождь сильный",
    71: "Снег слабый",
    73: "Снег умеренный",
    75: "Снег сильный",
    77: "Снежные зерна",
    80: "Ливни слабые",
    81: "Ливни умеренные",
    82: "Ливни сильные",
    85: "Снегопады слабые",
    86: "Снегопады сильные",
    95: "Гроза",
    96: "Гроза с градом",
    99: "Гроза с сильным градом",
}


def wind_direction_ru(deg):
    if deg is None:
        return "—"
    directions = [
        "Северный",
        "Северо-северо-восточный",
        "Северо-восточный",
        "Востоко-северо-восточный",
        "Восточный",
        "Востоко-юго-восточный",
        "Юго-восточный",
        "Юго-юго-восточный",
        "Южный",
        "Юго-юго-западный",
        "Юго-западный",
        "Западо-юго-западный",
        "Западный",
        "Западо-северо-западный",
        "Северо-западный",
        "Северо-северо-западный",
    ]
    idx = int((deg + 11.25) / 22.5) % 16
    return directions[idx]


def weather_page(request):
    city_key = request.GET.get("city", "bishkek")
    if city_key not in CITIES:
        city_key = "bishkek"
    city = CITIES[city_key]

    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "auto",
        "windspeed_unit": "ms",
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)

    error = None
    current = {}
    forecast = []

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current", {})
        daily = data.get("daily", {})
        days = daily.get("time", [])
        max_t = daily.get("temperature_2m_max", [])
        min_t = daily.get("temperature_2m_min", [])
        codes = daily.get("weather_code", [])

        for i in range(min(len(days), 7)):
            code = codes[i] if i < len(codes) else None
            forecast.append(
                {
                    "date": days[i],
                    "t_max": max_t[i] if i < len(max_t) else None,
                    "t_min": min_t[i] if i < len(min_t) else None,
                    "text": WEATHER_CODES.get(code, "—"),
                    "code": code,
                }
            )
    except Exception:
        error = "Не удалось получить погоду. Попробуйте позже."

    context = {
        "cities": CITIES,
        "city_key": city_key,
        "city_name": city["name"],
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_dir": wind_direction_ru(current.get("wind_direction_10m")),
        "weather_text": WEATHER_CODES.get(current.get("weather_code"), "—"),
        "forecast": forecast,
        "error": error,
    }

    return render(request, "page/weather.html", context)
