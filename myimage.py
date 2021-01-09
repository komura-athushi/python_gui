import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class MyImage():
    def __init__(self):
        self.item_id = -1
        self.image_position = None
        self.image_size = None
        self.tkimg = None

    def load_image(self,canvas,file):
        #画像読み込み
        img = Image.open(file)
        #このImageTk?は保持しておかないといけないらしい
        self.tkimg = ImageTk.PhotoImage(img)
        self.item_id = canvas.create_image(100, 100, image=self.tkimg, tags='img')
        #画像のサイズを取得
        self.image_size = img.size
        a = 0

    