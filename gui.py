import os
import sys
import requests
from user_settings import *
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
from pathlib import Path
from moviepy.editor import AudioFileClip, ImageClip
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from PIL import Image
from datetime import datetime
#TODO Youtube upload? dvd logo. include Unsplash accolades
#pyinstaller --onefile --windowed --target-arch arm64 gui.py


def unsplash_image():
    url = "https://api.unsplash.com/photos/random/?client_id=" + unsplash_client_id
    query = {'orientation':'landscape', 'topics':'Textures & Patterns', 'query': 'abstract'}
    response = requests.get(url, params=query)
    data = response.json()["urls"]["full"]
    color = response.json()["color"]
    citation = response.json()["user"]
    data_split_format = str(data).split("fm=")
    format = data_split_format[1].split('&')[0]
    response = requests.get(data)
    img = Image.open(BytesIO(response.content))
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    image_name = "unsplash_image_" + timestamp + "." + format
    img.save(image_name)
    return image_name, color


def contrast_color(r, g, b):
    d = 0
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if luminance > 0.5:
        d = 0
    else:
        d = 255
    return d


def draw_image_center(file, text, output_file, d):
    img = Image.open(file)
    fontsize = 1
    img_fraction = 0.7
    width, height = img.size
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('Arial Unicode.ttf', fontsize)
    while myFont.getsize(text)[0] < img_fraction * img.size[0]:
        fontsize += 5
        myFont = ImageFont.truetype('Arial Unicode.ttf', fontsize)
    t_width, t_height = draw.textsize(text, font=myFont)
    draw.text(((width-t_width)/2, (height-t_height)/2), text, font=myFont, fill=(d, d, d))
    img.save(output_file)
    return


def create_video(image_path, audio_path, output_video_path):
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(output_video_path)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Audio To Video"
        self.top = 100
        self.left = 100
        self.width = 1400
        self.height = 800
        self.InitUI()
        self.backgroundPicture = ""
        self.outputFolder = ""
        self.inputFolder = ""
        self.Unsplash = False

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.SelectInputFolder = QPushButton('Select Audio Folder', self)
        self.SelectInputFolder.resize(200, 32)
        self.SelectInputFolder.move(600, 190)
        self.SelectInputFolder.clicked.connect(self.select_input_folder)

        self.ifLabel = QLabel(self)
        self.ifLabel.setText("")
        self.ifLabel.setGeometry(850, 190, 400, 32)

        self.SelectOutputFolder = QPushButton('Select Output Folder', self)
        self.SelectOutputFolder.resize(200, 32)
        self.SelectOutputFolder.move(600, 400)
        self.SelectOutputFolder.clicked.connect(self.select_output_folder)

        self.ofLabel = QLabel(self)
        self.ofLabel.setText("")
        self.ofLabel.setGeometry(850, 400, 400, 32)

        self.SelectBackgroundPicture = QPushButton('Select Background Picture', self)
        self.SelectBackgroundPicture.resize(200, 32)
        self.SelectBackgroundPicture.move(600, 260)
        self.SelectBackgroundPicture.clicked.connect(self.select_background_picture_dialog)

        self.UnsplashLabel = QLabel("or", self)
        self.UnsplashLabel.setGeometry(690, 295, 20, 32)

        self.SelectUnsplashPicture = QPushButton("Use Random Abstract Photo", self)
        self.SelectUnsplashPicture.clicked.connect(self.unsplash_check)
        self.SelectUnsplashPicture.resize(200, 32)
        self.SelectUnsplashPicture.move(600, 330)

        self.UnsplashSelectLabel = QLabel(self)
        self.UnsplashSelectLabel.setText("")
        self.UnsplashSelectLabel.setGeometry(850, 330, 400, 32)

        self.bpLabel = QLabel(self)
        self.bpLabel.setText("")
        self.bpLabel.setGeometry(850, 260, 400, 32)

        self.GenerateVideos = QPushButton('Generate Videos', self)
        self.GenerateVideos.resize(200, 32)
        self.GenerateVideos.move(600, 470)
        self.GenerateVideos.clicked.connect(self.generate_videos)

        self.genLabel = QLabel(self)
        self.genLabel.setText("")
        self.genLabel.setGeometry(850, 470, 400, 32)

        self.show()

    def select_background_picture_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Background Picture")
        if fileName:
            self.backgroundPicture = fileName
            self.bpLabel.setText(fileName)
            self.UnsplashSelectLabel.setText("")
            self.Unsplash = False
        return fileName

    def unsplash_check(self):
        if self.Unsplash:
            self.Unsplash = False
            self.UnsplashSelectLabel.setText("")
        else:
            self.Unsplash = True
            self.UnsplashSelectLabel.setText("Uses a random photo from Unsplash.com.")
            self.bpLabel.setText("")
            self.backgroundPicture = ""
        return

    def select_input_folder(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Audio Folder')
        if folderPath:
            self.inputFolder = folderPath
            self.ifLabel.setText(folderPath)
        return folderPath

    def select_output_folder(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderPath:
            self.outputFolder = folderPath
            self.ofLabel.setText(folderPath)
        return folderPath

    def generate_videos(self):
        if self.outputFolder == "" or self.inputFolder == "" or (self.backgroundPicture == "" and not self.Unsplash):
            self.genLabel.setText("Please choose above options.")
        else:
            self.genLabel.setText("Processing.")
            audio_files_path = Path(self.inputFolder)
            audio_files_mp3 = list(audio_files_path.glob('*.mp3'))
            audio_files_wav = list(audio_files_path.glob('*.wav'))
            audio_files_m4a = list(audio_files_path.glob('*.m4a'))
            audio_files = audio_files_wav + audio_files_mp3 + audio_files_m4a
            for file in audio_files:
                file_name_base = os.path.basename(file).split('.')[0]
                full_file_path = os.path.abspath(file)
                if self.Unsplash:
                    image_name, color = unsplash_image()
                    extension = image_name.split('.')[1]
                    print(image_name)
                    rgb = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                    d_color = contrast_color(rgb[0], rgb[1], rgb[2])
                else:
                    image_name = self.backgroundPicture
                    extension = image_name.split('.')[1]
                    print(image_name)
                    im = Image.open(image_name)
                    rgb_im = im.convert('RGB')
                    r, g, b = rgb_im.getpixel((1, 1))
                    d_color = contrast_color(r, g, b)
                draw_image_center(image_name, file_name_base, "output_picture" + "." + extension, d_color)
                create_video("output_picture" + "." + extension, full_file_path, self.outputFolder + "/" + file_name_base + ".mp4")
            self.genLabel.setText("Videos Generated.")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
