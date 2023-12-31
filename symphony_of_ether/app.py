from flask import Flask, render_template, request, jsonify, send_from_directory, Response, redirect, url_for
from SectionAudioConverterv1 import SectionAudioConverter
from VideoMaker import VideoMaker

app = Flask(__name__, template_folder='templates')

coordinates = {'x': 0, 'y': 0}


@app.route('/video_generate', methods=['GET'])
def videomaker():
        # Pobierz wartość imageName z formularza
        #imageName = request.form.get('imageName')
    #
    #Tworzenie obiektu SectionAudioConverter z imageName
    #     # (Skorzystaj z poprawnej nazwy klucza 'x' i 'y' w słowniku coordinates)
    object_name = request.args.get('object_name')
    obj1 = SectionAudioConverter(x=int(coordinates['x']/4), y=int(coordinates['y']/4),z=4,
                                 scale_down_factor=4, imageName=object_name)
    obj1.SynthConvert()
    #
    #     # Reszta kodu
    obj2 = VideoMaker(fps=10)
    obj2.audio_path = "Sounds/ImageMusic.wav"
    #obj2.gen_video("combined")
    obj2.gen_video("grid")
    return redirect('http://127.0.0.1:5000/static/temp_video/output_grid.mp4')

@app.route('/video_combined', methods=['GET'])
def videomaker_combined():
        # Pobierz wartość imageName z formularza
        #imageName = request.form.get('imageName')
    #
    #Tworzenie obiektu SectionAudioConverter z imageName
    #     # (Skorzystaj z poprawnej nazwy klucza 'x' i 'y' w słowniku coordinates)
    object_name = request.args.get('object_name')
    obj1 = SectionAudioConverter(x=int(coordinates['x']/4), y=int(coordinates['y']/4),z=4,
                                 scale_down_factor=4, imageName=object_name)
    obj1.SynthConvert()
    #
    #     # Reszta kodu
    obj2 = VideoMaker(fps=10)
    obj2.audio_path = "Sounds/ImageMusic.wav"
    obj2.gen_video("combined")
    #obj2.gen_video("grid")
    return redirect('http://127.0.0.1:5000/static/temp_video/output_combined.mp4')


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

@app.route('/temp_video')
def video():
    video_files = ['output_combined.mp4']
    return render_template('videoplayer.html',video_files=video_files)

@app.route('/video/final_output.mp4')
def get_video():
    return send_from_directory('static', "temp_video/output_combined.mp4")


@app.route('/send-coordinates', methods=['POST'])
def receive_coordinates():
    try:
        data = request.get_json()
        x = data['y']
        y = data['x']

        # Zapisz współrzędne w słowniku
        global  coordinates
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
