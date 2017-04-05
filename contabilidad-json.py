from flask import Flask, jsonify, request
from flask_cors import CORS
import zeep
from zeep.helpers import serialize_object
from zeep.plugins import HistoryPlugin


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return jsonify({'endpoint': '/contabilidad/<accion>'})


@app.route('/contabilidad/<action>', methods=['GET', 'POST'])
def send_action(action):
    if request.method == 'GET':
        history = HistoryPlugin()
        client = zeep.Client('https://contabilidad.ngrok.io/Contabilidad/Contabilidad?wsdl', plugins=[history])
        try:
            oper = client.service[action]
            return jsonify(serialize_object(oper()))
        except AttributeError as err:
            return jsonify({'error': f"No existe la accion {action}"})
        except:
            return jsonify({'error': 'Hubo un error haciendo su request.'})
    elif request.method == 'POST':
        history = HistoryPlugin()
        client = zeep.Client('https://contabilidad.ngrok.io/Contabilidad/Contabilidad?wsdl', plugins=[history])
        try:
            oper = client.service[action]
            return jsonify(serialize_object(oper(request.json())))
        except AttributeError as err:
            return jsonify({'error': f"No existe la accion {action}"})
        except:
            return jsonify({'error': "Hubo un error haciendo su request."})

if __name__ == '__main__':
    app.run()
