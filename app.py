from flask import Flask, request, jsonify, send_file
from creditrisk import calculate_risk  # creditrisk.py-dakı funksiyanı çağırır

app = Flask(__name__)

@app.route('/')
def serve_front():
    return send_file('frontcredit.html')  # ön səhifəni göstərir

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    name = data.get('name')
    income = float(data.get('income'))
    debt = float(data.get('debt'))
    experience = float(data.get('experience'))

    result = calculate_risk(income, debt, experience)
    return jsonify({"name": name, "risk": result})

if __name__ == '__main__':
    app.run(debug=True)
