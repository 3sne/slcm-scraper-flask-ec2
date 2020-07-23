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

@app.route('/go', methods=["GET"])
def go():
    resData = {}
    ext_uname = ''
    ext_pw = ''
    if request.method == 'GET':
        try:
            if request.args.get('username') and request.args.get('password'):
                ext_uname = request.args.get('username')
                ext_pw = request.args.get('password')
            else:
                return render_template('slcmgo_get_response.html', bois_ip=request.remote_addr)
        except:
            resData["code"] = "200"
            return jsonify(resData)

    col = collector.Collector(ext_uname, ext_pw)
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

@app.route('/testgomarks', methods=['GET'])
def testgomarks():
    resData = {}
    ext_uname = ''
    ext_pw = ''
    if request.method == 'GET':
        try:
            if request.args.get('username') and request.args.get('password'):
                ext_uname = request.args.get('username')
                ext_pw = request.args.get('password')
            else:
                return render_template('slcmgo_get_response.html', bois_ip=request.remote_addr)
        except:
            resData["code"] = "200"
            return jsonify(resData)

    col = collector.Collector(ext_uname, ext_pw)
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
    resData["data"] = col.marksData
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

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
