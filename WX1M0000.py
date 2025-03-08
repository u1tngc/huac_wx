#PGM-ID:WX1M0000
#PGM-NAME:WX資料取得メイン

import datetime
import os
from PIL import Image
from pypdf import PdfWriter
from PyPDF2 import PdfReader, PdfWriter
import requests
import time
import webbrowser

import WX0S0100
import WX1S0001
import WX0S0200

class WX1M0000:
    nowdatetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def main(shori_Kbn,mt_location):

    blip = 0
    if shori_Kbn == "自家用":
        shoriKbn = 1
        msg = kyotsu_shori(shoriKbn, mt_location)
        file_name = ['wxファイル統合版_' + WX1M0000.nowdatetime + '.pdf']
    elif shori_Kbn == "教証":
        shoriKbn = 2
        msg = kyotsu_shori(shoriKbn, mt_location)
        file_name = ['wxファイル統合版_' + WX1M0000.nowdatetime + '.pdf', 'wx予報支援資料_' + WX1M0000.nowdatetime + '.pdf']
    return msg, file_name

def kyotsu_shori(shoriKbn, mt_location):
    try:
        currentDateTime = datetime.datetime.now()
        if shoriKbn != 0:
            currentDateTime = get_time()
            timeKbn = timeCheck(currentDateTime,1)
            #RJTYのmetar取得
            if shoriKbn == 1:
                fileName = [""] * 7
                #地上天気図・過去→現在→予報を取得
                fileName = get_asas(currentDateTime, fileName)
                #高層天気図850/700/500/300を取得（最新版）
                fileName = get_kosou(timeKbn, fileName)
                #短期予報解説資料
                fileName = get_tanki(fileName)
            elif shoriKbn == 2:
                fileName = [""] * 15
                fileName = WX1S0001.get_kyosho(timeKbn, currentDateTime, fileName)
                get_DOC(currentDateTime)
            metar_flg = 1
            fileName_MetarTaf = []
            try:
                if mt_location == "":
                    fileName_MetarTaf.append(get_MetarTaf("RJTY"))
                    retCD = WX0S0200.translate_MetarTaf(fileName_MetarTaf[0], "")
                else:
                    fileName_MetarTaf.append(get_MetarTaf("RJTY"))
                    retCD = WX0S0200.translate_MetarTaf(fileName_MetarTaf[0], "")
                    time.sleep(2)
                    fileName_MetarTaf.append(get_MetarTaf(mt_location))
                    if fileName_MetarTaf[1] == "":
                        metar_flg = 2
                    else:
                        retCD = WX0S0200.translate_MetarTaf(fileName_MetarTaf[1], "")
                    try:
                        os.rename('Metar.pdf', f"MetarTaf_{fileName_MetarTaf[1]}.pdf")
                    except FileNotFoundError:
                        pass
            except:
                metar_flg = 0
            url = 'https://tenki.jp/forecast/3/14/4320/11202/1hour.html'
            webbrowser.open(url, new=0, autoraise=True)
            blip = get_blipmap()
            html_name = WX0S0100.getWx(shoriKbn, "360-0222,JP", WX1M0000.nowdatetime,"")
            append_pdf(fileName_MetarTaf, fileName, blip, metar_flg)
            if shoriKbn == 2: 
                rotatePDF()
            removefiles(fileName_MetarTaf, fileName, blip, metar_flg)
            time.sleep(2)
            if metar_flg == 0:
                msg =  "metarもしくはtafの取得ができませんでした。"
            elif metar_flg == 2:
                msg = "指定した飛行場のMETAR/TAFを取得できませんでした。\n横田飛行場のMETAR/TAFのみ出力しています。"
            elif blip  == 1:
                msg = "処理が通常終了しました"
            else:
                msg =  "処理が終了しました。\nBlipMapの取得はできませんでした。\n楽天系の回線では取得できません。"
    except requests.exceptions.Timeout:
        msg = "異常終了しました。\nネットワークが弱いです。"
    except requests.exceptions.ConnectionError:
        msg = "異常終了しました。\nインターネットに接続されていません。"
    except PermissionError:
        msg =  "異常終了しました。\n開いているpdfファイルを閉じてから再実行してください。"
    return msg

def get_time():
    currentTimeUnix = time.time()
    currentDateTime = datetime.datetime.fromtimestamp(currentTimeUnix)
    return currentDateTime

