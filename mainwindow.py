import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk

#枠のサイズを画像より少し大きくする
ADD_FRAME_SIZE = 1

class Application(tk.Frame):
    CANVAS_WIDTH = 1280
    CANVAS_HEIGHT = 720

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
        #枠を初期化
        self.init_rectangle()
        #メニューの初期化
        self.init_menu()
      

    #画像がクリックされたときの処理
    def pressed(self,event):
        #枠が既に存在していたら
        if self.rect:
            #枠を削除する
            self.canvas.delete(self.rect)
            self.init_rectangle()
        #枠が存在していなければ
        else:
            #選択された画像を持ってくる
            self.item_id = self.canvas.find_closest(event.x, event.y)
            tag = self.canvas.gettags(self.item_id[0])[0]
            item = self.canvas.type(tag)
            #print(item)
            #print(tag)
            #クリックした場所を保存
            self.pressed_x = event.x
            self.pressed_y = event.y
            #画像の座標を持ってくる
            self.sprite_position = self.canvas.coords(self.item_id)
            #画像の座標と大きさを取得する
            sprite_position_x = self.sprite_position[0]
            sprite_position_y = self.sprite_position[1]
            sprite_size_x = self.sprite_size[0]
            sprite_size_y = self.sprite_size[1]
            #枠を生成する、引数の順番は、
            #左上のx座標、左上のy座標
            #右下のx座標、右下のy座標
            self.rect = self.canvas.create_rectangle(
            sprite_position_x - sprite_size_x / 2 - ADD_FRAME_SIZE,
            sprite_position_y + sprite_size_y / 2 + ADD_FRAME_SIZE,
            sprite_position_x + sprite_size_x / 2 + ADD_FRAME_SIZE,
            sprite_position_y - sprite_size_y / 2 - ADD_FRAME_SIZE,
            outline='red')

    
    #画像がドラッグされたときの処理
    def dragged(self,event):
        #枠が表示されていなかったら、
        #画像を動かす処理をしない
        if self.rect == None:
            return
        self.item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(self.item_id[0])[0]
        item = self.canvas.type(tag) # rectangle image
        #クリックした場所とドラッグした場所の差分を計算
        delta_x = event.x - self.pressed_x
        delta_y = event.y - self.pressed_y
        x, y = self.canvas.coords(self.item_id)
        #画像を動かす
        self.canvas.coords(self.item_id, x+delta_x, y+delta_y)
        #枠の座標を取得して
        rect_0x, rect_0y, rect_1x, rect_1y = self.canvas.coords(self.rect)
        #枠を動かす
        #左上のx座標、左上のy座標
        #右下のx座標、右下のy座標
        self.canvas.coords(self.rect,
        rect_0x+delta_x,
        rect_0y+delta_y,
        rect_1x+delta_x,
        rect_1y+delta_y
        )
        self.pressed_x = event.x
        self.pressed_y = event.y

    #ファイル読み込みが選択されたときの処理
    def load_sprite(self):
        #読み込むファイルの拡張子を指定
        typ = [('png画像','*.png'),
        ('jpg画像','*.jpg')]
        #ファイル選択ダイアログを表示
        self.fn = filedialog.askopenfilename(filetypes=typ)
         #画像読み込み
        img = Image.open(self.fn)
        #このImageTk?は保持しておかないといけないらしい
        self.tkimg = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=self.tkimg, tags='img')
        #画像のサイズを取得
        self.sprite_size = img.size
        

    def init_rectangle(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    def init_canvas(self):
        #キャンバス作って
        self.canvas = tk.Canvas(self, width=self.CANVAS_WIDTH,height=self.CANVAS_WIDTH, bg='white')
        self.canvas.pack()
        #関数をバインドする
        self.canvas.tag_bind('img', '<ButtonPress-1>', self.pressed)
        self.canvas.tag_bind('img', '<B1-Motion>', self.dragged)

    def init_various(self):
        self.pressed_x = pressed_y = 0
        self.item_id = -1

    def init_menu(self):
        #メニューを生成
        self.mbar = tk.Menu()
        #メニューコマンドを生成
        self.mcom = tk.Menu(self.mbar,tearoff=0)
        #コマンドを追加
        self.mcom.add_command(label='読み込み',command=self.load_sprite)
        self.mbar.add_cascade(label='ファイル',menu=self.mcom)
        self.master['menu'] = self.mbar


root = tk.Tk()
app = Application(master=root)
app.mainloop()
