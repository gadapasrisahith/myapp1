import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def get_demand_prediction(product_name):
    """
    Trains a real AI model on the sales_data.csv and predicts
    the demand for the given product for next week.
    """
    
    try:
        # 1. Load the data
        df = pd.read_csv("sales_data.csv")
    except FileNotFoundError:
        return "Error: sales_data.csv not found."
    
    # 2. Filter data for *only* the product we want
    df_product = df[df['Product'] == product_name].copy()
    
    if df_product.empty:
        return "Error: No data for this product."
        
    # --- Feature Engineering (The "AI" part) ---
    # Convert 'Date' string into a real date object
    df_product['Date'] = pd.to_datetime(df_product['Date'])
    
    # Create "learning" features from the date
    # This is what the AI learns from
    df_product['month'] = df_product['Date'].dt.month
    df_product['day_of_week'] = df_product['Date'].dt.dayofweek
    df_product['day_of_year'] = df_product['Date'].dt.dayofyear
    
    # 3. Prepare data for the model
    # X = The "questions" (the date features)
    X = df_product[['month', 'day_of_week', 'day_of_year']]
    
    # y = The "answer" (what we want to guess)
    y = df_product['Quantity_Sold']
    
    # 4. Create and Train the AI model
    # We use a powerful model called RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 5. Create the "question" for *next week*
    # We will predict for 7 days from the last data point
    last_date = df_product['Date'].max()
    future_date = last_date + timedelta(days=7)
    
    # Create the same features for the future date
    future_month = future_date.month
    future_day_of_week = future_date.dayofweek
    future_day_of_year = future_date.dayofyear
    
    # 6. Make the prediction
    # Put the future features into the same shape as the model was trained on
    prediction = model.predict([[future_month, future_day_of_week, future_day_of_year]])
    
    # Return the prediction, rounded to a whole number
    return round(prediction[0])

# --- This is just to test if the file works ---
if __name__ == "__main__":
    # This test code ONLY runs when you run "ai_model.py" directly
    print("--- Testing the REAL AI Model ---")
    
    product = "Apples"
    prediction = get_demand_prediction(product)
    
    print(f"Test: Predict sales for {product}.")
    print(f"AI Prediction for next week: {prediction} units")