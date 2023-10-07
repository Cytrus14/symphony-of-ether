from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/andromeda')
def about():
    return render_template('pomocniczy.html')

@app.route('/body')
def body():
    return render_template('pomocniczy.html')

if __name__ == '__main__':
    app.run(debug=True)
