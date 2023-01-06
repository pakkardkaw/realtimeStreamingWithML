
from flask import Flask,jsonify,request
from datetime import datetime
import pickle
import os
my_port = int(os.environ.get("PORT", 8030))
app = Flask(__name__)
# Load the model
#model = pickle.load(open('model.pkl','rb'))


@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json(force=True)
    #prediction = model.predict([[np.array(data['inputdata'])]])
    #output = prediction[0]
    return jsonify(message=data['inputdata']*544.53+5.02)
    #return jsonify(output)
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=my_port)