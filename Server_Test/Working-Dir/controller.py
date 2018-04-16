from flask import Flask, request
from flask.templating import render_template

app=Flask(__name__)

'''
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index', methods=['POST'])
def index():
    return render_template('index.html')

@app.route('/completaProfilo', methods=['POST'])
def completaProfilo():
    return render_template('completaProfilo.html')
'''

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    	app.run(host='0.0.0.0', port=8000)
