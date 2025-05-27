from flask import Flask, render_template, request, flash
from markupsafe import Markup
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# Load model and encoders
model_dir = os.path.join(os.path.dirname(__file__), "model")

with open(os.path.join(model_dir, "heart_disease_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(model_dir, "heart_disease_scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

with open(os.path.join(model_dir, "label_encoders.pkl"), "rb") as f:
    label_encoders = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            sex = request.form["sex"]
            cp = request.form["cp"]
            rbp = int(request.form["rbp"])
            chol = int(request.form["chol"])
            fbs = int(request.form["fbs"])
            ecg = request.form["ecg"]
            maxhr = int(request.form["maxhr"])
            exang = request.form["exang"]
            oldpeak = float(request.form["oldpeak"])
            slope = request.form["slope"]

            data = [
                age,
                label_encoders["Sex"].transform([sex])[0],
                label_encoders["ChestPainType"].transform([cp])[0],
                rbp,
                chol,
                fbs,
                label_encoders["RestingECG"].transform([ecg])[0],
                maxhr,
                label_encoders["ExerciseAngina"].transform([exang])[0],
                oldpeak,
                label_encoders["ST_Slope"].transform([slope])[0]
            ]

            scaled_data = scaler.transform([data])
            prediction = model.predict(scaled_data)[0]

            result = (
                "✅ No Heart Disease Detected"
                if prediction == 0
                else "⚠️ High Risk of Heart Disease"
            )
            flash(Markup(result))
        except Exception as e:
            flash(Markup(f"Error: {str(e)}"))

    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
