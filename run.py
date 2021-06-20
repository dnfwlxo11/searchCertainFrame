from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/api/startAnalyze', methods=['POST', 'GET'])
def getSimilarPart():
    return 'asd'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)