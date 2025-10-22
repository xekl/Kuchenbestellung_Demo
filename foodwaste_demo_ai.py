
import numpy as np
import pandas as pd

from foodwaste_demo_strings import * 

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb

# Global variables to store trained models and helpers
weather_encoder = LabelEncoder()
daytype_encoder = LabelEncoder()
knn_model = None
xgb_model = None

# data has columns = ["date", "dayofweek", "order", "sales", "leftover", "missed", "weather", "temperature", "daytype", "unexpected"]
# tomorrow has key/value pairs = {
#     "date": tomorrow_date, 
#     "dayofweek": tomorrow_date.strftime("%A"), 
#     "order": np.nan, 
#     "sales": tomorrow_sales, 
#     "leftover": np.nan, 
#     "missed": np.nan, 
#     "weather": tomorrow_weather, 
#     "temperature": tomorrow_temperature, 
#     "daytype": tomorrow_holiday,
#     "unexpected": unexpected
# }

# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

def preprocess_data(data):
    """
    Convert categorical features into numerical representations.
    """
    # Encode weather and daytype as categorical numerical values
    data["weather_num"] = weather_encoder.fit_transform(data["weather"])
    data["daytype_num"] = daytype_encoder.fit_transform(data["daytype"])
    
    # Convert dayofweek to a cyclic feature (sin transformation)
    data["dayofweek_num"] = pd.to_datetime(data["date"]).dt.weekday
    data["dayofweek_sin"] = np.sin(2 * np.pi * data["dayofweek_num"] / 7)
    
    return data

# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

def get_heuristic_prediction(data, tomorrow, language, k=4):
    """
    Predict tomorrow's sales using a simple heuristic: 
    Average sales of the last k occurrences of the same weekday.
    Args:
        data (pd.DataFrame): Historical sales data with required columns.
        tomorrow (dict): Dictionary containing tomorrow's details.
        language (str): language for outputs
        k (int): Number of past occurrences to consider for averaging.
    Returns:
        Prediction sales estimate and explanation dict
    """

    # Filter data for the same weekday as tomorrow
    tomorrow_dayofweek = get_localized_string(tomorrow["dayofweek"], "Deutsch") # data entries default to german daysofweek
    weekday_data = data[data["dayofweek"] == tomorrow_dayofweek]
    
    # Take the last k same weekdays
    reference_days = weekday_data.sort_values(by="date").tail(k)
    
    # Compute the heuristic sales prediction
    predicted_sales = reference_days["sales"].mean()

    # Build explanation 
    prediction_explanation = {
        "model_info": "modelInfoHeuristic",
        "reference_days": reference_days.to_dict(orient="records")
    }
    
    # Return results
    return predicted_sales, prediction_explanation

# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

def train_knn_model(data, k=4):
    """
    Train and store a KNN regressor model using historical sales data.
    """
    global knn_model
    
    data = preprocess_data(data.copy())
    features = ["dayofweek_num", "dayofweek_sin", "weather_num", "temperature", "daytype_num"]
    X = data[features]
    y = data["sales"]
    
    knn_model = KNeighborsRegressor(n_neighbors=k)
    knn_model.fit(X, y)

def get_knn_prediction(data, tomorrow, language, k=4):
    """
    Predict tomorrow's sales using a KNN regressor.
    
    Args:
        data (pd.DataFrame): Historical sales data.
        tomorrow (dict): Dictionary containing tomorrow's details.
        language (str): Language for outputs.
        k (int): Number of neighbors for KNN.
    
    Returns:
        Prediction sales estimate and explanation dict.
    """
    global knn_model
    
    # Ensure the model is trained
    if knn_model is None:
        train_knn_model(data, k)
    
    # Prepare input data for prediction
    tomorrow_processed = {
        "dayofweek_num": pd.to_datetime(tomorrow["date"]).weekday(),
        "dayofweek_sin": np.sin(2 * np.pi * pd.to_datetime(tomorrow["date"]).weekday() / 7),
        "weather_num": weather_encoder.transform([tomorrow["weather"]])[0],
        "temperature": tomorrow["temperature"],
        "daytype_num": daytype_encoder.transform([tomorrow["daytype"]])[0]
    }
    X_tomorrow = pd.DataFrame([tomorrow_processed])
    
    # Predict sales
    predicted_sales = knn_model.predict(X_tomorrow)[0]

    # Retrieve reference days = the k nearest neighbors
    neighbors_indices = knn_model.kneighbors(X_tomorrow, return_distance=False)[0]
    print("neighbors_indices", neighbors_indices)
    print("len(data)", len(data))
    reference_days = data.iloc[neighbors_indices]

    # Build explanation
    prediction_explanation = {
        "model_info": "modelInfoKNN",
        "reference_days": reference_days.to_dict(orient="records")
    }
    
    return predicted_sales, prediction_explanation

# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

def train_xgb_model(data):
    """
    Train and store an XGBoost model using historical sales data.
    """
    global xgb_model
    
    data = preprocess_data(data)
    features = ["dayofweek_num", "dayofweek_sin", "weather_num", "temperature", "daytype_num"]
    X = data[features]
    y = data["sales"]
    
    xgb_model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
    xgb_model.fit(X, y)

def get_xgb_prediction(data, tomorrow, language):
    """
    Predict tomorrow's sales using an XGBoost model.
    
    Args:
        data (pd.DataFrame): Historical sales data.
        tomorrow (dict): Dictionary containing tomorrow's details.
        language (str): Language for outputs.
    
    Returns:
        Prediction sales estimate and explanation dict.
    """
    global xgb_model
    
    # Ensure the model is trained
    if xgb_model is None:
        train_xgb_model(data)
    
    # Prepare input data for prediction
    tomorrow_processed = {
        "dayofweek_num": pd.to_datetime(tomorrow["date"]).weekday(),
        "dayofweek_sin": np.sin(2 * np.pi * pd.to_datetime(tomorrow["date"]).weekday() / 7),
        "weather_num": weather_encoder.transform([tomorrow["weather"]])[0],
        "temperature": tomorrow["temperature"],
        "daytype_num": daytype_encoder.transform([tomorrow["daytype"]])[0]
    }
    X_tomorrow = pd.DataFrame([tomorrow_processed])
    
    # Predict sales
    predicted_sales = xgb_model.predict(X_tomorrow)[0]
    
    # Build explanation
    prediction_explanation = {
        "model_info": "modelInfoXGB",
    }
    
    return predicted_sales, prediction_explanation

# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

def predict_tomorrow_sales_with(data, tomorrow, model, language):
    """Returns a dummy prediction based on the selected model."""
    if model == get_localized_string("modelHeu", language):
        return get_heuristic_prediction(data, tomorrow, language) # returns prediction and reference days
    elif model == get_localized_string("modelKNN", language):
        return get_knn_prediction(data, tomorrow, language) # returns prediction and reference days
    elif model == get_localized_string("modelXGB", language):
        return get_xgb_prediction(data, tomorrow, language) # returns prediction only
    else:
        return 0 # dummy
