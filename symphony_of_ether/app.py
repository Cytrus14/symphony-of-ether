from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('base.html')
@app.route('/video')
def video():
    video_files = ['video1.mp4']
    return render_template('video.html',video_files=video_files)

if __name__ == '__main__':
    app.run(debug=True)
