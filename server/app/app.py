from flask import Flask
from flask import render_template
from jinja2 import Environment, FileSystemLoader
import read_test_data


app = Flask(__name__)

@app.route("/")
def main_page():
    i = 0;
    sections = read_test_data.create_section_data()
    return render_template("main.html", sections=sections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

