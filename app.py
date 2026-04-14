
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/user/<Oleg>')
def user(Oleg):
    return f'Hello, {Oleg}!'

if __name__ == '__main__':
    app.run(debug=True)

