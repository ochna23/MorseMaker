import json
from App.Asset.Symbol.Symbol import symbol
def getSignalList(inputText,lng):
    #json格納場所
    jsonPass = ""
    
    #json指定
    if lng:
        #日本語
        jsonPass = symbol.JAPANESE_PATH
    else:
        #英語
        jsonPass = symbol.ALPHABET_PARH

    #json読み込み
    json_open = open(jsonPass,"r",encoding="utf-8")
    json_load = json.load(json_open)


    #結果辞書型配列
    resultList = []

    #配列編集
    for txt in inputText:
        resultList.append({symbol.KEY_TXT:txt,symbol.KEY_SIGNAL:json_load[txt]})
    return resultList