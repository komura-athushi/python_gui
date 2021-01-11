import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import constant

class MyImage():
    def __init__(self):
        self.item_id = -1
        self.image_position = None
        self.image_size = None
        self.tkimg = None
        self.file_name = None

    #画像の座標を取得
    def get_position(self,canvas):
        return canvas.coords(self.item_id)
    
    #画像を読み込む
    def load_image(self,canvas,file):
        #画像読み込み
        img = Image.open(file)
        #このImageTk?は保持しておかないといけないらしい
        self.tkimg = ImageTk.PhotoImage(img)
        self.item_id = canvas.create_image(constant.CANVAS_WIDTH/2 + constant.ADD_CANVAS_SIZE,
        constant.CANVAS_HEIGHT/2 + constant.ADD_CANVAS_SIZE,
        image=self.tkimg,
        tags='img')
        #画像のサイズを取得
        self.image_size = img.size
        #ファイルの名前を抽出していく、/と.を除いていく
        slash_number = file.rfind('/')
        number = file.rfind('.')
        if slash_number == -1:
            self.file_name = file[:number]
        else:
            self.file_name = file[slash_number + 1:number]
        print(self.file_name)


    