from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# Przechowuje współrzędne
coordinates = {'x': None, 'y': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('base.html')

@app.route('/video')
def video():
    video_files = ['video1.mp4']
    return render_template('video.html', video_files=video_files)

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
