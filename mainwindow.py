import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import myimage
import constant


class Application(tk.Frame):
    

    def __init__(self, master=None):
        super().__init__(master)
        #なんか作って
        self.master = master
        self.master.title('python gui')
        #self.master.geometry("1920x1080")
        #ウィンドウ最大可
        self.master.state('zoomed')
        #色
        self.master.configure(bg=constant.WINDOW_COLOR)
        #これをしないとフレームがどうのこうので
        #placeしても表示されない
        self.pack(expand=1, fill=tk.BOTH)
        #self.pack()
        #キャンバスの初期化
        self.init_canvas()
        #色々初期化
        self.init_various()
        #枠を初期化
        self.init_rectangle()
        #メニューの初期化
        self.init_menu()
        #ラベルの初期化
        self.init_label()
        #インスペクターウィンドウ？の初期化
        self.init_inspector()
        #プロジェクトウィンドウ？の初期化
        self.init_project()

        #指定した色を透過する
        #self.master.wm_attributes("-transparentcolor", constant.WINDOW_COLOR)
        #読み込んだ画像のリスト
        self.myimage_list = {}

    def select_image(self):
        try:
        #画像の座標を持ってくる
            self.image_position = self.canvas.coords(self.item_id)
            #画像の座標と大きさを取得する
            image_position_x = self.image_position[0]
            image_position_y = self.image_position[1]
            image_size_x = self.myimage_list[self.item_id].image_size[0]
            image_size_y = self.myimage_list[self.item_id].image_size[1]
        except:
            return
        
        #枠が既に存在していたら
        if self.rect:
            #pass
            #枠を削除する
            #self.canvas.delete(self.rect)
            #self.init_rectangle()
            #枠を動かす
            #左上のx座標、左上のy座標
            #右下のx座標、右下のy座標
            self.canvas.coords(self.rect,
            image_position_x - image_size_x / 2 - constant.ADD_FRAME_SIZE,
            image_position_y + image_size_y / 2 + constant.ADD_FRAME_SIZE,
            image_position_x + image_size_x / 2 + constant.ADD_FRAME_SIZE,
            image_position_y - image_size_y / 2 - constant.ADD_FRAME_SIZE,
            )
        #枠が存在していなければ
        else:
            #枠を生成する、引数の順番は、
            #左上のx座標、左上のy座標
            #右下のx座標、右下のy座標
            self.rect = self.canvas.create_rectangle(
            image_position_x - image_size_x / 2 - constant.ADD_FRAME_SIZE,
            image_position_y + image_size_y / 2 + constant.ADD_FRAME_SIZE,
            image_position_x + image_size_x / 2 + constant.ADD_FRAME_SIZE,
            image_position_y - image_size_y / 2 - constant.ADD_FRAME_SIZE,
            outline='red')
        #選択した画像を上に持ってくる
        self.canvas.tag_raise(self.item_id)       

    def select_listbox(self,event):
        number = self.project_list.curselection()
        number2 = 0
        for i in self.myimage_list:
            if number[0] == number2:
                self.item_id = self.myimage_list[i].item_id
                break
            number2+=1
        self.select_image()
            
    #画像がクリックされたときの処理
    def pressed(self,event):
        #選択された画像を持ってくる
        self.item_id = self.canvas.find_closest(event.x, event.y)[0]
        #tag = self.canvas.gettags(self.item_id[0])[0]
        #print(item)
        #print(tag)
        #クリックした場所を保存
        self.pressed_x = event.x
        self.pressed_y = event.y
        self.select_image()
        self.project_list.selection_clear(0, tk.END)
        number = 0
        for i in self.myimage_list:
            if self.item_id == self.myimage_list[i].item_id:
                break
            number+=1
        #リストボックスを選択
        self.project_list.select_set(number)
    
    #画像がドラッグされたときの処理
    def dragged(self,event):
        #枠が表示されていなかったら、
        #画像を動かす処理をしない
        if self.rect == None:
            return
        self.item_id = self.canvas.find_closest(event.x, event.y)[0]
        #tag = self.canvas.gettags(self.item_id[0])[0]
        #item = self.canvas.type(tag) # rectangle image
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
    def load_image(self,fn=None,list_number=None):
        
        if fn == None:
            #読み込むファイルの拡張子を指定
            typ = [('png画像','*.png'),
                ('jpg画像','*.jpg')]
            #ファイル選択ダイアログを表示
            fn = filedialog.askopenfilename(filetypes=typ)
        #画像読み込み
        myimg = myimage.MyImage()
        myimg.load_image(self.canvas,fn)
        self.myimage_list[myimg.item_id] = myimg
        #リストボックスに名前を追加
        if list_number == None:
            self.project_list.insert(tk.END, myimg.name)
        else:
            self.project_list.insert(list_number, myimg.name)
        #レクタングルを設定して、リストボックスも選択する
        self.item_id = myimg.item_id
        self.select_image()
        self.project_list.selection_clear(0, tk.END)
        number = 0
        if list_number == None:
            for i in self.myimage_list:
                if self.item_id == self.myimage_list[i].item_id:
                    break
                number+=1
        else:
            number = list_number+1
        #リストボックスを選択
        self.project_list.select_set(number)


    def export_level(self):
        #読み込むファイルの拡張子を指定
        typ = [('レベル','*'+constant.FILE_EXTENSION)]
        #ファイル選択ダイアログを表示
        fn = filedialog.asksaveasfilename(filetypes=typ)
        #保存先のファイルが何も選択されてない場合は以下の処理をしない
        if fn == '':
            return
        if fn.find(constant.FILE_EXTENSION) == -1:
            fn += constant.FILE_EXTENSION
        #ファイルをオープンする、withでcloseをしなくていいらしい
        with open(fn,'wb') as file:
            for i in self.myimage_list:
                #画像の名前を書き出す
                file.write(bytes((str(self.myimage_list[i].file_name) + ' ').encode()))
                #画像の座標を取得
                x,y = self.myimage_list[i].get_position(self.canvas)
                #画像の座標を書き出す
                file.write(bytes((str(x-constant.ADD_CANVAS_SIZE) + ' ').encode()))
                file.write(bytes((str(y-constant.ADD_CANVAS_SIZE) + ' ').encode()))
                file.write(bytes('\n'.encode()))
        
        messagebox.showinfo('メッセージ', '書き出しに成功しました！')

    #枠を初期化
    def init_rectangle(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    def motion(self,event):
        #マウス座標を取得する
        self.label['text'] = 'x : {}, y : {}'.format(event.x - constant.ADD_CANVAS_SIZE,event.y - constant.ADD_CANVAS_SIZE)

    def duplicate_image(self):
        number = self.project_list.curselection()
        #何も選択されてなかったら処理をしない
        if len(number) == 0:
            return
        number2 = 0
        fn = None
        for i in self.myimage_list:
            if number[0] == number2:
                fn = self.myimage_list[i].file_name
                break
            number2+=1
        self.load_image(fn)
        
    def delete_image(self):
        number = self.project_list.curselection()
        #何も選択されてなかったら処理をしない
        if len(number) == 0:
            return
        self.project_list.delete(number)
        number2 = 0
        fn = None
        for i in self.myimage_list:
            if number[0] == number2:
                #画像をキャンバスから削除
                self.canvas.delete(self.myimage_list[i].item_id)
                #リストから削除
                self.myimage_list.pop(i)
                break
            number2+=1
        #枠を削除する
        self.canvas.delete(self.rect)
        self.init_rectangle()
        self.item_id = None
        

    #今は使ってない
    #使うときが来るかもしれない
    def on_resize(self,event):
        # 右下のCanvasをリサイズに合わせて高さを自動調整
        #self.height = self.frame.winfo_height() - 30 # 30 == canvas.height
        width = event.width
        height = event.height
        xx=width-(constant.CANVAS_WIDTH+constant.ADD_CANVAS_SIZE*2)
        #self.canvas.place_forget()
        #self.canvas.place(x=xx,y=0)
        #self.canvas.pack()
        #self.canvas.place_forget()
        #self.canvas.pack(side=tk.LEFT,anchor=tk.NE)


    #キャンバスを初期化
    def init_canvas(self):
        #キャンバス作って
        self.canvas = tk.Canvas(self,
        width=constant.CANVAS_WIDTH+constant.ADD_CANVAS_SIZE*2,
        height=constant.CANVAS_HEIGHT+constant.ADD_CANVAS_SIZE*2,
        bg = constant.WINDOW_COLOR)
        self.canvas.place(x=0, y=0)

        #関数をバインドする
        self.canvas.tag_bind('img', '<ButtonPress-1>', self.pressed)
        self.canvas.tag_bind('img', '<B1-Motion>', self.dragged)
        #マウスの座標を表示したい
        self.canvas.bind('<Motion>', self.motion)
        #720*1280の枠を作る
        self.canvas_rect = self.canvas.create_rectangle(
            constant.ADD_CANVAS_SIZE,
            constant.ADD_CANVAS_SIZE,
            constant.CANVAS_WIDTH + constant.ADD_CANVAS_SIZE,
            constant.CANVAS_HEIGHT + constant.ADD_CANVAS_SIZE
        )
        #キャンバスの色をウィンドウの色と同じにする
        #self.canvas['bg'] = self.master['bg']
        self.canvas['bg'] = constant.CANVAS_COLOR
        

    #色々初期化
    def init_various(self):
        self.pressed_x = pressed_y = 0
        self.item_id = -1
        self.item_id_list = -1

    #メニューを初期化
    def init_menu(self):
        #メニューを生成
        self.mbar = tk.Menu()
        #メニューコマンドを生成
        self.mcom = tk.Menu(self.mbar,tearoff=0)
        #コマンドを追加
        self.mcom.add_command(label='画像読み込み',command=self.load_image)
        self.mcom.add_command(label='レベル書き出し',command=self.export_level)
        self.mbar.add_cascade(label='ファイル',menu=self.mcom)
        self.master['menu'] = self.mbar

    #ラベルを初期化
    def init_label(self):
        self.label = tk.Label(self.master,text='x : y :')
        self.label.place(relx=constant.LABEL_RELX, rely=constant.LABEL_RELY)

    #インスペクターウィンドウ？の初期化
    def init_inspector(self):
        #self.inspector = tk.Label(self.master,width=50,height=25)
        #フレーム生成
        self.inspector = tk.Frame(self.master)
        #フレームの中にキャンバス生成
        self.inspector_canvas = tk.Canvas(self.inspector,
        width=constant.INSPECTOR_WIDTH,
        height=constant.INSPECTOR_HEIGHT)
        #キャンバス配置
        self.inspector.place(relx=constant.INSPECTOR_RELX,
        rely=constant.INSPECTOR_RELY)
        #色   
        self.inspector['bg']='white'
        self.inspector_canvas['bg'] = 'white'
        
        #フレームを親にスクロールバーを生成
        self.inspector_bar_y = tk.Scrollbar(self.inspector,orient=tk.VERTICAL,command=self.inspector_canvas.yview)
        #スクロールバーを配置
        self.inspector_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        #キャンバスとスクロールバーを紐づける
        self.inspector_canvas.config(yscrollcommand=self.inspector_bar_y.set)
        #スクロールの範囲を設定
        self.inspector_canvas.config(scrollregion=(0,0,2000,2000))
        #キャンバスを設置、スクロールバーより後に配置すること！！
        self.inspector_canvas.pack()
    
    #プロジェクトウィンドウ？の初期化
    def init_project(self):
        self.project = tk.Frame(self.master)
        self.project_list = tk.Listbox(self.project,
        listvariable=None,
        selectmode='single',
        width=constant.PROJECT_WIDTH,
        height=constant.PROJECT_HEIGHT)
        self.project_list.bind('<<ListboxSelect>>', self.select_listbox)
        self.project.place(relx=constant.INSPECTOR_RELX,
        rely=constant.PROJECT_RELY)

        #フレームを親にスクロールバーを生成
        self.project_bar_y = tk.Scrollbar(self.project,orient=tk.VERTICAL,command=self.project_list.yview)
        #スクロールバーを配置
        self.project_bar_y.pack(side=tk.RIGHT, fill=tk.Y)
        #キャンバスとスクロールバーを紐づける
        self.project_list.config(yscrollcommand=self.project_bar_y.set)
        #なんかよくわからんがスクロールバーが自動で調整される
        self.project_list.see('end')
        #リストを設置
        self.project_list.pack()
        
        self.duplicate_button = ttk.Button(
        self.project,
        text='複製',
        command=self.duplicate_image)
        self.duplicate_button.pack(side=tk.LEFT)

        self.delete_button = ttk.Button(
        self.project,
        text='削除',
        command=self.delete_image)
        self.delete_button.pack(side=tk.LEFT)

        

    
root = tk.Tk()
app = Application(master=root)
app.mainloop()
