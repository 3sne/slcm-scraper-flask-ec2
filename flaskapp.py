import collector
import admintools
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from collections import Counter
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello Child'

@app.route('/go', methods=["GET","POST"])
def go():
    resData = {}
    if request.method == 'POST':
        print(request.form)
        try:
            if request.form.get('username') == None or request.form.get('password') == None:
                return '{"error" : "missing parameter", "code" : "00"}'
            if request.form.get('api_call') != 'True':
                return '{"error" : "missing parameter", "code" : "01"}'
            col = collector.Collector(request.form['username'], request.form['password'])
            col.makeReq()
            if col.errorDuringExtraction == True:
                return '{"error" : "server side error", "code" : "10"}'
            return '<h1 style="text-align: center; font-family: consolas">POST SUCCESSFUL</h1>'
        except:
            return '{"error" : "server side error" , "code" : "11"}'
    
    if request.method == 'GET':
        try:
            if request.args.get('username') and request.args.get('password'):
                col = collector.Collector(request.args['username'], request.args['password'])
                col.makeReq()
                if col.loginError:
                    resData["code"] = "100"
                    return jsonify(resData)
                if col.collectionError:
                    resData["code"] = "101"
                    return jsonify(resData)
                if col.errorDuringExtraction:
                    resData["code"] = "102"
                    return jsonify(resData)
                resData["code"] = "666"
                resData["data"] = col.attendanceData
                return jsonify(resData)
            else:
                return render_template('slcmgo_get_response.html', bois_ip=request.remote_addr)
        except:
            resData["code"] = "200"
            return jsonify(resData)

@app.route('/adminFetch', methods=["GET"])
def adminFetch():
    if request.method == 'GET':
        try:
            if request.args.get('jvsz') == None or request.args.get('pl') == None:
                return '{"error" : "adminFetch arg if error" , "code" : "-11"}'
            else:
                if request.args.get('jvsz') == 'zqmpxwno' and request.args.get('pl') == 'get':
                    dpu = admintools.DataPrepUtil('html', auto=1)
                    theStuff = {
                        "data": dpu.passList,
                        "code" : "666"
                    }
                    return jsonify(theStuff)
                else:
                    return '{"error" : "adminFetch arg if error" , "code" : "-111"}'
        except:
            return '{"error" : "adminFetch main if error" , "code" : "-1"}'

@app.route('/testGoPost')
def testSlcmGo():
    dictToSend = {'username':'160905032', 'password':'Eybitches', 'api_call':'True'}
    res = requests.post('http://localhost:5000/go', data=dictToSend)
    return res.text

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
