#PGM-ID:WX1S0012
#PGM-NAME:WX[定時]教証資料取得

import datetime
import os
from PIL import Image
import requests

def get_kyosho(timeKbn, currentDateTime, fileName, path):
    fileName = get_kyosho_asas(timeKbn, currentDateTime, fileName, path)
    fileName = get_kyosho_kousou(timeKbn, currentDateTime, fileName, path)
    return fileName

def get_kyosho_kousou(timeKbn, currentDate, fileName, path):
    currentDateTime = currentDate
    currentYYYY = str(currentDate.year)
    currentMM  = str(currentDate.strftime("%m"))
    currentDD  = str(currentDate.strftime("%d"))
    if timeKbn == 21:
        for ix1 in range(3):
            delta = datetime.timedelta(days=-1)
            currentDate = currentDate + delta
            currentYYYY = str(currentDate.year)
            currentMM  = str(currentDate.strftime("%m"))
            currentDD  = str(currentDate.strftime("%d"))
            url_78_1 = 'https://weather.kakutyoutakaki.com/tenkizu/'
            url_78_2 = currentYYYY + currentMM + currentDD
            url_78_3 = '/aupq78_12.pdf'
            url_35_3 = '/aupq35_12.pdf'
            url_78 = url_78_1 + url_78_2 + url_78_3
            url_35 = url_78_1 + url_78_2 + url_35_3
            response = requests.get(url_78)
            file = open(path + "/" + "高層天気図(850・700)_" + str(3 - ix1) + ".pdf","wb")
            fileName[8 - ix1] = "高層天気図(850・700)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            response = requests.get(url_35)
            file = open(path + "/" + "高層天気図(500・300)_" + str(3 - ix1) + ".pdf","wb")
            fileName[11 - ix1] = "高層天気図(500・300)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
    elif timeKbn == 9:
        for ix1 in range(3):
            url_78_1 = 'https://weather.kakutyoutakaki.com/tenkizu/'
            url_78_2 = currentYYYY + currentMM + currentDD
            url_78_3 = '/aupq78_00.pdf'
            url_35_3 = '/aupq35_00.pdf'
            url_78 = url_78_1 + url_78_2 + url_78_3
            url_35 = url_78_1 + url_78_2 + url_35_3
            response = requests.get(url_78)
            file = open(path + "/" + "高層天気図(850・700)_" + str(3 - ix1) + ".pdf","wb")
            fileName[8 - ix1] = "高層天気図(850・700)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            response = requests.get(url_35)
            file = open(path + "/" + "高層天気図(500・300)_" + str(3 - ix1) + ".pdf","wb")
            fileName[11 - ix1] =  "高層天気図(500・300)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            delta = datetime.timedelta(days=-1)
            currentDate = currentDate + delta
            currentYYYY = str(currentDate.year)
            currentMM  = str(currentDate.strftime("%m"))
            currentDD  = str(currentDate.strftime("%d"))
    elif timeKbn == 90:
        delta = datetime.timedelta(days=-1)
        currentDate = currentDate + delta
        currentYYYY = str(currentDate.year)
        currentMM  = str(currentDate.strftime("%m"))
        currentDD  = str(currentDate.strftime("%d"))
        for ix1 in range(3):
            url_78_1 = 'https://weather.kakutyoutakaki.com/tenkizu/'
            url_78_2 = currentYYYY + currentMM + currentDD
            url_78_3 = '/aupq78_12.pdf'
            url_35_3 = '/aupq35_12.pdf'
            url_78 = url_78_1 + url_78_2 + url_78_3
            url_35 = url_78_1 + url_78_2 + url_35_3
            response = requests.get(url_78)
            file = open(path + "/" + "高層天気図(850・700)_" + str(3 - ix1) + ".pdf","wb")
            fileName[8 - ix1] = "高層天気図(850・700)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            response = requests.get(url_35)
            file = open(path + "/" + "高層天気図(500・300)_" + str(3 - ix1) + ".pdf","wb")
            fileName[11 - ix1] = "高層天気図(500・300)_" + str(3 - ix1) + ".pdf"
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            delta = datetime.timedelta(days=-1)
            currentDate = currentDate + delta
            currentYYYY = str(currentDate.year)
            currentMM  = str(currentDate.strftime("%m"))
            currentDD  = str(currentDate.strftime("%d"))
    
    currentDate = currentDateTime
    delta = datetime.timedelta(days=-1)
    currentDate = currentDate + delta
    currentHH = int(currentDate.hour)
    if currentHH < 1:
        currentDate = currentDate + delta
    currentYYYY = str(currentDate.year)
    currentMM = str(currentDate.strftime("%m"))
    currentDD = str(currentDate.strftime("%d"))
    eof_flg = 0
    hh_num = 0
    mm_num = 30
    while eof_flg <= 1:
        try:
            hh = f'{hh_num:02}'
            mm = f'{mm_num:02}'
            hhmm = hh + mm
            url1 = 'https://www.sunny-spot.net/chart/data/AUXN50/'
            url2 = currentYYYY + '/' + currentMM + '/AUXN50_'
            url3 = currentYYYY + currentMM + currentDD + hhmm + '.pdf'
            url_50 = url1 + url2 + url3
            response = requests.get(url_50)
            response.raise_for_status()
            file = open(path + "/" + "高層天気図(北半球500)_" + str(2 - eof_flg) + ".pdf","wb")
            fileName[13 - eof_flg] = "高層天気図(北半球500)_" + str(2 - eof_flg) + ".pdf"
            eof_flg += 1
            for chunk in response.iter_content(200000):
                file.write(chunk)    
            file.close()
            delta = datetime.timedelta(days=-1)
            currentDate = currentDate + delta
            currentYYYY = str(currentDate.year)
            currentMM  = str(currentDate.strftime("%m"))
            currentDD  = str(currentDate.strftime("%d"))
            hh_num = 0
            mm_num = 30
        except requests.exceptions.HTTPError:
            if mm_num == 58:
                mm_num = 0
                hh_num += 1
            else:
                mm_num += 2

    url_50 = 'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/auxn50_12.pdf'
    response = requests.get(url_50)
    file = open(path + "/" + "高層天気図(北半球500)_3.pdf","wb")
    fileName[14] = "高層天気図(北半球500)_3.pdf"
    for chunk in response.iter_content(200000):
        file.write(chunk)    
    file.close()
    return fileName

