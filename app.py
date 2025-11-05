import os
from flask import Flask, request, jsonify, send_file
from creditrisk import calculate_risk  # creditrisk.py-dakı funksiyanı çağırır

app = Flask(__name__)

@app.route('/')
def serve_front():
    return send_file('frontcredit.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        name = data.get('name')
        income = float(data.get('income'))
        debt = float(data.get('debt'))
        experience = float(data.get('experience'))
        result = calculate_risk(income, debt, experience)
        return jsonify({"name": name, "risk": result})
    except Exception as e:
        print("⚠️ Xəta baş verdi:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
