import requests
from django.shortcuts import render
from datetime import datetime

def home(request):
    city = request.GET.get('city', 'Delhi')
    api_key = "1c1bcb9fc19a2f51bc9c212d0fb65948"
    units = request.GET.get('units', 'metric') # Celsius ya Fahrenheit ke liye
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    res = requests.get(url).json()
    
    # --- ERROR HANDLING ---
    if res.get('cod') != '200':
        return render(request, "index.html", {"error": f"City '{city}' not found! Check spelling."})

    # Weather Condition for Dynamic Background
    main_status = res['list'][0]['weather'][0]['main'].lower() # e.g., 'clouds', 'rain'

    current_weather = {
        "city": city,
        "temp": res['list'][0]['main']['temp'],
        "desc": res['list'][0]['weather'][0]['description'],
        "status": main_status,
        "icon": res['list'][0]['weather'][0]['icon'],
        "time": datetime.now().strftime("%I:%M %p"),
        "unit_symbol": "°C" if units == 'metric' else "°F"
    }

    forecast_list = []
    for item in res['list'][::8]:
        forecast_list.append({
            "day": datetime.fromtimestamp(item['dt']).strftime("%A"),
            "temp": item['main']['temp'],
            "icon": item['weather'][0]['icon'],
        })

    return render(request, "index.html", {"current": current_weather, "forecast": forecast_list, "units": units})