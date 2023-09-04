import json
from urllib.request import urlopen
from datetime import datetime
import requests
import sys
import logging
import mysql.connector
import threading
import time
import re
import uuid


symbol = []
positions = []
marketData = []

holding = []

class Holding:
  def __init__(self, id, symbol, quality, stopProfitsPosition, stopLostPosition, keyPosition):
    self.id = id
    self.symbol = symbol
    self.quality = quality
    self.stopProfitsPosition = stopProfitsPosition
    self.stopLostPosition = stopLostPosition
    self.keyPosition = keyPosition

def lambda_handler(event, context):
    symbol = []
    positions = []
    marketData = []
    holding = []
    get_Latest_Strong_Volumn_Position(symbol, positions)
    print("symbol:"+str(symbol))
    print("positions:"+str(positions))
    get_Holding(holding)
    print("holding:"+str(holding))
    update_Holding(holding, symbol, positions)
    print("updated holding:"+str(holding))
    check_Market(symbol, marketData)
    print("marketData:"+str(marketData))
    check_Holding(symbol, holding, marketData)
    check_OpenNewOrNot(holding, positions, symbol, marketData)
        
    
def get_Latest_Strong_Volumn_Position(symbol, positions):
    mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
    mycursor = mydb.cursor()
    sql = " SELECT a.symbol, a.positions, a.checkdatetime from patrick_strategy_StrongVolumn a "
    sql += " INNER JOIN "
    sql += " ( SELECT symbol, max(checkdatetime) as latestcheckdatetime FROM patrick_strategy_StrongVolumn group by symbol ) b "
    sql += " ON a.symbol = b.symbol and a.checkdatetime = b.latestcheckdatetime "
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for data in result:
        symbol.append(data[0])
        positions.append(data[1].split(","))
        

def get_Holding(holding):
    mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
    mycursor = mydb.cursor()
    sql = " SELECT id, symbol, quality, stopProfitsPosition, stopLostPosition, keyPosition FROM patrick_strategy_StrongVolumn_OrderMapping WHERE status=0 "
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for data in result:
        h = Holding(data[0], data[1], data[2], data[3], data[4], data[5])
        holding.append(h)
        
        
def update_Holding(holding, symbol, positions):
    for h in holding:
        _position = positions[ symbol.index(h.symbol) ]
        for x in range(len(_position)):
            p = _position[x]
            if(int(p)==int(h.keyPosition)):
                if(h.quality>0):
                    if(int(h.stopLostPosition)!=int(p)):
                        stopProfitsPosition = int(p)
                        stopLostPosition = ( int(_position[x-1]) - ((int(_position[x-1])-int(p))/4) )
                        mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
                        mycursor = mydb.cursor()
                        sql = " UPDATE patrick_strategy_StrongVolumn_OrderMapping set stopLostPosition="+str(stopProfitsPosition)+", stopProfitsPosition="+str(stopLostPosition)+" WHERE id='"+h.id+"' "
                        mycursor.execute(sql)
                        mydb.commit()
                        get_Holding(holding)
                if(h.quality<0):
                    if(int(h.stopLostPosition)!=int(p)):
                        stopProfitsPosition = int(p)
                        stopLostPosition = ( int(_position[x-1]) - ((int(p)-int(_position[x-1]))/4) )
                        mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
                        mycursor = mydb.cursor()
                        sql = " UPDATE patrick_strategy_StrongVolumn_OrderMapping set stopLostPosition="+str(stopProfitsPosition)+", stopProfitsPosition="+str(stopLostPosition)+" WHERE id='"+h.id+"' "
                        mycursor.execute(sql)
                        mydb.commit()
                        get_Holding(holding)
                        
                        

def check_Holding(symbol, holding, marketData):
    for h in holding:
        mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
        mycursor = mydb.cursor()
        marketPrice = marketData[ symbol.index(h.symbol) ]
        if(marketPrice is not None):
            if h.quality > 0:
                if int(marketPrice) >= h.stopProfitsPosition or marketPrice <= h.stopLostPosition:
                    sql = " UPDATE patrick_strategy_StrongVolumn_OrderMapping set status=1, offsetPosition="+str(marketPrice)+" WHERE id='"+h.id+"' "
                    mycursor.execute(sql)
                    mydb.commit()
            if h.quality < 0:
                if int(marketPrice) <= h.stopProfitsPosition or marketPrice >= h.stopLostPosition:
                    sql = " UPDATE patrick_strategy_StrongVolumn_OrderMapping set status=1, offsetPosition="+str(marketPrice)+" WHERE id='"+h.id+"' "
                    mycursor.execute(sql)
                    mydb.commit()
                