def get_kyosho_asas(timeKbn, currentDate, fileName, path):
    try:
        url_asas_1 = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/'
        url_asas_3 = '/ASAS_COLOR_'
        if timeKbn == 21:
            url_pdf = '1200.pdf'
            delta = datetime.timedelta(days=-1)
            currentDate = currentDate + delta
            currentYYYY = str(currentDate.year)
            currentMM  = str(currentDate.strftime("%m"))
            currentDD  = str(currentDate.strftime("%d"))
            for ix1 in range(2):
                delta = datetime.timedelta(days=-1)
                currentDate = currentDate + delta
                currentYYYY = str(currentDate.year)
                currentMM  = str(currentDate.strftime("%m"))
                currentDD  = str(currentDate.strftime("%d"))
                url_asas_2 = currentYYYY + currentMM
                url_asas_4 = currentYYYY + currentMM + currentDD
                url_asas = url_asas_1 + url_asas_2 + url_asas_3 + url_asas_4 + url_pdf
                response = requests.get(url_asas, timeout = 10)
                file = open(path + "/" + "地上天気図_" + str(2 - ix1) + ".pdf","wb")
                fileName[1 - ix1] = "地上天気図_" + str(2 - ix1) + ".pdf"
                for chunk in response.iter_content(200000):
                    file.write(chunk)    
                file.close()
        elif timeKbn == 9:
            url_pdf = '0000.pdf'
            for ix1 in range(2):
                delta = datetime.timedelta(days=-1)
                currentDate = currentDate + delta
                currentYYYY = str(currentDate.year)
                currentMM  = str(currentDate.strftime("%m"))
                currentDD  = str(currentDate.strftime("%d"))
                url_asas_2 = currentYYYY + currentMM
                url_asas_4 = currentYYYY + currentMM + currentDD
                url_asas = url_asas_1 + url_asas_2 + url_asas_3 + url_asas_4 + url_pdf
                response = requests.get(url_asas, timeout = 10)
                file = open(path + "/" + "地上天気図_" + str(2 - ix1) + ".pdf","wb")
                fileName[1 - ix1] = "地上天気図_" + str(2 - ix1) + ".pdf"
                for chunk in response.iter_content(200000):
                    file.write(chunk)    
                file.close()
        url_asas = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/ASAS_COLOR.pdf'
        response = requests.get(url_asas, timeout = 10)
        file = open(path + "/" + "地上天気図_3.pdf","wb")
        fileName[2] = "地上天気図_3.pdf"
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()

        url_asas = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/FSAS24_COLOR_ASIA.pdf'
        response = requests.get(url_asas, timeout = 10)
        file = open(path + "/" + "予報天気図_1.pdf","wb")
        fileName[3] = "予報天気図_1.pdf"
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()

        url_asas = 'https://www.data.jma.go.jp/fcd/yoho/data/wxchart/quick/FSAS48_COLOR_ASIA.pdf'
        response = requests.get(url_asas, timeout = 10)
        file = open(path + "/" + "予報天気図_2.pdf","wb")
        fileName[4] = "予報天気図_2.pdf"
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()

        url = 'https://www.jma.go.jp/bosai/numericmap/data/nwpmap/fefe19.png'
        response = requests.get(url, timeout = 10)
        file = open(path + "/" + "fefe19.png","wb")
        fileName[5] = "fefe19.pdf"
        for chunk in response.iter_content(200000):
            file.write(chunk)    
        file.close()
        #pngファイルのpdf化
        image1 = Image.open(path + "/" + 'fefe19.png')
        im_pdf = image1.convert("RGB")
        im_pdf.save(path + "/" + "fefe19.pdf")
        #pngファイルの削除
        os.remove(path + "/" + 'fefe19.png')
        return fileName
    except requests.exceptions.Timeout as e:
        raise e
    except requests.exceptions.ConnectionError as e:
        raise e
    

