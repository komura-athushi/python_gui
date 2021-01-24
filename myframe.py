import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import re

import myimage
import constant

#画像を覆うように枠を表示するクラス
class MyFrame():
    def __init__(self):
        #枠
        self.rect = None
        self.child_rect = None
        self.position1_x = None
        self.position1_y = None
        self.position2_x = None
        self.position2_y = None


    #座標を取得
    #それぞれ左上と右下のxとy
    def get_position(self):
        return self.position1_x,self.position1_y,self.position2_x,self.position2_y

    #枠を動かす
    def set_position(self,canvas,position_x,position_y,myimg):
        if self.rect == None:
            return
        widht = float(myimg.get_width())
        height = float(myimg.get_height())
        self.position1_x = position_x - widht / 2 - constant.ADD_FRAME_SIZE
        self.position1_y = position_y + height / 2 + constant.ADD_FRAME_SIZE
        self.position2_x = position_x + widht / 2 + constant.ADD_FRAME_SIZE
        self.position2_y = position_y - height / 2 - constant.ADD_FRAME_SIZE
        canvas.coords(self.rect,
        self.position1_x,
        self.position1_y,
        self.position2_x,
        self.position2_y,)

    def get_is_rect(self):
        return self.rect != None


    #座標と画像の大きさ
    def create_frame(self,canvas,position_x,position_y,myimg):
        #枠が存在していたら削除する
        if self.rect != None:
            self.delete_frame(canvas)
        widht = float(myimg.get_width())
        height = float(myimg.get_height())
        self.position1_x = position_x - widht / 2 - constant.ADD_FRAME_SIZE
        self.position1_y = position_y + height / 2 + constant.ADD_FRAME_SIZE
        self.position2_x = position_x + widht / 2 + constant.ADD_FRAME_SIZE
        self.position2_y = position_y - height / 2 - constant.ADD_FRAME_SIZE
        #枠を生成する、引数の順番は、
        #左上のx座標、左上のy座標
        #右下のx座標、右下のy座標
        self.rect = canvas.create_rectangle(
        self.position1_x,
        self.position1_y,
        self.position2_x,
        self.position2_y,
        outline='red') 



    def delete_frame(self,canvas):
        #枠を削除する
        canvas.delete(self.rect)
        self.rect = None
    