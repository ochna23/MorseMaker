import threading
import tkinter as tk
import tkinter.filedialog as fd
from .checker import checker
from tkinter import messagebox
from App.Logic.getMorse import getSignalList
from App.Asset.Symbol.Symbol import symbol
from pydub import AudioSegment

import time

class downloadMorse:

    def download(formText,longSound,shortSound,langFlg):
        check = checker
        text = formText.get(0.0,tk.END).strip()

        #文字チェック
        resText = check.textChecker(text,langFlg)

        #エラーの場合
        if not type(resText) is list:
            return messagebox.showerror("テキストエラー",resText)
        
        #音声ファイルチェック
        resSound = check.soundChecker(longSound,shortSound)
        if type(resSound) is str:
            return messagebox.showerror("サウンドエラー",resSound)

        #音声を取得
        longSignal = None
        if longSound[-3:] == "mp3":
            longSignal = AudioSegment.from_file(longSound,format="mp3")
        elif longSound[-3:]=="wav":
            longSignal = AudioSegment.from_file(longSound,format="wav")
        else:
            longSignal = AudioSegment.from_file("./App/Asset/Sound/space.mp3",format="mp3")
            
        shortSignal = None
        if shortSound[-3:]=="mp3":
            shortSignal = AudioSegment.from_file(shortSound,format="mp3")
        elif shortSound[-3:]=="wav":
            shortSignal = AudioSegment.from_file(shortSound,format="wav")
        else:
            shortSignal = AudioSegment.from_file("./App/Asset/Sound/space.mp3",format="mp3")

        intervalSignal = AudioSegment.from_file("./App/Asset/Sound/space.mp3",format="mp3")

        #ファイル作成
        exportFile = AudioSegment.from_file("./App/Asset/Sound/space.mp3",format="mp3")

        signals = getSignalList(resText,langFlg)

        for signal in signals:
            for s in signal[symbol.KEY_SIGNAL]:
                if s == 0:
                    exportFile = exportFile + shortSignal
                elif s == 1:
                    exportFile = exportFile + longSignal
                else:
                    exportFile = exportFile + intervalSignal

            exportFile = exportFile +intervalSignal

        #保存先ダイアログ設定
        root = tk.Tk()
        root.withdraw()

        file = fd.asksaveasfilename(
            initialfile = text[:5]+"_信号",
            defaultextension = ".mp3",
            title = "保存先",
            filetypes=[("mp3", ".mp3")]
        )
        exportFile.export(file,format="mp3")

