import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

from lib import utils

# Initialize Flask app
app = Flask(__name__)

cred = credentials.Certificate('credentials/plant-pot-41e34-firebase-adminsdk-ps1tl-b6e84a4352.json')
default_app = initialize_app(cred)
db = firestore.client()
pots_collection = db.collection('pots')

@app.route('/add', methods=['POST'])
def create():
    try:
        id = request.json['id']
        data = utils.create_new_pot_schema(id)
        pots_collection.document(id).set(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    try:
        id = request.json['id']
        param_name = request.json['parameter']
        param_value = request.json['value']
        data = utils.update_parameter_schema(param_name,param_value)
        pots_collection.document(id).update(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

# @app.route('/list', methods=['GET'])
# def read():
#     try:
#         # Check if ID was passed to URL query
#         pot_id = request.args.get('id')
#         if pot_id:
#             pot = pots_collection.document(pot_id).get()
#             return jsonify(pot.to_dict()), 200
#         else:
#             all_pots = [doc.to_dict() for doc in pots_collection.stream()]
#             return jsonify(all_pots), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8080))
print(port)
if __name__ == '__main__':
    # app.run(threaded=True, host='0.0.0.0', port=port)
    app.run(debug=True)