def check_OpenNewOrNot(holding, positions, symbol, marketData):
    for i in range(0, len(symbol)):
        _symbol = symbol[i]
        alreadyOnHold = False
        for h in holding:
            if h.symbol == _symbol:
                alreadyOnHold = True
                break
        
        if alreadyOnHold == False:
            _marketPrice = int(marketData[i])
            _position = positions[i]
            upperPos = 99999
            lowerPos = -99999
            p_count = 0
            for p in _position:
                _p = int(p)
                if (_p - _marketPrice)>0 and (_p - _marketPrice)<upperPos:
                        upperPos = _p
                if (_p - _marketPrice)<0 and (_p - _marketPrice)>lowerPos:
                        lowerPos = _p
                p_count+=1
            print("upperPos:{}, lowerPos:{}".format(upperPos, lowerPos))
            if(upperPos!=99999 and lowerPos!=-99999):
                if(abs(upperPos-_marketPrice) < abs(lowerPos-_marketPrice)):
                    if(_marketPrice < (upperPos-(upperPos-lowerPos)/4) and _marketPrice > (upperPos-(upperPos-lowerPos)/4)*0.9 ):
                        mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
                        mycursor = mydb.cursor()
                        sql = " INSERT INTO patrick_strategy_StrongVolumn_OrderMapping VALUES('{}', '{}', {}, NOW(), {}, {}, {}, {}, NULL, {})".format(
                            uuid.uuid4(),
                            _symbol,
                            -1,
                            upperPos,
                            _marketPrice,
                            str((lowerPos+(upperPos-lowerPos)/4)),
                            upperPos,
                            0
                        )
                        print("put sql:{}".format(sql))
                        mycursor.execute(sql)
                        mydb.commit()
                if(abs(lowerPos-_marketPrice) < abs(upperPos-_marketPrice)):
                    if(_marketPrice > (lowerPos+(upperPos-lowerPos)/4) and _marketPrice < (lowerPos+(upperPos-lowerPos)/4)*1.1 ):
                        mydb=mysql.connector.connect(host="151.106.124.51", user="u628315660_projectB", password="wtfWTF0506536", database="u628315660_projectB")
                        mycursor = mydb.cursor()
                        sql = " INSERT INTO patrick_strategy_StrongVolumn_OrderMapping VALUES('{}', '{}', {}, NOW(), {}, {}, {}, {}, NULL, {})".format(
                            uuid.uuid4(),
                            _symbol,
                            1,
                            lowerPos,
                            _marketPrice,
                            str((upperPos-(upperPos-lowerPos)/4)),
                            lowerPos,
                            0
                        )
                        print("call sql:{}".format(sql))
                        mycursor.execute(sql)
                        mydb.commit()
                    
        

def check_Market(symbol, marketData):
    for s in symbol:
        if s=="YM_Future":
            marketData.append(update_YM_Future())
        if s=="HSI_Future":
            marketData.append(update_HSI_Future())


def update_YM_Future():
    url = 'https://markets.businessinsider.com/futures/dow-futures'
    response = requests.get(url)
    result = None
    if response.status_code == 200:
        content = response.text
        target_substr1 = '<span class="price-section__current-value">'
        startPos_of_target_substr1 = content.find(target_substr1) + len(target_substr1)
        result = int((content[startPos_of_target_substr1 : startPos_of_target_substr1+6]).replace(",", ""))
    return result
    
def update_HSI_Future():
    url = 'http://www.aastocks.com/en/stocks/market/bmpfutures.aspx'
    response = requests.get(url)
    result = None
    if response.status_code == 200:
        content = response.text
        target_substr1 = '<div class="font26 bold cls ff-arial">'
        startPos_of_target_substr1 = content.find(target_substr1) + len(target_substr1)
        result = int((content[startPos_of_target_substr1 : startPos_of_target_substr1+8]).replace(",", ""))
    return result

