from flask import Flask, request
from flask_restx import Api, Resource, fields
import pandas as pd
import joblib
import os

app = Flask(__name__)
api = Api(app, version='1.0', title='Stress Prediction API', description='API to predict stress labels')

# Loading the trained models
nb_model = joblib.load('MultinomialNB_stress.pkl')
bb_model = joblib.load('BernoulliNB_stress.pkl')

# Swagger UI input model for POST request
text_input_model = api.model('Text_Input', {
    'text': fields.String(description='Text for stress prediction', example='I am feeling stressed')
})

# Swagger UI input model for GET request
file_input_model = api.model('File_Input', {
    'file': fields.String(description='CSV file containing texts for stress prediction with header "text"', 
                           example='file.csv')
})

# Swagger UI output model
text_output_model = api.model('Text_Output', {
    'label': fields.Integer(description='Predicted stress label (0 or 1)', example=1)
})

# Endpoint for POST request
@api.route('/predict_text')
class Text_Predict(Resource):
    @api.expect(text_input_model)
    @api.marshal_with(text_output_model)
    def post(self):
        text = request.json['text']
        label = nb_model.predict([text])[0]
        return {'label': int(label)}

# Endpoint for GET request
@api.route('/predict_file')
class File_Predict(Resource):
    @api.expect(file_input_model)
    def get(self):
        file_path = request.args.get('file')
        df = pd.read_csv(file_path)
        texts = df['text'].tolist()
        labels = nb_model.predict(texts)
        df['label'] = labels
        return df.to_dict()

if __name__ == '__main__':
    app.run(debug=True)
