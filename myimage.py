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
        self.name = None
        self.scale= [1,1]

    #自身の情報を相手にコピーする
    def copy_image_infromation(self,canvas,opp):
        opp.name = self.name
        position=self.get_position(canvas)
        opp.set_position(canvas,position[0],position[1])
        opp.scale=self.scale


    #画像の座標を取得
    #戻り値はキャンバス内の座標
    def get_position(self,canvas):
        return canvas.coords(self.item_id)
    
    #画像を特定の座標に移動させる
    #引数はキャンバス内の座標
    def set_position(self,canvas,position_x,position_y):
        canvas.coords(self.item_id,position_x,position_y)

    #画像を読み込む
    def load_image(self,canvas,file):
        self.file_name = file
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
            self.name = file[:number]
        else:
            self.name = file[slash_number + 1:number]
        print(self.name)
        print(self.file_name)


    