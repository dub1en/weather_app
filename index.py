# import requests
# import json

import json
import aiohttp
import asyncio
# Network

from urllib import parse
# Parser

import datetime
# Set Parameter time

import tkinter
# GUI



from enum import Enum

# 아울러 정보 중 강수형태는 코드값으로 값에 대한 의미는 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)입니다.
class RainStyle(Enum):
    NONE = 0
    RAIN = 1
    RAIN_SNOW = 2
    SNOW = 3
    SHOWER = 4
    RAINDROP = 5
    RAINDROP_BLIZZARD = 6
    BLIZZARD = 7
temperature: float = 0.0
# 기온
precipitation: float = 0.0
# 강수량
humidity: int = 0
# 습도
rain_style: RainStyle = RainStyle.NONE
# 강수형태
wind_speed: float = 0.0
# 풍속 (900이상 -900이하일 경우 누락된 값으로 판단)

#### SETTING PARAMETERS
def getCurrentTime():
    nowTime = datetime.datetime.now()
    curTime = nowTime - datetime.timedelta(minutes=30)
    paraDate = curTime.strftime('%Y%m%d')
    paraHour = curTime.strftime('%H')
    paraMinStr = curTime.strftime('%M')
    paraMin = "00" if int(paraMinStr) < 30 else "30"

    t = f"{paraHour}{paraMin}"
    return paraDate, t


def getUrl():
    d, t = getCurrentTime()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    service = parse.unquote('AEzq7pxIxi57hon%2FGWtpa2jrDuCA5Q9a8zG8mXYXJoWBij75R90cczmk93hHsYqQQuO33UTE85P7LxthbWCKcg%3D%3D')
    params = {'serviceKey' : service, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : d, 'base_time' : t, 'nx' : '59', 'ny' : '126' }

    return url, params


##### GET SERVER DATA
async def getWeatherOnServer():
    print("getWeatherOnServer()")
    url, params = getUrl()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            print("Here")
            jsonData = await resp.json()
            print(jsonData)
            (temperature, precipitation, humidity, rain_style, wind_speed) = parseWithJson(getItem(jsonData))

            print(f"현재 신촌의 기온은 {temperature}도이며, 습도는 {humidity}%입니다.")
            return (temperature, precipitation, humidity, rain_style, wind_speed)

##### PARSER
async def getItem(data):
    return data["response"]["body"]["items"]["item"]

async def parseWithJson(json):
    weatherInfo = {}
    for item in json:
        weatherInfo[item["category"]] = item["obsrValue"]
    
    for key in weatherInfo:
        match key:
            case "PTY":
                pt = int(weatherInfo[key])
            case "RN1":
                rn = float(weatherInfo[key])
            case "REH":
                re = int(weatherInfo[key])
            case "T1H":
                t1 = float(weatherInfo[key])
            case "WSD":
                ws = float(weatherInfo[key])
    return (t1, rn, re, pt, ws)


##### UI
def showGUI():
    window = tkinter.Tk()
    window.title("오늘의 날씨")
    window.geometry("200x320+100+100")
    window.resizable(False, False)
    
    window.mainloop()



##### MAIN
    
    
    
showGUI()
loop = asyncio.get_event_loop()
loop.run_until_complete(getWeatherOnServer())