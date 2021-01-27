import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import glob
import sys

import myimage
import constant

#画像を覆うように枠を表示するクラス
class MyFrame():
    def __init__(self):
        #枠
        self.rect = None
        self.rect_list = {}
        #最初から、上　下　左　右　左上　右下　右上　左下
        self.myimage_position_list = {
            0 : [0.0,-1/2, 0,-1],
            1 : [0.0,1/2 ,0,1],
            2 : [-1/2,0.0, -1,0],
            3 : [1/2,0.0, 1,0],
            4 : [-1/2,-1/2, -1,-1],
            5 : [1/2,1/2, 1,1],
            6 : [-1/2,1/2, -1,1],
            7 : [1/2,-1/2, 1,-1]
        }
        self.myimage_id_list = None
        self.position = [0.0,0.0]
        self.position1_x = None
        self.position1_y = None
        self.position2_x = None
        self.position2_y = None
        self.color_move = 'red'
        self.color_scale = 'blue'


        self.is_move = False

    #8つの枠のうち、どこの枠をクリックしたのか判断する
    def determine_where_frame_pressed(self,item_id):
        for i in self.rect_list:
            if self.rect_list[i].item_id == item_id:
                return i 
    
    #座標からどこの枠が選択されたのか判断する
    #座標はキャンバス座標
    def determine_where_frame_pressed_from_position(self,position_x,position_y):
        number = 0
        min_diff = sys.float_info.max   
        for i in self.rect_list:
            rect_position = self.rect_list[i].get_position()
            diff = abs(rect_position[0] - position_x) + abs(rect_position[1] - position_y)
            if min_diff > diff:
                min_diff = diff
                number =i
        return number

    def calculate_size_image(self,number_rect,myimage,delta_x,delta_y):
            #現在の大きさ
            width = myimage.get_width()
            height = myimage.get_height()

            #現在の大きさ
            image_size = myimage.image_size

            #上下左右の枠が押されたいた時
            if number_rect < len(self.rect_list) / 2:
                delta_x *= self.myimage_position_list[number_rect][2]
                delta_y *= self.myimage_position_list[number_rect][3]
                width += delta_x * 2
                height += delta_y * 2
                return width / image_size[0], height / image_size[1]
            else:
                delta = delta_x * self.myimage_position_list[number_rect][2] + delta_y * self.myimage_position_list[number_rect][3]
                width += delta
                height += delta
                scale = (width / image_size[0] + height / image_size[1]) / 2
                return scale,scale

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

        self.move_rect(canvas,position_x,position_y)

    def get_is_rect(self):
        return self.rect != None

    def move_rect(self,canvas,position_x,position_y):
            delta_x = position_x - self.position[0]
            delta_y = position_y - self.position[1]

            for i in self.rect_list:
                self.rect_list[i].move_position(canvas,delta_x,delta_y)
                #選択した画像を上に持ってくる
                canvas.tag_raise(self.rect_list[i].item_id)

            self.position = [position_x,position_y]

    def create_image(self,canvas,position_x,position_y,myimg):
        fn = glob.glob('Assets/rect.png')
        for i in range(constant.NUMBER_IMAGE):
            rect = myimage.MyImage()
            rect.load_image(canvas,fn[0],constant.MYFRAME_IMAGE_TAG)
            widht = float(myimg.get_width())
            height = float(myimg.get_height())
            pos_x = position_x + widht * self.myimage_position_list[i][0]
            pos_y = position_y + height * self.myimage_position_list[i][1]
            #枠は画像よりちょっと大き目なのでそれを考慮した座標を指定する
            rect.set_position(canvas,
            pos_x + constant.ADD_FRAME_SIZE * self.myimage_position_list[i][2],
            pos_y + constant.ADD_FRAME_SIZE * self.myimage_position_list[i][3]
            )
            self.rect_list[i] = rect

    #座標と画像の大きさ
    def create_frame(self,canvas,position_x,position_y,myimg):
        #枠が存在していたら削除する
        if self.rect != None:
            self.delete_frame(canvas)
        self.position = [position_x,position_y]
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

       
        self.create_image(canvas,position_x,position_y,myimg)


    def delete_frame(self,canvas):
        #枠を削除する
        canvas.delete(self.rect)
        self.rect = None
        for i in self.rect_list:
            canvas.delete(self.rect_list[i].item_id)
        self.rect_list.clear()
    