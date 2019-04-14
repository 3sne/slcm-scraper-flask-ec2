import collector
from flask import Flask
from flask import request
from flask import render_template
from collections import Counter
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/go', methods=["GET","POST"])
def go():
    if request.method == 'POST':
        print(request.form)
        try:
            if request.form.get('username') == None or request.form.get('password') == None:
                return '{"error" : "missing parameter", "code" : "00"}'
            col = collector.Collector(request.form['username'], request.form['password'])
            col.makeReq()
            if col.errorDuringExtraction == True:
                return '{"error" : "server side error", "code" : "10"}'
            return '<h1 style="text-align: center; font-family: consolas">POST SUCCESSFUL</h1>'
        except:
            return '{"error" : "server side error" , "code" : "11"}'
    
    if request.method == 'GET':
        return render_template('slcmgo_get_response.html', bois_ip=request.remote_addr)

@app.route('/testGoPost')
def testSlcmGo():
    dictToSend = {'username':'160905032', 'password':'Eybitches'}
    res = requests.post('http://localhost:5000/go', data=dictToSend)
    return res.text

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
