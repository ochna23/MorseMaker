import jaconv
import unicodedata
import json
import os
from pydub import AudioSegment

class checker:
    #テキストチェック：返却→エラー：str 正常：list
    def textChecker(text,lang):

        resList = []
        if len(text) < 1:
            return "テキストを入力してください"
        elif len(text)> 30:
            return "テキストは30文字以内で入力してください"
        
        if lang:
            #日本語の場合
            jsonPass = "./App/Asset/Symbol/japanese.json"

            #json読み込み
            json_open = open(jsonPass,"r",encoding="utf-8")
            json_load = json.load(json_open)

            res = False
            errList = []

            for t in list(text):
                try:
                    r = unicodedata.normalize('NFKC',jaconv.hira2kata(t))

                    #大文字を小文字に
                    if r == "ァ":
                        r = "ア"
                    elif r == "ィ":
                        r = "イ"
                    elif r == "ゥ":
                        r = "ウ"
                    elif r =="ェ":
                        r ="エ"
                    elif r =="ォ":
                        r = "オ"
                    elif r == "ャ":
                        r = "ヤ"
                    elif r =="ュ":
                        r = "ユ"
                    elif r == "ョ":
                        r = "ヨ"
                    elif r =="ッ":
                        r ="ツ"

                    json_load[r]
                    resList.append(r)
                except:
                    res = True
                    errList.append(t)
                
            if res:
                tx = ""
                for r in errList:
                    tx += r + ","
                return "("+tx[:-1]+")"+"は日本語モールスでは対応しておりません"
        else:
            #英語の場合
            jsonPass = "./App/Asset/Symbol/alphabet.json"

            #json読み込み
            json_open = open(jsonPass,"r",encoding="utf-8")
            json_load = json.load(json_open)

            res = False
            resList = []
            errList = []

            for t in list(text):
                try:
                    json_load[unicodedata.normalize('NFKC',jaconv.hira2kata(t)).upper()]
                    resList.append(unicodedata.normalize('NFKC',jaconv.hira2kata(t)).upper())
                except:
                    res = True
                    errList.append(t)
                
            if res:
                tx = ""
                for r in errList:
                    tx += r + ","
                return "("+tx[:-1]+")"+"は英語モールスでは対応しておりません"

        return resList
    
    #サウンドチェック
    def soundChecker(longSound,shortSound):
        #入力チェック
        if not longSound.strip():
            return "長音ファイルを選択してください"
        else:
            if not os.path.exists(longSound):
                return "長音ファイルがディレクトリに存在しません"

        if not shortSound.strip():
            return "短音ファイルを選択してください"
        else:
            if not os.path.exists(shortSound):
                return "短音ファイルがディレクトリに存在しません"
        
        
        longFileType = longSound[-4:]
        shortFileType = shortSound[-4:]

        #ファイルの型チェック
        if not(longFileType == ".mp3" or longFileType == ".wav"):
            return "長音ファイルが対応ファイルではありません"
        
        if not(shortFileType == ".mp3" or shortFileType == ".wav"):
            return "短音音ファイルが対応ファイルではありません"
        
        #同一チェック
        if longSound == shortSound:
            return "長音と短音が同一のファイルです"
        
        #ファイルの長さチェック
        if AudioSegment.from_file(longSound,longFileType[1:]).duration_seconds<=0:
            return "長音ファイルが破損しています"
        elif AudioSegment.from_file(longSound,longFileType[1:]).duration_seconds>=2:
            return "長音ファイルが長すぎます"

        if AudioSegment.from_file(shortSound,shortFileType[1:]).duration_seconds<=0:
            return "短音ファイルが破損しています"
        elif AudioSegment.from_file(shortSound,shortFileType[1:]).duration_seconds>=2:
            return "短音ファイルが長すぎます"

        return None