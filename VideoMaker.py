import os
import cv2 as cv
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip

class VideoMaker:
    def __init__(self, images_path=os.path.join('symphony_of_ether', 'temp_files', 'temp_images'),
            audio_path=None, fps=10):
        self.audio_path = audio_path
        self.images_path = images_path
        self.fps = fps
        self.frame_size = None
        self.output_video_temp = os.path.join('symphony_of_ether', 'temp_files', 'temp_video', 'temp.mp4')

    def gen_video(self, visualization_type='combined'):
        img_count = len(os.listdir(os.path.join(self.images_path, visualization_type)))
        img_paths = []
        for i in range(img_count):
            img_path = os.path.join(self.images_path, visualization_type, str(i) + '.png')
            img_paths.append(img_path)

        height, width, _ = cv.imread(img_paths[0]).shape
        frame_size = (width, height)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(self.output_video_temp, fourcc, self.fps, frame_size)

        for image_path in img_paths:
            frame = cv.imread(image_path)
            out.write(frame)
        out.release()

        video_clip = VideoFileClip(self.output_video_temp)
        if self.audio_path != None:
            audio_clip = AudioFileClip(self.audio_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(os.path.join('symphony_of_ether', 'temp_files', 'temp_video', 'output-' + visualization_type +'.mp4')
                ,codec='libx264', audio_codec='aac')

# temp = VideoMaker(fps=10, audio_path='symphony_of_ether/temp_files/temp_video/untitled.wav')
# temp.gen_video(visualization_type='combined')
