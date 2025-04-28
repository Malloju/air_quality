from flask import Flask, render_template, request
from demo import compute_air_quality  # import the function

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    pm25 = float(request.form['pm25'])
    pm10 = float(request.form['pm10'])
    no2 = float(request.form['no2'])
    co = float(request.form['co'])

    score, status = compute_air_quality(pm25, pm10, no2, co)

    return render_template('index.html', score=round(score, 2), status=status)

if __name__ == '__main__':
    app.run(debug=True)
