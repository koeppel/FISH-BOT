from typing import TypedDict
import json

def getAcceptEmoji() -> str:
    return "✔"

def getTrashEmoji() -> str:
    return "🗑"

def getAllData() -> str:
    file = open("data.json", "r")
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
    file = open("data.json", "w")
    file.write(json.dumps(outPut))
    file.close()