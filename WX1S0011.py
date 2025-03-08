#PGM-ID:WX1S0011
#PGM-NAME:WX[定時]天気概況変換

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import json
import shutil

def convertToPdf(filename1,filename2, path):

    # 保存対象URL一覧取得
    html_path = path + '/' + filename1
    url = f"file:///{html_path}"

    # Chrome の印刷機能でPDFとして保存
    options = webdriver.ChromeOptions()

    # PDF印刷設定
    appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "pageSize": 'A4',
        "marginsType": 2,
        "scalingType": 3,  # 0：デフォルト 1：ページに合わせる 2：用紙に合わせる 3：カスタム
        "scaling": "90",  # 倍率
        "isLandscapeEnabled": True,  # 横向きに設定
        "isCssBackgroundEnabled": True  # 背景グラフィックをオンに設定
    }
    # ドライバへのPDF印刷設定の適用
    options.add_experimental_option("prefs", {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        "download.default_directory": "C:/Users/tanig/Downloads"  # 保存先をデスクトップに変更
    })
    options.add_argument('--kiosk-printing')

    """
    # Serviceオブジェクトの作成
    service = Service(ChromeDriverManager().install())
    """
    webdriver_path = ChromeDriverManager().install()
    if os.path.splitext(webdriver_path)[1] != '.exe':
        webdriver_dir_path = os.path.dirname(webdriver_path)
        webdriver_path = os.path.join(webdriver_dir_path, 'chromedriver.exe')
    chrome_service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    with webdriver.Chrome(service=chrome_service, options=options) as driver:
        # 任意のHTMLの要素が特定の状態になるまで待つ
        wait = WebDriverWait(driver, 15)
        driver.implicitly_wait(10)
        driver.get(url)
        # ページ上のすべての要素が読み込まれるまで待機
        wait.until(EC.presence_of_all_elements_located)
        # PDFとして印刷
        driver.execute_script('window.print()')
        # 待機
        time.sleep(10)
    current_path = 'C:/Users/tanig/OneDrive/法政教育証明/09_谷口ツール/wx資料バックナンバー'
    shutil.move("C:/Users/tanig/Downloads/気象概況.pdf", current_path + "/" + filename2 + "_気象概況.pdf")

    return filename2 + "_気象概況"

