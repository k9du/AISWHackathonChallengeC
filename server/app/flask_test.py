from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_mom():
    return "<p> Hello there! </p>"

@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
