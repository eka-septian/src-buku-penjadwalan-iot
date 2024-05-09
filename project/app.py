from flask import Flask,redirect, url_for,render_template
from piUtils import setLedState
import RPi.GPIO as io 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fungsi')
def pushbtn_state():
       return("Mantap")

@app.route('/led/<int:state>',methods=["POST"])
def setLed(state):
    if state == 0: 
        setLedState(False)
    elif state == 1:
        setLedState(True)
    else: 
        return ('Unknown state', 400)
    return 'LED state set successfully'

@app.route('/monitor')
def test():
          return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
