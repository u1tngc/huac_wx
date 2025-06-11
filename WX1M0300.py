#PGM-ID:WX1M0300
#PGM-NAME:WXメタタフ一括取得翻訳メイン

import datetime
import os
from pypdf import PdfWriter
import requests
import sys
import time
from flask import flash
import zoneinfo

import WX0S0200

class WX1M0300:
    jts = zoneinfo.ZoneInfo("Asia/Tokyo")
    now_datetime = datetime.datetime.now(jts)
    filename1 = now_datetime.strftime('%Y%m%d%H%M')

def get_and_transtale(inp_location,hour,shori_kbn):
    # metar取得
    if shori_kbn == 11:
        fileName_MetarTaf = get_MetarTaf(inp_location,hour,1)
    elif shori_kbn == 12: 
        fileName_MetarTaf = get_MetarTaf(inp_location,hour,2)
    else:
        fileName_MetarTaf = get_MetarTaf(inp_location,hour,shori_kbn)
    if fileName_MetarTaf == "":
        retCD = 1
        output = ""
    else:
        retCD = WX0S0200.translate_MetarTaf(fileName_MetarTaf, "")
        os.remove('MetarTaf_' + fileName_MetarTaf + '.txt')
        try:
            if shori_kbn == 1 or shori_kbn == 11:
                try:
                    os.rename("Metar.pdf",'METAR_' + fileName_MetarTaf + '.pdf')
                    output = 'METAR_' + fileName_MetarTaf + '.pdf'
                except FileExistsError:
                    os.rename("Metar.pdf",'METAR_' + fileName_MetarTaf + '_new.pdf')
                    output = 'METAR_' + fileName_MetarTaf + '_new.pdf'                    
            elif shori_kbn == 2:
                try:
                    os.rename("Taf.pdf",'TAF_' + fileName_MetarTaf + '.pdf')
                    output = 'TAF_' + fileName_MetarTaf + '.pdf'
                except FileExistsError:
                    os.rename("Taf.pdf",'TAF_' + fileName_MetarTaf + '_new.pdf')
                    output = 'TAF_' + fileName_MetarTaf + '_new.pdf' 
            elif shori_kbn == 12:
                merger = PdfWriter()
                merger.append('METAR_' + fileName_MetarTaf + '.pdf')
                merger.append('Taf.pdf')
                merger.write('METAR・TAF_' + fileName_MetarTaf + '.pdf')
                merger.close()
                output = 'METAR・TAF_' + fileName_MetarTaf + '.pdf'
                os.remove('METAR_' + fileName_MetarTaf + '.pdf')
                os.remove('Taf.pdf')
        except FileNotFoundError:
            pass
    return retCD, output

def get_MetarTaf(inp_location,inp_hour,shori_kbn):
    if shori_kbn == 1:
        url = f'https://aviationweather.gov/cgi-bin/data/metar.php?ids={inp_location}&hours={inp_hour}&order=id%2C-obs&sep=true'
    elif shori_kbn == 2:
        url = f'https://aviationweather.gov/api/data/taf?ids={inp_location}&format=raw&hours={inp_hour}&%20Server%20response'
    try:
        response = requests.get(url, timeout=7)
        file_name = inp_location + "_" + str(WX1M0300.filename1)
        file_path = f"MetarTaf_{file_name}.txt"
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(200000):
                file.write(chunk)
            file.close() 
        if file_empty(f"MetarTaf_{file_name}"):
            return file_name
        else:
            os.remove(f"MetarTaf_{file_name}.txt")
            return ""       
    except requests.exceptions.Timeout:
        #messagebox.showerror("エラー", "異常終了しました。\nネットワークが弱いです。")
        sys.exit()
    except requests.exceptions.ConnectionError:
        #messagebox.showerror("エラー", "異常終了しました。\nインターネットに接続されていません。")
        sys.exit()

# metar tafをtxtファイルから読み込む
def translate(fileName):
    retCD = WX0S0200.translate_MetarTaf(fileName, "")
    return retCD

def file_empty(file_path):
    if os.path.getsize(file_path + ".txt") == 0:
        return False
    else:
        with open(file_path + ".txt", 'r') as f:
            content = f.read()
            if not content.strip():
                return False
            else:
                return True

def main(selected_option ,inp_location, taishoTime):
    location = inp_location[1:5]
    taf_umu = inp_location[0:1]
    ck_retCd = check_input(selected_option, taf_umu, taishoTime)
    if ck_retCd == 0 or ck_retCd == 11:
        if selected_option == "0":
            if ck_retCd == 11:
                taishoTime = "7"
            retCD, output = get_and_transtale(location, taishoTime, 11)
            time.sleep(5)
            retCD, output = get_and_transtale(location, taishoTime, 12)
            time.sleep(1)
        elif selected_option == "1":
            shorikbn = 1
            retCD, output = get_and_transtale(location, taishoTime, shorikbn)
            time.sleep(1)
        elif selected_option == "2":
            if ck_retCd == 11:
                taishoTime = "7"
            shorikbn = 2
            retCD, output = get_and_transtale(location, taishoTime, shorikbn)
            time.sleep(1)
        if retCD == 0:
            flash(f"処理が通常終了しました\n出力ファイル：{output}")
            ck_retCd = 0
        elif retCD == 1:
            flash(f"MetarTafが取得できませんでした。\n過去{taishoTime}時間にMETARもしくはTAFが通報されていません。\n数字を大きくして再実行してください。")
            ck_retCd = 1
        return ck_retCd ,output
    else:
        if ck_retCd == 10:
            flash("対象時間に数字以外が入力されました。")
        elif ck_retCd == 12:
            flash("対象時間が未入力です。")
        elif ck_retCd == 13:
            flash("TAFの出力がない飛行場が選択されました。\n飛行場を再選択してください。")
    return ck_retCd ,output

def check_input(selected_option, taf_umu, hour):
    retcd = 0
    try:
        dummy = int(hour)
    except ValueError:
        retcd = 10
    if retcd == 0:
        if hour == "" or hour is None:
            retcd = 12
        elif selected_option == "2" or selected_option == "0":
            if taf_umu != "●":
                retcd = 13
        elif int(hour) < 6:
            retcd = 11
    return retcd
