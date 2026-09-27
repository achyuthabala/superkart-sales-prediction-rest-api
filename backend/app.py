
# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_final_model.pkl")


# ---------------------------------------------------------
# Home endpoint
# ---------------------------------------------------------

@superkart_sales_predictor_api.get('/')
def home():
    """
    Handles GET requests to the root URL.
    """
    return "Welcome to the SuperKart Sales Prediction API!"


# ---------------------------------------------------------
# Single prediction endpoint
# ---------------------------------------------------------

@superkart_sales_predictor_api.post('/v1/sales')
def predict_sales():
    """
    Handles single product-store sales prediction.

    Expects JSON containing the 10 model input features.
    """

    # Get JSON data from request
    product_store_data = request.get_json()

    # Extract the model features
    sample = {
        'Product_Weight': product_store_data['Product_Weight'],
        'Product_Sugar_Content': product_store_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_store_data['Product_Allocated_Area'],
        'Product_MRP': product_store_data['Product_MRP'],
        'Store_Size': product_store_data['Store_Size'],
        'Store_Location_City_Type': product_store_data['Store_Location_City_Type'],
        'Store_Type': product_store_data['Store_Type'],
        'Product_Id_char': product_store_data['Product_Id_char'],
        'Store_Age_Years': product_store_data['Store_Age_Years'],
        'Product_Type_Category': product_store_data['Product_Type_Category']
    }

    # Convert input into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert prediction to Python float and round
    predicted_sales = round(float(predicted_sales), 2)

    # Return prediction as JSON
    return jsonify({
        'Predicted Product Store Sales (in dollars)': predicted_sales
    })


# ---------------------------------------------------------
# Batch prediction endpoint
# ---------------------------------------------------------

@superkart_sales_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    Handles batch product-store sales prediction.

    Expects a CSV file containing the 10 model input features.
    """

    # Get uploaded CSV file
    file = request.files['file']

    # Read CSV into DataFrame
    input_data = pd.read_csv(file)

    # Make predictions
    predicted_sales = model.predict(input_data)

    # Convert predictions to Python floats and round
    predicted_sales = [
        round(float(sales), 2)
        for sales in predicted_sales
    ]

    # Create output dictionary using row numbers
    output_dict = {
        str(index + 1): sales
        for index, sales in enumerate(predicted_sales)
    }

    # Return predictions
    return jsonify(output_dict)


# ---------------------------------------------------------
# Run Flask application
# ---------------------------------------------------------

if __name__ == '__main__':
    superkart_sales_predictor_api.run(
        host='0.0.0.0',
        port=7860,
        debug=True
    )
