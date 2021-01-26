from tkinter import *
import tkinter.ttk as ttk

class CursorSample(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        mac_cursorlist=[
        "arrow","top_left_arrow","left_ptr","cross",
        "crosshair","tcross","ibeam","none","xterm","copyarrow",
        "aliasarrow","contextualmenuarrow","movearrow","text",
        "cross-hair","hand","openhand","closedhand",
        "fist","pointinghand","resize","resizeleft","resizeright",
        "resizeleftright","resizeup","resizedown","resizeupdown",
        "resizebottomleft","resizetopleft","resizebottomright",
        "resizetopright","notallowed","poof","wait","countinguphand",
        "countingdownhand","countingupanddownhand","spinning",
        "help","bucket","cancel","eyedrop","eyedrop-full","zoom-in",
        "zoom-out"
        ]

        cursorlist = ["arrow","center_ptr","crosshair",
        "fleur","ibeam","icon","none","sb_h_double_arrow",
        "sb_v_double_arrow","watch","xterm","no",
        "starting","size","size_ne_sw","size_ns","size_nw_se",
        "size_we","uparrow","wait"]
        for item in cursorlist:
            frame = ttk.Labelframe(self,text="cursor",width="30",height="30")
            frame.pack()
            label=ttk.Label(frame,width="",text=item,cursor=item)
            label.pack()


if __name__ == '__main__':
    master = Tk()
    master.title("CursorSample")
    master.geometry("300x800")
    CursorSample(master)
    master.mainloop()