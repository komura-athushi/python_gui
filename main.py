import tkinter as tk
from PIL import Image, ImageTk
import urllib.request as req
 
'''
web上にある画像を保存します
'''
url = "http://imgcc.naver.jp/kaze/mission/USER/20180519/35/3012705/157/500x718xedab7ba7e203cd7576d12004.jpg"
req.urlretrieve(url, "test.jpg")
 
'''
tkinterのメイン
'''
root = tk.Tk()
 
root.geometry('800x560')
root.title('IMG')
 
canvas = tk.Canvas(
    root, # 親要素をメインウィンドウに設定
    width=500,  # 幅を設定
    height=500 # 高さを設定
    #relief=tk.RIDGE  # 枠線を表示
    # 枠線の幅を設定
)
 
canvas.place(x=0, y=0)  # メインウィンドウ上に配置
 
#PILでjpgを使用
img1 = Image.open(open('test.jpg', 'rb'))
img1.thumbnail((500, 500), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1)  # 表示するイメージを用意
 
canvas.create_image(  # キャンバス上にイメージを配置
    0,  # x座標
    0,  # y座標
    image=img1,  # 配置するイメージオブジェクトを指定
    tag="img",  # タグで引数を追加する。
    anchor=tk.NW  # 配置の起点となる位置を左上隅に指定
)

pressed_x = pressed_y = 0
item_id = -1

def pressed(event):
    global pressed_x, pressed_y, item_id
    item_id = canvas.find_closest(event.x, event.y)
    tag = canvas.gettags(item_id[0])[0]
    item = canvas.type(tag)
    #print(item)
    #print(tag)
    pressed_x = event.x
    pressed_y = event.y

    def select_all(self):
        if self.rect:
            self.test_canvas.coords(self.rect, 0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        else:
            self.rect = self.test_canvas.create_rectangle(0, 0,
                self.CANVAS_WIDTH, self.CANVAS_HEIGHT, outline='red')
        x0, y0, x1, y1 = self.test_canvas.coords(self.rect)
        self.start_x.set('x : ' + str(x0))
        self.start_y.set('y : ' + str(y0))
        self.current_x.set('x : ' + str(x1))
        self.current_y.set('y : ' + str(y1))


def dragged(event):
    global pressed_x, pressed_y, item_id
    item_id = canvas.find_closest(event.x, event.y)
    tag = canvas.gettags(item_id[0])[0]
    item = canvas.type(tag) # rectangle image
    delta_x = event.x - pressed_x
    delta_y = event.y - pressed_y
    if item == "rectangle":
        x0, y0, x1, y1 = canvas.coords(item_id)
        canvas.coords(item_id, x0+delta_x, y0+delta_y, x1+delta_x, y1+delta_y)
    else:
        x, y = canvas.coords(item_id)
        canvas.coords(item_id, x+delta_x, y+delta_y)
    pressed_x = event.x
    pressed_y = event.y

   
# クリックされたとき
canvas.tag_bind("img", "<ButtonPress-1>", pressed)
# ドラッグされたとき
canvas.tag_bind("img", "<B1-Motion>", dragged)
 
root.mainloop()