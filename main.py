from flask import Flask, render_template, request
from weather_api import get_weather

app = Flask(__name__)


API_KEY = "00cf445406c6ba37f0f4547fcbab4c3b"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city']
        try:
            weather_data = get_weather(city, API_KEY)
        except Exception as e:
            error = str(e)

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
