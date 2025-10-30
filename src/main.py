from flask import Flask
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'bacaa3381e4c453088449ccd04f270cf'
CORS(app)

add = '127.0.0.1:5000'

# Define a parser for the incoming symptom data
symptom_parser = reqparse.RequestParser()
symptom_parser.add_argument('fever', type=int, required=True, help='Severity of fever (0-9)')
symptom_parser.add_argument('cough', type=int, required=True, help='Severity of cough (0-9)')
symptom_parser.add_argument('headache', type=int, required=True, help='Severity of headache (0-9)')
symptom_parser.add_argument('fatigue', type=int, required=True, help='Severity of fatigue (0-9)')
symptom_parser.add_argument('nausea', type=int, required=True, help='Severity of nausea (0-9)')
# For keys with spaces, specify the destination variable name
symptom_parser.add_argument('sore throat', type=int, required=True, help='Severity of sore throat (0-9)', dest='sore_throat')
symptom_parser.add_argument('runny nose', type=int, required=True, help='Severity of runny nose (0-9)', dest='runny_nose')

import pandas as pd

class Home(Resource):
    def post(self):
        # Parse the arguments from the request
        args = symptom_parser.parse_args()

        # Assign the values to a list in the correct order
        sym = [
            args['fever'],
            args['cough'],
            args['headache'],
            args['fatigue'],
            args['nausea'],
            args['sore_throat'],
            args['runny_nose']
        ]

        # Process the symptoms to find a match
        processor = DataProcessor()
        matched_diseases = processor.process_symptoms(sym)

        # Return the result
        if matched_diseases:
            return {'matched_diseases': matched_diseases}, 200
        else:
            return {'message': 'No matching disease found'}, 404

class DataProcessor:
    def process_symptoms(self, user_symptoms: list):
        try:
            df = pd.read_csv('src/database/disease_symptoms.csv')
        except FileNotFoundError:
            return ["Error: The disease database file was not found."]

        match_scores = {}

        # Iterate through each row in the DataFrame
        for _, row in df.iterrows():
            disease_name = row[0]  # First column contains disease name
            symptoms = row[1:].astype(float)  # Rest of the columns are symptoms
            score = 0
           
            # Compare each user symptom with the database symptom
            for i, db_symptom_severity in enumerate(symptoms):
                user_symptom_severity = user_symptoms[i]
                # Check if the user's symptom is within the tolerance range
                if (db_symptom_severity - 1) <= user_symptom_severity <= (db_symptom_severity + 1):
                    score += 1
            match_scores[disease_name] = score

        # Find the highest score
        if not match_scores:
            return []
       
        max_score = max(match_scores.values())

        # Find all diseases that have the highest score, only if the score is greater than 0
        if max_score > 0:
            best_matches = [disease for disease, score in match_scores.items() if score == max_score]
            return best_matches
        else:
            return []

api.add_resource(Home,'/ai/')

app.run(debug=True)
