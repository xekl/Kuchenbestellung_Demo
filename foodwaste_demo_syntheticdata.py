
from datetime import datetime, timedelta
import holidays

import numpy as np
import pandas as pd

from foodwaste_demo_strings import * 


def get_holiday(date):
    """Given a date, returns its holiday name, a before/after info or 'normal' for non-holidays.
    Only checks for German/Berlin holidays for now.
    :param date: The date to check for holidays.
    :return: type of day: 'normal' or '(day before/after) holiday name'
    """
    state_holidays = holidays.country_holidays(country="DE", subdiv="BE", years=date.year)
    date_type = state_holidays.get(date, "normal")
    if date_type == "normal": # for normal days, check if previous/next day is holiday
        if state_holidays.get(date - timedelta(days=1)):
            date_type = "day after " + state_holidays.get(date - timedelta(days=1))
        elif state_holidays.get(date + timedelta(days=1)):
            date_type = "day before " + state_holidays.get(date + timedelta(days=1))
    return date_type

def get_weather(date, history):
    """Given a date and some history, derives realistic-ish weather conditions for that day.
    :param date: The date for which to get weather info.
    :param history: All history before the date, in a pd.DataFrame with at leat columns: date, temperature, weather.
    :return: temperature, weather as int, string (of an icon)
    """

    # Define weather conditions and probabilities
    weather_conditions = ["☀️", "🌧️", "❄️", "🌤️"]  # Sunny, Rainy, Snowy, Partly Cloudy
    month = date.month
    
    # Compute seasonal baseline temperature
    base_temperature = int(10 + 10 * np.sin((month - 3) * 2 * np.pi / 12))
    
    # If history is available, adjust based on previous day
    if not history.empty:
        
        prev_day = history.iloc[-1]
        prev_temp = prev_day.temperature
        prev_weather = prev_day.weather
        
        # Ensure temperature change is gradual
        temp_variation = np.random.randint(-5, 6)  # Normally varies between -5 to 5 degrees
        temperature = prev_temp + temp_variation
        temperature = max(min(temperature, base_temperature + 10), base_temperature - 10)  # Bound temperature
        
        # Weather should have some persistence
        if prev_weather == "❄️":
            weather_probs = [0.1, 0.1, 0.4, 0.4]  # Higher chance of continuing snow
        elif prev_weather == "🌧️":
            weather_probs = [0.2, 0.4, 0.1, 0.3]  # Rain persists often
        else:
            weather_probs = [0.5, 0.2, 0.1, 0.2]  # Default probabilities

        # Ensure no snow in warm months (May - September)
        if month in [5, 6, 7, 8, 9] and temperature > 2:
            weather_probs[2] = 0  # Set snow probability to 0
            total_prob = sum(weather_probs)
            weather_probs = [p / total_prob for p in weather_probs]  # Normalize probabilities
        
        weather = np.random.choice(weather_conditions, p=weather_probs)
        
    else:

        # If no history, use default logic
        temperature = base_temperature + np.random.randint(-5, 5)
        weather = np.random.choice(weather_conditions, p=[0.6, 0.2, 0.1, 0.1])
    
    return temperature, weather

