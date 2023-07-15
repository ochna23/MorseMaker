import threading
import os,sys
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from App.Asset.Symbol.Symbol import symbol

from App.Logic.playMorse import playMarse

#幅
width = 480
#高さ
heigth = 360

#基本ウィンドウの作成
root = tk.Tk()

#内部パラメータ
#言語フラグ
langText = tk.StringVar()
langText.set("ア")
#再生フラグ:・・・再生中
playText = tk.StringVar()
playText.set("再生")

#現表示文字数
txtCnt = tk.StringVar()
txtCnt.set(str(0)+"/30")

#再生中文字
nowText = tk.StringVar()
nowText.set("")

#再生音
nowSound = tk.StringVar()
nowSound.set("")

#画面本体
def baseWindow():
    #タイトル
    root.title("MorseMaker")
    #サイズ
    root.geometry("480x360")
    root.resizable(width=False,height=False) 
    #背景色：緑
    root.config(bg="lightgreen")

    #タイトルラベル
    titleLabel()
    #長音
    long = longSound()
    #短音
    short= shortSound()
    #警告文
    alertLabel()
    #テキスト部
    textCnt = cntTxtLen()
    formText = textPart(textCnt)
    
    #コントロールボタン
    langBtn()
    playBtn(formText,long,short)
    downloadBtn()
    nowTxtLbl()
    nowSoundLbl()

    #テキスト入力制御
    if playText.get() == symbol.PLAY_BTN:
        formText.configure(state=tk.NORMAL)
    else:
        formText.configure(state=tk.DISABLED)
    
    #メインループ
    root.mainloop()

#画面項目一覧
#タイトルラベル
def titleLabel():
    #タイトルラベル
    titleLabel = tk.Label(text="モールスメイカー")
    #色
    titleLabel.config(fg="white")
    titleLabel.config(bg="lightgreen")
    #フォントサイズ
    titleLabel.config(font=("",36))
    #配置
    titleLabel.place(x=width/8,y=heigth/12,width=width*3/4,height=heigth/10)

#長音選択
def longSound():
    
    #ラベル
    longFileLabel = tk.Label(text="─")
    longFileLabel.config(bg="lightgreen")
    longFileLabel.config(fg="black")
    longFileLabel.config(font=("",11))

    #ファイル選択
    longFile = tk.Entry(root)

    #参照ボタン
    def findBtn():
        longFile.delete(0,"end")
        idir = "./"
        longFiletype = [(".mp3","*.mp3"), (".wav",".wav")]
        longFile_path = tk.filedialog.askopenfilename(filetypes = longFiletype, initialdir = idir)
        longFile.insert(tk.END, longFile_path)
    longFileFind = tk.Button(text="参照",command=findBtn)


    #配置
    longFileLabel.place(x=0,y=heigth/4,width=width/8,height=heigth/12)
    longFile.place(x=width/12,y=heigth/4,width=width*3/10,height=heigth/12)
    longFileFind.place(x=width/5*2,y=heigth/4,width=width/10,height=heigth/12)

    return longFile

#短音選択
def shortSound():
    
    #ラベル
    shortFileLabel = tk.Label(text="・")
    shortFileLabel.config(bg="lightgreen")
    shortFileLabel.config(fg="black")
    shortFileLabel.config(font=("",11))

    #ファイル選択
    shortFile = tk.Entry(root)

    #参照ボタン
    def findBtn():
        shortFile.delete(0,"end")
        idir = "./"
        shortFiletype = [(".mp3","*.mp3"), (".wav","*.wav")]
        shortFile_path = tk.filedialog.askopenfilename(filetypes = shortFiletype, initialdir = idir)
        shortFile.insert(tk.END, shortFile_path)
    shortFileFind = tk.Button(text="参照",command=findBtn)


    #配置
    shortFileLabel.place(x=0,y=heigth/8*3,width=width/8,height=heigth/12)
    shortFile.place(x=width/12,y=heigth/8*3,width=width*3/10,height=heigth/12)
    shortFileFind.place(x=width/5*2,y=heigth/8*3,width=width/10,height=heigth/12)

    return shortFile