def timeCheck(currentDateTime,kino_cd):
    #現在時刻の取得
    currentTime = currentDateTime.time()
    if kino_cd == 1:
        time0900 = datetime.time(13,00,00) #高層天気図0900の更新時間
        time2100 = datetime.time(1,00,00) #高層天気図2100の更新時間
        time0000 = datetime.time(0,00,00)
        time0300 = datetime.time(5,45,00) #地上天気図0300の更新時間
        if currentTime > time2100 and currentTime < time0900:
            timeKbn = 21 #2100
        elif currentTime > time0000 and currentTime < time2100:
            timeKbn = 90 #0900
        else:
            timeKbn = 9 #0900
        return timeKbn
    elif kino_cd == 2:
        time2100 = datetime.time(23,45,00) #地上天気図2100の更新時間
        time0300 = datetime.time(5,45,00) #地上天気図0300の更新時間
        if currentTime > time2100 or currentTime < time0300:
            timeKbn = 21 #2100
        else:
            timeKbn = 3 #0900
    elif kino_cd == 3:
        time0900 = datetime.time(13,45,00) #2100の更新時間
        time2100 = datetime.time(1,45,00) #0900の更新時間
        if currentTime > time2100 and currentTime < time0900:
            timeKbn = 21 #2100
        else:
            timeKbn = 9 #0900
        return timeKbn

