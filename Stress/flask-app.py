# 1. Import the dependencies
from flask import Flask, request
import pandas as pd
import numpy as np
import joblib
import os
import flasgger
from flasgger import Swagger, swag_from

# 2. Initialize the Flask app and Swagger UI
app = Flask(__name__)
swagger = Swagger(app)

# 3. Read the pickle file
bb_model = joblib.load('BernoulliNB_stress.pkl')

# 4. Endpoint for GET request
@app.route('/predict_text', methods=["GET"])
#@swag_from('text_predict.yml')
def predict_text():
    """
    Endpoint to predict stress labels from text input.
    ---
    parameters:
        - name: text
          in: query
          type: string
          required: true
          description: Text for stress prediction
          example: "I am feeling stressed"
    responses:
        200:
            description: Predicted stress label
            schema:
                type: object
                properties:
                    label:
                        type: integer
                        description: Predicted stress label (0 or 1)
                        example: 1
    """
    text = request.args.get('text')
    label = bb_model.predict([text])[0]
    return {'label': int(label)}

# 5. Endpoint for POST request
@app.route('/predict_file', methods=["POST"])
#@swag_from('file_predict.yml')
def predict_file():
    """
    Endpoint to predict stress labels from CSV file input.
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
          description: CSV file containing texts for stress prediction with header "text"
          example: file.csv
    responses:
        200:
            description: Predicted stress labels
            schema:
                type: object
                properties:
                    label:
                        type: integer
                        description: Predicted stress label (0 or 1)
                        example: 1
    """
    file = request.files.get('file')
    df = pd.read_csv(file)
    texts = df['text'].tolist()
    labels = bb_model.predict(texts)
    df['label'] = labels
    return df.to_dict()

if __name__ == '__main__':
    app.run(debug=True)

