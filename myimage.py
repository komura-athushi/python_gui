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
        self.position = [0,0]

        self.img = None
        self.tkimg = None

    #自身の情報を相手にコピーする
    def copy_image_infromation(self,canvas,opp):
        opp.name = self.name
        position=self.get_position()
        opp.set_position(canvas,position[0],position[1])
        opp.scale=self.scale

    #画像の座標を取得
    #戻り値はキャンバス内の座標
    def get_position(self):
        return self.position
    
    #画像を特定の座標に移動させる
    #引数はキャンバス内の座標
    def set_position(self,canvas,position_x,position_y):
        canvas.coords(self.item_id,position_x,position_y)
        self.position=[position_x,position_y]

    #画像を読み込む
    def load_image(self,canvas,file):
        self.file_name = file
        #画像読み込み
        self.img = Image.open(file)
        #画像のサイズを取得
        self.image_size = self.img.size
        #self.img = self.img.resize((int(self.image_size[0]/2),self.image_size[1]))
        #このImageTk?は保持しておかないといけないらしい
        self.position = [constant.CANVAS_WIDTH/2 + constant.ADD_CANVAS_SIZE,constant.CANVAS_HEIGHT/2 + constant.ADD_CANVAS_SIZE]
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.item_id = canvas.create_image(constant.CANVAS_WIDTH/2 + constant.ADD_CANVAS_SIZE,
        constant.CANVAS_HEIGHT/2 + constant.ADD_CANVAS_SIZE,
        image=self.tkimg,
        tags='img')
        
        #ファイルの名前を抽出していく、/と.を除いていく
        slash_number = file.rfind('/')
        number = file.rfind('.')
        if slash_number == -1:
            self.name = file[:number]
        else:
            self.name = file[slash_number + 1:number]
        print(self.name)
        print(self.file_name)


    