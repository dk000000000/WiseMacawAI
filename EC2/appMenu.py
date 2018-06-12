from flask import Flask, request
from flask import jsonify


app = Flask(__name__)

#############
# Routing
#
@app.route('/put', methods=['POST'])
def reply():
    return jsonify( t.Handle_Session(request.get_json()) )
#############

# start app
if (__name__ == "__main__"):
    #_________________________________________________________________
    from WiseMacawMenu import WiseMacawMenu
    t = WiseMacawMenu()

    #_________________________________________________________________
    app.run(host='0.0.0.0',port = 8888)
