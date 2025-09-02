from flask import Flask, request, render_template
import numpy as np
import pickle

# Load model and scalers
model = pickle.load(open('mmmm.pkl', 'rb'))
ms = pickle.load(open('mmss.pkl', 'rb'))
sc = pickle.load(open('sssss.pkl', 'rb'))

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    N = float(request.form['Nitrogen'])
    P = float(request.form['Phosporus'])
    K = float(request.form['Potassium'])
    temp = float(request.form['Temperature'])
    humidity = float(request.form['Humidity'])
    ph = float(request.form['Ph'])
    rainfall = float(request.form['Rainfall'])

    features = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    scaled = ms.transform(features)
    final_features = sc.transform(scaled)
    prediction = model.predict(final_features)

    crop_dict = {
        1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
        8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
        14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
        19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
    }

    result = crop_dict.get(prediction[0], "Unable to determine the best crop.")
    return render_template('index.html', result=f"{result} is the best crop to be cultivated right there.")

if __name__ == "__main__":
    app.run(debug=True)
