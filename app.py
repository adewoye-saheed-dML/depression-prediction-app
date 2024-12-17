from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  
import pickle

# Load the model and DictVectorizer
output_file = 'student.pkl'
with open(output_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)


# Function to validate input
def validate_input(student):
    required_features = ['age', 'academic_pressure', 'cgpa', 'study_satisfaction',
                         'sleep_duration', 'dietary_habits', 'degree',
                         'have_you_ever_had_suicidal_thoughts_?',
                         'work/study_hours', 'financial_stress']
    missing_features = [feature for feature in required_features if feature not in student]
    return missing_features

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    student = request.get_json()
    print("Received input:", student)  # Debug incoming data

    # Validate input
    missing_features = validate_input(student)
    if missing_features:
        print(f"Missing features: {missing_features}")  # Debug validation
        return jsonify({'error': f'Missing features: {missing_features}'}), 400

    try:
        # Transform and predict
        X = dv.transform([student])
        print("Transformed input:", X)  # Debug transformation

        y_pred = model.predict_proba(X)[:, 1]
        depression = y_pred >= 0.5
        print("Prediction output:", y_pred)  # Debug prediction result

        result = {
            'depression_probability': float(y_pred[0]),
            'depression': bool(depression[0])
        }
        print("Final result:", result)
        return jsonify(result)

    except Exception as e:
        print("Error during prediction:", e)  # Debug errors
        return jsonify({'error': 'An error occurred during prediction'}), 500
