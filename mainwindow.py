import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import re

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

        #セレクトしている画像
        self.number_image = None

        self.is_pressd_image = False

    #画像の情報をインスペクターウィンドウに反映させる
    def reflect_information_inspector_window(self):
        if self.item_id == None:
            return
        myimg = self.myimage_list[self.item_id]
        #インスペクターウィンドウに情報を反映させる
        #名前
        self.inspector_image_name_entry.delete(0, tk.END)
        self.inspector_image_name_entry.insert(tk.END,myimg.name)

        #座標
        self.inspector_image_position_x_entry.delete(0, tk.END)
        self.inspector_image_position_y_entry.delete(0, tk.END)
        position = myimg.get_position()
        self.inspector_image_position_x_entry.insert(tk.END,position[0]-constant.ADD_CANVAS_SIZE)
        self.inspector_image_position_y_entry.insert(tk.END,position[1]-constant.ADD_CANVAS_SIZE)

        #ピクセル数
        width=myimg.get_width()
        height=myimg.get_height()
        self.inspector_pixel_size_x_text.set('X : '+str(width))
        self.inspector_pixel_size_y_text.set('Y : '+str(height))

        #スケール
        self.inspector_image_scale_x_entry.delete(0, tk.END)
        self.inspector_image_scale_y_entry.delete(0, tk.END)
        scale=myimg.scale
        self.inspector_image_scale_x_entry.insert(tk.END,scale[0])
        self.inspector_image_scale_y_entry.insert(tk.END,scale[1])

       

    #画像が選択されたときの処理
    def select_image(self):
        try:
        #画像の座標を持ってくる
            self.image_position = self.myimage_list[self.item_id].get_position()
            #画像の座標と大きさを取得する
            image_position_x = self.image_position[0]
            image_position_y = self.image_position[1]

            image_size_x = self.myimage_list[self.item_id].get_width()
            image_size_y = self.myimage_list[self.item_id].get_height()
        except:
            return
        
        #枠を削除する
        self.canvas.delete(self.rect)
        self.init_rectangle()        
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

        #インスペクターウィンドウに情報を反映させる
        self.reflect_information_inspector_window()


    def select_listbox(self,event):
        number = self.project_list.curselection()
        #何も選択されてなかったら処理しない
        if len(number) == 0:
            return
        number2 = 0
        for i in self.myimage_list:
            if number[0] == number2:
                self.item_id = self.myimage_list[i].item_id
                break
            number2+=1
        self.select_image()
        self.number_image = number[0]
            
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
        self.number_image = number
        self.is_pressd_image = True
    
    #スケールを変化させる
    #delta_xとdelta_yはマウスの移動量
    def change_scale(self,delta_x,delta_y):
        if self.is_pressd_image == False:
            return
        print(1)
        try:
            myimg = self.myimage_list[self.item_id]
            #リサイズした後の大きさ
            width = myimg.width
            height=myimg.height
            #リサイズする前の大きさ
            image_size=myimg.image_size

            change_width = width + delta_x
            change_height = height + delta_y

            myimg.scale[0] = change_width / image_size[0]
            myimg.scale[1] = change_height / image_size[1]
            #リサイズするために一旦消してもう一回読み込む
            self.delete_image()
            self.load_image(myimg)
        except:
            a=0
        

    #座標を変化させる
    #delta_xとdelta_yはマウスの移動量
    def change_position(self,delta_x,delta_y):
        img = self.myimage_list[self.item_id]
        position = img.get_position()
        #画像を動かす
        img.set_position(self.canvas,position[0]+delta_x,position[1]+delta_y)
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

    #画像がドラッグされたときの処理
    def dragged(self,event):
        #枠が表示されていなかったら、
        #画像を動かす処理をしない
        if self.rect == None:
            return
        #tag = self.canvas.gettags(self.item_id[0])[0]
        #item = self.canvas.type(tag) # rectangle image
        #クリックした場所とドラッグした場所の差分を計算
        delta_x = event.x - self.pressed_x
        delta_y = event.y - self.pressed_y
        #self.change_position(delta_x,delta_y)
        self.change_scale(delta_x,delta_y)
        self.pressed_x = event.x
        self.pressed_y = event.y

        #インスペクターウィンドウに情報を反映させる
        self.reflect_information_inspector_window()

    #右クリックが終わったとき
    def mouse_release(self,event):
        self.is_pressd_image = False

    #ファイル読み込みが選択されたときの処理
    def load_image(self,original_myimg=None):
        
        fn = None
        if original_myimg == None:
            #読み込むファイルの拡張子を指定
            typ = [('png画像','*.png'),
                ('jpg画像','*.jpg')]
            #ファイル選択ダイアログを表示
            fn = filedialog.askopenfilename(filetypes=typ)
        else:
            fn=original_myimg.file_name
        #画像読み込み
        myimg = myimage.MyImage()
         #複製した画像に複製元の画像の情報をコピーする
        if original_myimg != None:
            myimg.copy_image_infromation(self.canvas,original_myimg)
        myimg.load_image(self.canvas,fn)
        #リストに追加
        self.myimage_list[myimg.item_id] = myimg
        #リストボックスに名前を追加
        self.project_list.insert(tk.END, myimg.name) 
        #レクタングルを設定して、リストボックスも選択する
        self.item_id = myimg.item_id
        self.select_image()
        self.project_list.selection_clear(0, tk.END)
        number = 0
        for i in self.myimage_list:
            if self.item_id == self.myimage_list[i].item_id:
                break
            number+=1
        #リストボックスを選択
        self.project_list.select_set(number)
        self.number_image = number

    #レベルデータを出力する
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
                myimg=self.myimage_list[i]
                #画像の名前を書き出す
                file.write(bytes((str(myimg.name) + ' ').encode()))
                #画像の座標を取得
                x,y = myimg.get_position()
                #画像の座標を書き出す
                file.write(bytes((str(x-constant.ADD_CANVAS_SIZE) + ' ').encode()))
                file.write(bytes((str(y-constant.ADD_CANVAS_SIZE) + ' ').encode()))
                scale=myimg.scale
                #画像のスケールを書き出す
                file.write(bytes((str(scale[0]) + ' ').encode()))
                file.write(bytes((str(scale[1]) + ' ').encode()))
                file.write(bytes('\n'.encode()))
        
        messagebox.showinfo('メッセージ', '書き出しに成功しました！')

    #枠を初期化
    def init_rectangle(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    #マウスが動いた時の処理
    def motion(self,event):
        #マウス座標を取得する
        self.label['text'] = 'x : {}, y : {}'.format(event.x - constant.ADD_CANVAS_SIZE,event.y - constant.ADD_CANVAS_SIZE)

    #画像を複製する
    def duplicate_image(self):
        number = self.project_list.curselection()
        #何も選択されてなかったら処理をしない
        if len(number) == 0:
            return
        number2 = 0
        myimg = None
        for i in self.myimage_list:
            if number[0] == number2:
                myimg = self.myimage_list[i]
                break
            number2+=1
        self.load_image(myimg)
        
    #画像を削除する
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
        self.number_image = None
        
    #文字列検証関数、文字の入力を数字のみに制限させる
    #Falseで入力拒否
    def validation(self,before_word, after_word):
        if len(after_word) == 0:
            return True
        #elif (after_word.isdecimal()):
        #入力された文字が0～9の半角であれば
        elif re.match(re.compile('[0-9]+'), after_word) or re.match(re.compile('-([0-9]+)'), after_word):
            return True
        else:
            return False
            
    
    #入力された情報を反映させる
    def apply_input_information(self):
        #何も選択されてなかったら処理しない
        if self.number_image == None:
            return
        self.project_list.delete(self.number_image)
        self.myimage_list[self.item_id].name = self.inspector_image_name_entry.get()
        self.project_list.insert(self.number_image, self.myimage_list[self.item_id].name)

        self.myimage_list[self.item_id].set_position(self.canvas,
        float(self.inspector_image_position_x_entry.get())+constant.ADD_CANVAS_SIZE,
        float(self.inspector_image_position_y_entry.get())+constant.ADD_CANVAS_SIZE)
        self.myimage_list[self.item_id].scale=[float(self.inspector_image_scale_x_entry.get()),
        float(self.inspector_image_scale_y_entry.get())]
        #リストボックスを選択
        self.project_list.select_set(self.number_image)
        self.select_image()
        myimg = self.myimage_list[self.item_id]
        #リサイズするために一旦消してもう一回読み込む
        self.delete_image()
        self.load_image(myimg)
        

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
        #self.canvas.pack(side=tk.LEFT)

        #関数をバインドする
        self.canvas.tag_bind('img', '<ButtonPress-1>', self.pressed)
        #self.canvas.tag_bind('img', '<B1-Motion>', self.dragged)
        #マウスの座標を表示したい
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<B1-Motion>', self.dragged)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)
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

    #インスペクターウィンドウの名前のラベルを初期化する
    def init_inspector_name_label(self):
        #名前
        inspector_image_name = tk.Label(self.inspector,text='名前')
        inspector_image_name.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_NAME_Y)
        self.inspector_image_name_entry = tk.Entry(self.inspector,width=constant.INSPECTOR_NAME_ENTRY_SIZE_X)
        self.inspector_image_name_entry.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_NAME_ENTRY_Y)


    #インスペクターウィンドウの座標のラベルを初期化する
    def init_inspector_position_label(self):
        inspector_image_name = tk.Label(self.inspector,text='座標')
        inspector_image_name.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_POSITION_Y)

        #X
        inspector_image_position_x = tk.Label(self.inspector,text='x',font=("", "15", ""))
        inspector_image_position_x.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_POSITION_XY_Y)
        #entryを設定
        sv = tk.StringVar()
        self.inspector_image_position_x_entry = tk.Entry(self.inspector,width=constant.INSPECTOR_POSITION_ENTRY_SIZE_X,textvariable=sv)
        self.inspector_image_position_x_entry.place(x=constant.INSPECTOR_POSITION_X_ENTRY_X,y=constant.INSPECTOR_POSITION_ENTRY_Y)
        # %s は変更前文字列, %P は変更後文字列を引数で渡す
        vcmd1 = (self.inspector_image_position_x_entry.register(self.validation), '%s', '%P')
        #Validationコマンドを設定（'key'は文字が入力される毎にイベント発火）
        self.inspector_image_position_x_entry.configure(validate='key', vcmd=vcmd1)

        #y
        inspector_image_position_y = tk.Label(self.inspector,text='y',font=("", "15", ""))
        inspector_image_position_y.place(x=constant.INSPECTOR_POSITION_Y_X,y=constant.INSPECTOR_POSITION_XY_Y)
        #entryを設定
        sv = tk.StringVar()
        self.inspector_image_position_y_entry = tk.Entry(self.inspector,width=constant.INSPECTOR_POSITION_ENTRY_SIZE_X,textvariable=sv)
        self.inspector_image_position_y_entry.place(x=constant.INSPECTOR_POSITION_Y_ENTRY_X,y=constant.INSPECTOR_POSITION_ENTRY_Y)
        # %s は変更前文字列, %P は変更後文字列を引数で渡す
        vcmd2 = (self.inspector_image_position_y_entry.register(self.validation), '%s', '%P')
        #Validationコマンドを設定（'key'は文字が入力される毎にイベント発火）
        self.inspector_image_position_y_entry.configure(validate='key', vcmd=vcmd2)

    #インスペクターウィンドウのスケールのラベルを初期化する
    def init_inspector_scale_label(self):
        inspector_image_scale = tk.Label(self.inspector,text='スケール')
        inspector_image_scale.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_SCALE_Y)

        #X
        inspector_image_scale_x = tk.Label(self.inspector,text='x',font=("", "15", ""))
        inspector_image_scale_x.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_SCALE_XY_Y)
        #entryを設定
        sv = tk.StringVar()
        self.inspector_image_scale_x_entry = tk.Entry(self.inspector,width=constant.INSPECTOR_SCALE_ENTRY_SIZE_X,textvariable=sv)
        self.inspector_image_scale_x_entry.place(x=constant.INSPECTOR_SCALE_X_ENTRY_X,y=constant.INSPECTOR_SCALE_ENTRY_Y)
        # %s は変更前文字列, %P は変更後文字列を引数で渡す
        vcmd1 = (self.inspector_image_scale_x_entry.register(self.validation), '%s', '%P')
        #Validationコマンドを設定（'key'は文字が入力される毎にイベント発火）
        self.inspector_image_scale_x_entry.configure(validate='key', vcmd=vcmd1)

        #y
        inspector_image_scale_y = tk.Label(self.inspector,text='y',font=("", "15", ""))
        inspector_image_scale_y.place(x=constant.INSPECTOR_SCALE_Y_X,y=constant.INSPECTOR_SCALE_XY_Y)
        #entryを設定
        sv = tk.StringVar()
        self.inspector_image_scale_y_entry = tk.Entry(self.inspector,width=constant.INSPECTOR_SCALE_ENTRY_SIZE_X,textvariable=sv)
        self.inspector_image_scale_y_entry.place(x=constant.INSPECTOR_SCALE_Y_ENTRY_X,y=constant.INSPECTOR_SCALE_ENTRY_Y)
        # %s は変更前文字列, %P は変更後文字列を引数で渡す
        vcmd2 = (self.inspector_image_scale_y_entry.register(self.validation), '%s', '%P')
        #Validationコマンドを設定（'key'は文字が入力される毎にイベント発火）
        self.inspector_image_scale_y_entry.configure(validate='key', vcmd=vcmd2)


    #インスペクターウィンドウのピクセルのラベルを初期化する
    def init_inspector_pixel_label(self):
        inspector_pixel_size = tk.Label(self.inspector,text='ピクセル')
        inspector_pixel_size.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTOR_PIXEL_Y)
        self.inspector_pixel_size_x_text = tk.StringVar()
        self.inspector_pixel_size_x_text.set('X : ')
        self.inspector_pixel_size_x = tk.Label(self.inspector,textvariable=self.inspector_pixel_size_x_text,font=('','10'))
        self.inspector_pixel_size_x.place(x=constant.INSPECTOR_STANDARS_POSITION_X,y=constant.INSPECTPR_PIXEL_XY_Y)
        self.inspector_pixel_size_y_text = tk.StringVar()
        self.inspector_pixel_size_y_text.set('Y : ')
        self.inspector_pixel_size_y = tk.Label(self.inspector,textvariable=self.inspector_pixel_size_y_text,font=('','10'))
        self.inspector_pixel_size_y.place(x=constant.INSPECTPR_PIXEL_Y_X,y=constant.INSPECTPR_PIXEL_XY_Y)

    #インスペクターウィンドウ？の初期化
    def init_inspector(self):
        #ラベル配置
        self.inspector = tk.Frame(self.master,width=constant.INSPECTOR_WIDTH,height=constant.INSPECTOR_HEIGHT)
        #self.inspector['bg'] = 'white'
        self.inspector.place(relx=constant.INSPECTOR_RELX,rely=constant.INSPECTOR_RELY)

        #名前項目の初期化
        self.init_inspector_name_label()
        
        #座標項目の初期化
        self.init_inspector_position_label()

        #スケール項目の初期化
        self.init_inspector_scale_label()

        #ピクセル項目の初期化
        self.init_inspector_pixel_label()



        self.inspector_button = tk.Button(self.inspector,text='入力項目を反映させる',command=self.apply_input_information,fg='red')
        self.inspector_button.place(x=40,y=360)
    
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
        
        #画像の複製ボタンを生成
        self.duplicate_button = ttk.Button(
        self.project,
        text='複製',
        command=self.duplicate_image)
        self.duplicate_button.pack(side=tk.LEFT)

        #画像の削除ボタンを生成
        self.delete_button = ttk.Button(
        self.project,
        text='削除',
        command=self.delete_image)
        self.delete_button.pack(side=tk.LEFT)

        

    
root = tk.Tk()
app = Application(master=root)
app.mainloop()
