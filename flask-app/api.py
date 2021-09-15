from flask import Flask,url_for, jsonify, request
from flask.wrappers import Response
from joblib import dump, load
from flask_cors import CORS, cross_origin





app = Flask(__name__)


# CORS(app)
app.ml_model = load('diamond_predictor.joblib') 



@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"
#print(url_for(welcome))


@app.route('/diamonds_api/', methods=['GET', 'POST'])
@cross_origin()
def hello():
    query_params = request.args
    # ([('color', '3'), ('clarity', '5'), ('cut', '1'), ('carat', '10'), ('x', '5'), ('y', '5'), ('z', '5')])

    
    color = int(query_params.get('color'))
    clarity = int(query_params.get('clarity'))
    cut = int(query_params.get('cut'))
    carat = float(query_params.get('carat'))
    x = float(query_params.get('x'))
    y = float(query_params.get('y'))
    z = float(query_params.get('z'))
    table = float(query_params.get('table'))
    depth_percent = 2 * z/(x+y)
    input_params = [[carat,cut,color, clarity, depth_percent, table, x, y, z ]]
    output = app.ml_model.predict(input_params)
    print(output) 
    return jsonify({'price':str(output[0]),
                    **query_params.to_dict()})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)