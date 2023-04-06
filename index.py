import sys
from flask import Flask
app = Flask(__name__)

def sum(x, y):
  return x+y

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/sub')
def sub():
    return "This is Sub Page!"

if __name__ == "__main__":
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
    result = sum(num1, num2)
    print(result)

    app.run()