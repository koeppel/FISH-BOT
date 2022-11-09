from typing import TypedDict
import json

def getRegexItemID() -> str:
    return r'([0-9]+)'

def getRegextItem() -> str:
    return r'\[([\w+\s]+)(\([0-9]+\))?\]' # gets words inside of "[]" e.g. [Spaulders of Catatonia] also considers if the ID is included e.g. [Spaulders of Catatonia(40594)]

def getAcceptEmoji() -> str:
    return "✔"

def getTrashEmoji() -> str:
    return "🗑"

def getAllData() -> str:
    file = open("data.json", "r+")
    fileContent = file.read()
    file.close()
    return fileContent

def getDataByName(dataName:str) -> list:
    fileContent = getAllData()
    resultData = []
    if fileContent:
        data = json.loads(fileContent)
        if dataName in data:
            resultData = data[dataName]
    return resultData

def setDataByName(dataName:str, data:list):
    fileContent = getAllData()
    if (fileContent):
        outPut = json.loads(fileContent)
        outPut[dataName] = data
    else:
        outPut = {
            dataName: data
        }
    file = open("data.json", "w+")
    file.write(json.dumps(outPut))
    file.close()