#脚注
def alertLabel():
    #アラートラベル
    alertLabel = tk.Label(text="※\n"+"音声ファイルは2秒以内\n"+"ファイルはmp3,wavに対応\n"+"テキストは30文字まで")
    #色
    alertLabel.config(fg="black")
    alertLabel.config(bg="lightgreen")
    #フォントサイズ
    alertLabel.config(font=("",12))
    alertLabel.config(justify=tk.LEFT)

    #配置
    alertLabel.place(x=width/2,y=heigth/4,width=width/2,height=heigth/5)

#テキスト
def textPart(el):
    text = tk.Text(root)
    text.config(font=("",24))

    text.place(x=width/18,y=heigth*6/11,width=width/2,height=heigth/3)
    #文字カウント
    def countText(e):
        s = len(text.get(0.0,tk.END ))-1
        txtCnt.set(str(s)+"/30")
        if s<30:
            el["foreground"] = "black"
        else:
            el["foreground"] = "red"

    text.bind("<KeyRelease>",countText)
    return text

#言語切り替え
def langBtn():  
    def clickBtn():
        if langText.get() == symbol.LNG_JPN:
            langText.set(symbol.LNG_ENG)
        else:
            langText.set(symbol.LNG_JPN)

    langBtn = tk.Button(root,textvariable=langText,command=clickBtn)
    langBtn.place(x=width*4/7,y=heigth*4/5,width=width/15,height=heigth/12)

#再生・停止ボタン
def playBtn(formText,formLong,formShort):  
    def clickBtn():
        #パラメータ
        if playText.get() == symbol.PLAY_BTN:
            text = formText.get(0.0,tk.END).strip()
            long = formLong.get().strip()
            short = formShort.get().strip()
            langFlg = True
            if langText.get() == symbol.LNG_JPN:
                langFlg = True
            else:
                langFlg =False
            playText.set(symbol.STOP_BTN)
            formText.configure(state=tk.DISABLED)
            player = playMarse
            player.playMorse(formText,long,short,langFlg,playText,nowText,nowSound)
        else:
            formText.configure(state=tk.NORMAL)
            playText.set(symbol.PLAY_BTN)

    playBtn = tk.Button(root,textvariable=playText,command=clickBtn)
    playBtn.place(x=width*2/3,y=heigth*4/5,width=width/10,height=heigth/12)

#保存ボタン
def downloadBtn():
    text = tk.StringVar()
    text.set(symbol.SAVE_BTN)
    def clickBtn():
        if playText.get() == symbol.PLAY_SYMBOL:
            print("保存メソッド")

    downBtn = tk.Button(root,textvariable=text,command=clickBtn)
    downBtn.place(x=width*4/5,y=heigth*4/5,width=width/10,height=heigth/12)

#数字カウント
def cntTxtLen():
    cntLabel = tk.Label(textvariable=txtCnt,fg="black",bg="lightgreen")
    cntLabel.config(font=("",11))
    cntLabel.place(x=width/3,y=heigth*9/10,width=width*3/10,height=heigth/12)

    return cntLabel

#再生文字
def nowTxtLbl():
    txtLbl = tk.Label(textvariable=nowText,fg="black",bg="lightgreen")
    txtLbl.config(font=("",48))
    txtLbl.place(x=width*21/27,y=heigth*6/11,width=width/5,height=heigth/4)

    return txtLbl
    
#再生音
def nowSoundLbl():
    soundLbl = tk.Label(textvariable=nowSound,fg="black",bg="lightgreen")
    soundLbl.config(font=("",48))
    soundLbl.place(x=width*12/21,y=heigth*6/11,width=width/5,height=heigth/4)

    return soundLbl

    