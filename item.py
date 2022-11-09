import requests
import json
import os
import re

from re import Match
from typing import TypedDict
from dotenv import load_dotenv
from util import getDataByName, setDataByName, getRegextItem, getRegexItemID

load_dotenv()

fetchData = True

OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

class JSONItem(TypedDict):
    name: str
    id: int

def getItems() -> list[JSONItem]|None:
    return getDataByName("items")

def getItem(itemName:str) -> JSONItem|None:
    items = getItems()
    resultItem = None
    if items != None:
        for item in items:
            if (item["name"] == itemName):
                resultItem = item
                break
    return resultItem

def setItems(items:list[JSONItem]):
    setDataByName("items", items)

def addItem(item:JSONItem):
    items = getItems()
    if (items != None
        and not item in items):
        items.append(item)
        setItems(items)

async def getItemData(itemName:str, itemID:int|None = None) -> JSONItem|None:
    item = getItem(itemName)
    if not item:
        if itemID:
            item = JSONItem(name=itemName, id=itemID)
        elif fetchData:
            item = await retrieveItemData(itemName)
        if item != None:
            addItem(item)
    return item

async def retrieveItemData(itemName:str) -> JSONItem|None:
    # Add coding to check if we have a similar item already in the lootMessages -> no API request needed
    itemFound = False
    keepLooping = True
    itemNameForURL = itemName.replace(" ", "%20")
    attempt = 1
    maxAttempts = 5
    currentPage = 1
    itemID = 0

    while(keepLooping and not itemFound):
        requestURL = f"https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&name.en_US={itemNameForURL}&orderby=id&_page={currentPage}"
        requestHeaders = { "Authorization": f"Bearer {OAUTH_TOKEN}" }
        request = requests.get(requestURL, headers=requestHeaders)

        if request.ok:
            attempt = 1
            responseJSON = json.loads(request.text)
            pageCount = responseJSON["pageCount"]
            print(f"retrieving data for '{itemName}' page {currentPage}/{pageCount} request status OK")
            for result in responseJSON["results"]:
                if result["data"]["name"]["en_US"] == itemName:
                    itemFound = True
                    itemID = result["data"]["id"]
            if currentPage == pageCount:
                keepLooping = False
            else:
                currentPage = currentPage + 1
        else:
            print(f"retrieving data for '{itemName}' request status NOT OK (attempt {attempt}/{maxAttempts}) reason:")
            print(request.reason)
            if (request.reason == "Unauthorized"):
                keepLooping = False
                fetchData = False
            if (attempt == maxAttempts):
                keepLooping = False
            else:
                attempt = attempt + 1

    if itemFound:
        return JSONItem(name=itemName, id=itemID)
    else:
        return None

def getWowHeadURL(item:JSONItem) -> str:
        itemNameFormatted = item["name"].lower()
        itemNameFormatted = itemNameFormatted.replace(" ", "-")
        return f"https://www.wowhead.com/wotlk/item={item['id']}/{itemNameFormatted}"

async def getItemsForString(context:str) -> list[JSONItem]:
    items = []

    matches = re.findall(getRegextItem(), context)
    for match in matches:
        itemName = None
        itemID = None
        itemIDMatch = None

        if isinstance(match, str):
            itemName = match
        elif isinstance(match, Match):
            itemName = match.group()
            itemIDMatch = re.search(getRegexItemID(), match.group(1))
        else:
            itemName = match[0]
            if match[1]:
                itemIDMatch = re.search(getRegexItemID(), match[1])

        if itemName:
            if itemIDMatch:
                itemID = int(itemIDMatch.group(0))
            item = await getItemData(itemName, itemID)
            if item:
                items.append(item)

    return items