def get_sales(date, history, temperature, weather, is_holiday, language):
    """Given a date and some history, derives realistic-ish sales for that day.
    :param date: The date for which to get sales.
    :param history: All history before the date, in a pd.DataFrame with at leat columns: date, sales, temperature, weather.
    :param temperature: Temperature for date.
    :param weather: Weather for date.
    :param is_holiday: Type of the day: 'normal' or '(day before/after) holiday name'.
    :return: sales as int (amount of cakes)
    """

    avg_sales = 500  # Base average sales
    day_of_week = date.strftime("%A")
    
    # Base sales pattern: 50% higher on weekends
    base_sales = avg_sales * (1.5 if day_of_week in ["Saturday", "Sunday"] else 1.0)
    
    # Historical weather trend adjustments
    recent_weather = history.tail(7)["weather"] if len(history) >= 7 else history["weather"]
    recent_temp = history.tail(7)["temperature"] if len(history) >= 7 else history["temperature"]
    
    avg_recent_temp = recent_temp.mean() if not recent_temp.empty else temperature
    
    # Weather impact heuristics
    if weather == "❄️":  # Snow
        base_sales *= 0.7 if avg_recent_temp > -2 else 0.8
    elif weather == "🌧️":  # Rain
        if recent_weather.tolist().count("🌧️") > 3:
            base_sales *= 0.95  # People adapt after multiple rainy days
        else:
            base_sales *= 0.85  # Initial drop
    elif weather == "☀️":  # Sun
        if temperature > avg_recent_temp + 5:
            base_sales *= 0.9  # Too hot, people feel sluggish
        else:
            base_sales *= 1.1  # Pleasant sunshine boosts sales

    # Holiday impact heuristics
    if "before" in is_holiday:
        base_sales *= 1.2  # Slightly higher sales before holidays
        if "New Year's Day" in is_holiday:
            base_sales *= 3.0  # Extremely high sales before New Year's Day
    elif "after" in is_holiday:
        base_sales *= 1.1  # Slightly higher sales after holidays
    elif is_holiday != "normal":
        return 0, ""  # No sales on holidays
    
    # Random unforeseen event 
    event = ""
    unforeseen_events = [ 
        (get_localized_string("unexpEventConstruction", language), 0.85),
        (get_localized_string("unexpEventDemo", language), 1.2),
        (get_localized_string("unexpEventFlea", language), 1.3),
        (get_localized_string("unexpEventOffer", language), 0.8),
        (get_localized_string("unexpEventStrike", language), 0.7),
        (get_localized_string("unexpEventSportsGood", language), 1.15),
        (get_localized_string("unexpEventSportsBad", language), 0.75),
        (get_localized_string("unexpEventBirthday", language), 1.15),
    ]
    
    if np.random.rand() < 0.03: # 3% chance for unexpected events
        event, event_modifier = unforeseen_events[np.random.randint(len(unforeseen_events))]
        base_sales *= event_modifier
    
    # Final sales with some variance
    sales = int(base_sales * np.random.uniform(0.95, 1.05))
    
    return sales, event

def generate_synthetic_data(start_date, end_date, language):
    """Generates a synthetic dataset of cake orders and sales over a given time period.
    :param start_date: The start date of the dataset.
    :param end_date: The end date of the dataset.
    :return: A pandas DataFrame with synthetic data.
    """

    np.random.seed(42)
    
    # Prepare to store data
    columns = ["date", "dayofweek", "order", "sales", "leftover", "missed", "weather", "temperature", "daytype", "unexpected"]
    data = []
    
    # Generate data for each day
    current_date = start_date
    while current_date <= end_date:
        
        # Check if/which holiday
        day_of_week = get_localized_string(current_date.strftime("%A"), language)
        is_holiday = get_holiday(current_date)
        
        # Simulate weather and temperature with seasonality
        temperature, weather = get_weather(current_date, pd.DataFrame(data, columns=columns))

        # Get seasonal + influenced sales
        sales, unexpected = get_sales(current_date, pd.DataFrame(data, columns=columns), temperature, weather, is_holiday, language)
        
        # Generate order quantities based on previous sales (introduce some randomness)
        # to start, always order last week's sales
        order = data[-7][3] if len(data) > 7 else sales + np.random.randint(-3, 3)
        
        # Calculate leftover and missed sales
        leftover = max(order - sales, 0)
        missed = max(sales - order, 0)

        # Append row to data list
        data.append([
            current_date, day_of_week, order, sales, leftover, missed, weather, temperature, is_holiday, unexpected
        ])
        
        # Move to next day
        current_date += timedelta(days=1)

    # Create and return DataFrame    
    return pd.DataFrame(data, columns=columns)

def generate_tomorrow(data_history, language):
    tomorrow_date = data_history["date"].iloc[-1] + timedelta(days=1)
    tomorrow_temperature, tomorrow_weather = get_weather(tomorrow_date, data_history)
    tomorrow_holiday = get_holiday(tomorrow_date)
    tomorrow_sales, unexpected = get_sales(tomorrow_date, data_history, tomorrow_temperature, tomorrow_weather, tomorrow_holiday, language)
    return {
        "date": tomorrow_date, 
        "dayofweek": get_localized_string(tomorrow_date.strftime("%A"), language), 
        "order": np.nan, 
        "sales": tomorrow_sales, 
        "leftover": np.nan, 
        "missed": np.nan, 
        "weather": tomorrow_weather, 
        "temperature": tomorrow_temperature, 
        "daytype": tomorrow_holiday,
        "unexpected": unexpected
    }
