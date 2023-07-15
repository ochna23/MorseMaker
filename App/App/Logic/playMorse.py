import json
import threading
import tkinter as tk
from .checker import checker
from tkinter import messagebox
from playsound import playsound
from App.Logic.getMorse import getSignalList
from App.Asset.Symbol.Symbol import symbol


import time


class playMarse:
    

    def playMorse(formText,longSound,shortSound,langFlg,playTxt,nowTxt,nowSound):
        check = checker
        text = formText.get(0.0,tk.END).strip()

        #文字チェック
        resText = check.textChecker(text,langFlg)
        #エラーの場合
        if not type(resText) is list:
            playTxt.set(symbol.PLAY_BTN)
            formText.configure(state=tk.NORMAL)
            return messagebox.showerror("テキストエラー",resText)
        
        #音声ファイルチェック
        resSound = check.soundChecker(longSound,shortSound)
        if type(resSound) is str:
            playTxt.set(symbol.PLAY_BTN)
            
            return messagebox.showerror("サウンドエラー",resSound)

        #再生スレッド
        def playSignals():
            #再生制御
            playFlg = 1
            global loopFlg
            loopFlg = True

            def waitTimer():
                time.sleep(2)
                nowTxt.set("ロード中")
                global loopFlg
                loopFlg = False

            waitThread = threading.Thread(target=waitTimer)
            waitThread.start()

            while loopFlg:
                if playTxt.get()==symbol.PLAY_BTN:
                    playFlg = 0

            if playFlg == 0:
                nowTxt.set("")
                return

            signals = getSignalList(resText,langFlg)
            
            for signal in signals:
                nowTxt.set(signal[symbol.KEY_TXT])
                for s in signal[symbol.KEY_SIGNAL]:
                    if playTxt.get() == symbol.STOP_BTN:
                        if s == 0:
                            nowSound.set(symbol.SHORT_SOUND)
                            playsound(shortSound)
                        elif s == 1:
                            nowSound.set(symbol.LONG_SOUND)
                            playsound(longSound)
                        else:
                            nowSound.set("")
                            playInterval()
                    else:
                        playFlg = "0"
                        nowTxt.set("")
                        nowSound.set("")
                        return    
                nowSound.set("")
                nowTxt.set("")
                playInterval()

            playFlg = "0"
            nowTxt.set("")
            nowSound.set("")
            playTxt.set(symbol.PLAY_BTN)
        
        soundThread = threading.Thread(target=playSignals)
        soundThread.start()

        def playInterval():
            playsound("./App/Asset/Sound/space.mp3")    
                
    
    
