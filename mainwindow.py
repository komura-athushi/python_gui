import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class Application(tk.Frame):
    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 300

    def __init__(self, master=None):
        super().__init__(master)
        #なんか作って
        self.master = master
        self.master.title('python gui')
        self.pack()
        #キャンバスの初期化
        self.init_canvas()
        #色々初期化
        self.init_various()
        

    def init_canvas(self):
        #キャンバス作って
        self.canvas = tk.Canvas(self, width=1280,height=720, bg='white')
        self.canvas.pack()
        #画像読み込み
        img = Image.open('clockkari2.png')
        self.tkimg = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=self.tkimg, tags="img")

    #画像がクリックされたときの処理
    def pressed(self,event):
        self.item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(self.item_id[0])[0]
        item = self.canvas.type(tag)
        #print(item)
        #print(tag)
        self.pressed_x = event.x
        self.pressed_y = event.y
    
    #画像がドラッグされたときの処理
    def dragged(self,event):
        self.item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(self.item_id[0])[0]
        item = self.canvas.type(tag) # rectangle image
        delta_x = event.x - self.pressed_x
        delta_y = event.y - self.pressed_y
        x, y = self.canvas.coords(self.item_id)
        self.canvas.coords(self.item_id, x+delta_x, y+delta_y)
        self.pressed_x = event.x
        self.pressed_y = event.y

    def init_various(self):
        self.pressed_x = pressed_y = 0
        self.item_id = -1
        
        #関数をバインドする
        self.canvas.tag_bind('img', '<ButtonPress-1>', self.pressed)
        self.canvas.tag_bind("img", "<B1-Motion>", self.dragged)
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()
