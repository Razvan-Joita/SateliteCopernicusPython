from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/odata/v1/Products')
def get_products():

    data = {
        "value": [
            {
                "Name": "S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE"
            }
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