def get_asas(currentDateTime: datetime, fileName):
  #地上天気図（実況）  
    url_asas = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/ASAS_COLOR.pdf'
    response = requests.get(url_asas, timeout = 10)
    file = open("地上天気図(実況).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[1] = "地上天気図(実況).pdf"

  #地上天気図（予報）  
    url_fsas24 = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/FSAS24_COLOR_ASIA.pdf'
    response = requests.get(url_fsas24)
    file = open("地上天気図(予報・当日21時).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[2] = "地上天気図(予報・当日21時).pdf"

  #地上天気図（予報）  
    url_fsas48 = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/FSAS48_COLOR_ASIA.pdf'
    response = requests.get(url_fsas48)
    file = open("地上天気図(予報・翌日21時).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[3] = "地上天気図(予報・翌日21時).pdf"

  #地上天気図（過去） 
    #昨日21時のＵＲＬを準備  
    url1 = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/'
    url3 = '/ASAS_COLOR_'
    currentDateTimeYesterday = currentDateTime + datetime.timedelta(days=-1)
    url2 =  str(currentDateTimeYesterday.strftime('%Y%m'))
    timeKbn = timeCheck(currentDateTime,2)
    if timeKbn == 21: #最新版が昨日21時版の場合は一昨日の21時を取得
        hours = int(currentDateTime.hour)
        minutes = int(currentDateTime.minute)
        asas_time = (hours * 60) + minutes
        if asas_time <= 330:
            currentDateTimeYesterday = currentDateTimeYesterday + datetime.timedelta(days=-1)
            url2 =  str(currentDateTime.strftime('%Y%m'))        
    url4 = str(currentDateTimeYesterday.strftime('%Y%m%d'))
    url5 = '1200.pdf'
    url_asasPast = url1 + url2 + url3 + url4 + url5
    #ファイル取得
    response = requests.get(url_asasPast)
    file = open("地上天気図(過去).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[0] = "地上天気図(過去).pdf"
    return fileName

def get_kosou(timeKbn, fileName):
    if timeKbn == 21:
        urlTime = '12.pdf'
    else:
        urlTime = '00.pdf'

    url_aupq78 = 'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/aupq78_' + str(urlTime)
    response = requests.get(url_aupq78)
    file = open("高層天気図(850・700).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[4] = "高層天気図(850・700).pdf"
    url_aupq35 = 'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/aupq35_' + str(urlTime)
    response = requests.get(url_aupq35)
    file = open("高層天気図(500・300).pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[5] = "高層天気図(500・300).pdf"
    return fileName

def get_MetarTaf(location):
    url = f'https://aviationweather.gov/cgi-bin/data/metar.php?ids={location}&hours=1&order=id%2C-obs&sep=true&taf=true'
    response = requests.get(url)
    file_name = f"{location}_x"
    file_path = f"MetarTaf_{file_name}.txt"
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(200000):
            file.write(chunk)
        file.close() 
    if file_empty(f"MetarTaf_{file_name}"):
        return file_name
    else:
        get_eof = 0
        mt_hour = 1
        while get_eof == 0:
            mt_hour = mt_hour + 0.5
            if str(mt_hour)[-2:-1] == "." and str(mt_hour)[-1:] == "0":
                mt_hour_str, mt_hour_2 = str(mt_hour).split(".")
            else:
                mt_hour_str = str(mt_hour)
            url = f'https://aviationweather.gov/cgi-bin/data/metar.php?ids={location}&hours={mt_hour_str}&order=id%2C-obs&sep=true&taf=true'
            response = requests.get(url, timeout=7)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(200000):
                    file.write(chunk)
                file.close()
            if file_empty(f"MetarTaf_{file_name}"):
                return file_name
            if mt_hour == 12:
                get_eof = 1
        return ""

def file_empty(file_name):
    file_path = file_name + '.txt'
    if os.path.getsize(file_path) == 0:
        return False
    else:
        with open(file_path, 'r') as f:
            content = f.read()
            if not content.strip():
                return False
            else:
                return True
   
def get_blipmap():
    blip = 0
    url = 'http://blipmap.glider.jp/BLIPMAP/KANTO_JAPAN/FCST/sounding3.curr.1400lst.w2.png'
    try:
        response = requests.get(url, timeout = 10)
        # ステータスコードがエラーでないことを確認
        response.raise_for_status()
        file = open("blipmap.png","wb")
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()
        #pngファイルのpdf化
        image1 = Image.open('blipmap.png')
        im_pdf = image1.convert("RGB")
        im_pdf.save("blipmap.pdf")
        #pngファイルの削除
        os.remove('blipmap.png')
        blip = 1
        return blip
    except requests.exceptions.Timeout:
        blip = 0
        return blip

def append_pdf(fileName_MetarTaf, fileName, blip, metar_flg):
    merger = PdfWriter()
    for ix2 in range(len(fileName)):
        merger.append(fileName[ix2])
    if blip == 1:
        merger.append('blipmap.pdf')
    if metar_flg != 0:
        for ix10 in range(len(fileName_MetarTaf)):
            merger.append('MetarTaf_' + fileName_MetarTaf[ix10] + '.pdf')
    merger.write('wxファイル統合版_' + WX1M0000.nowdatetime + '.pdf')
    merger.close()

def removefiles(fileName_MetarTaf, fileName, blip, metar_flg):
    for ix3 in range(len(fileName)):       
        os.remove(fileName[ix3])
    if blip == 1:
        os.remove('blipmap.pdf')
    if metar_flg == 1:
        for ix10 in range(len(fileName_MetarTaf)):
            os.remove('MetarTaf_' + fileName_MetarTaf[ix10] + '.pdf')
            os.remove('MetarTaf_' + fileName_MetarTaf[ix10] + '.txt')

def get_DOC(currentDateTime: datetime):
    timeKbn = timeCheck(currentDateTime,3)
    url_tanki = 'https://www.data.jma.go.jp/fcd/yoho/data/jishin/kaisetsu_tanki_latest.pdf'
    response = requests.get(url_tanki, timeout = 10)
    file = open("短期予報解説資料.pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    url_shukan = 'https://www.data.jma.go.jp/fcd/yoho/data/jishin/kaisetsu_shukan_latest.pdf'
    response = requests.get(url_shukan, timeout = 10)
    file = open("週間天気予報解説資料.pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()

    #500hPa予報
    if timeKbn == 9:
        time_url = '00'
    else:
        time_url = '12'
    url_num = ["2","4","7"]
    for ix1 in range(3):
        url_fxfe = f'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/fxfe50{url_num[ix1]}_{time_url}.pdf'
        response = requests.get(url_fxfe, timeout = 10)
        file = open(f"fefx_{str(ix1)}.pdf","wb")
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()
    
    #200hPa
    url_tanki = f'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/aupa20_{time_url}.pdf'
    response = requests.get(url_tanki, timeout = 10)
    file = open("aupa20.pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()    

    merger = PdfWriter()
    merger.append("短期予報解説資料.pdf")
    merger.append("週間天気予報解説資料.pdf")
    for ix1 in range(3):
        merger.append(f"fefx_{str(ix1)}.pdf")
    merger.append("aupa20.pdf")

    merger.write('wx予報支援資料_' + WX1M0000.nowdatetime + '.pdf')
    merger.close()
    os.remove("短期予報解説資料.pdf")
    os.remove("週間天気予報解説資料.pdf")
    for ix1 in range(3):
        os.remove(f"fefx_{str(ix1)}.pdf")
    os.remove("aupa20.pdf")

def get_tanki(fileName):
    url_tanki = 'https://www.data.jma.go.jp/fcd/yoho/data/jishin/kaisetsu_tanki_latest.pdf'
    response = requests.get(url_tanki, timeout = 10)
    file = open("短期予報解説資料.pdf","wb")
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    fileName[6] = "短期予報解説資料.pdf"
    return fileName

def rotatePDF():
    reader = PdfReader('wxファイル統合版_' + WX1M0000.nowdatetime + '.pdf')
    writer = PdfWriter()
    rotation = 270
    page_number = [12,13]
    # 各ページを処理
    for i, page in enumerate(reader.pages):
        if i in page_number:
            # ページを回転
            page.rotate(rotation)
        writer.add_page(page)

    # 新しいPDFファイルに保存
    with open('wxファイル統合版_' + WX1M0000.nowdatetime + '.pdf', 'wb') as outfile:
        writer.write(outfile)