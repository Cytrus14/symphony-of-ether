from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, template_folder='templates')

coordinates = {'x': None, 'y': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/andromeda')
def andromeda():
    return render_template('andromeda.html')

@app.route('/bode')
def bode():
    return render_template('bode.html')

@app.route('/surfboard')
def surfboard():
    return render_template('surfboard.html')

@app.route('/angelfish')
def angelfish():
    return render_template('angelfish.html')

@app.route('/Casper_the_Friendly_Ghost_Nebular')
def Casper_the_Friendly_Ghost_Nebular():
    return render_template('Casper_the_Friendly_Ghost_Nebular.html')

@app.route('/Crab_Nebula')
def Crab_Nebula():
    return render_template('Crab_Nebula.html')

@app.route('/Owl_Nebula')
def Owl_Nebula():
    return render_template('Owl_Nebula.html')


@app.route('/Spider_Globular')
def Spider_Globular():
    return render_template('Spider_Globular.html')

@app.route('/sombrero')
def sombrero():
    return render_template('sombrero.html')

@app.route('/Phantom')
def Phantom():
    return render_template('Phantom.html')


@app.route('/NGC_5272')
def NGC_5272():
    return render_template('NGC_5272.html')


@app.route('/Dumbbell_Nebula')
def Dumbbell_Nebula():
    return render_template('Dumbbell_Nebula.html')

def get_video():
    video_path = 'static/final_output.mp4'  # Ścieżka do pliku wideo
    return Response(open(video_path, 'rb'), mimetype='video/mp4')

@app.route('/video/final_output.mp4')
def get_video(filename):
    return send_from_directory('static', "static/final_output.mp4")

@app.route('/send-coordinates', methods=['POST'])
def receive_coordinates():
    try:
        data = request.get_json()
        x = data['x']
        y = data['y']

        # Zapisz współrzędne w słowniku
        coordinates['x'] = x
        coordinates['y'] = y

        # Wypisz współrzędne na konsoli
        print(f'Odebrane współrzędne - X: {x}, Y: {y}')

        # Możesz tutaj wykonać operacje na otrzymanych współrzędnych, jeśli jest to potrzebne

        return jsonify({'message': 'Dane współrzędnych zostały zapisane pomyślnie'})
    except Exception as e:
        return jsonify({'error': 'Wystąpił błąd podczas przetwarzania danych'}), 400


if __name__ == '__main__':
    app.run(debug=True)
