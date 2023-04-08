from flask import Flask, render_template
app = Flask(__name__)

@app.route('/index')
def index():
    name = 'nanami'
    return render_template('index.html', name=name)

@app.route('/sub')
def sub():
    return "This is Sub Page!"

if __name__ == "__main__":
    app.run()