import collector
from flask import Flask
from flask import request
from collections import Counter
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}": {}'.format(letter, count))
    return '<br>'.join(response)

@app.route('/attemptSlcmLogin', methods=["GET","POST"])
def attemptSlcmLogin():
    if request.method == 'POST':
        col = collector.Collector(request.form['username'], request.form['password'])
        col.makeReq()
        return 'dOnEzO'
    
    if request.method == 'GET':
        col = collector.Collector('160905032', 'Eybitches')
        col.makeReq()
        return '<h1 style="text-align: center; font-family: consolas">WOKE</h1>'

@app.route('/test')
def test():
    dictToSend = {'username':'160905032', 'password':'Eybitches'}
    res = requests.post('http://localhost:5000/attemptSlcmLogin', json=dictToSend)
    print ('response from server:',res.text)
    return 'yay'

if __name__ == '__main__':
  app.run()
