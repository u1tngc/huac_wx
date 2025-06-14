#PGM-ID:WX0L0000
#PGM-NAME:WXウェブメイン

from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
import io
import zipfile
import glob

import WL1M0000
#import WX1M0100
import WL1M0200
import WL1M0300


# ユーザー情報の定義（ユーザー名とパスワード）
app = Flask(__name__)
app.secret_key = os.urandom(24)  # 毎回ランダムなキーを生成
USER_DATA = {
    'password': '245422kz'
}

# ログインページの表示
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == USER_DATA['password']:
            session['logged_in'] = True
            for file_path in glob.glob("*.pdf"):
                os.remove(file_path)
            for file_path in glob.glob("templates/天気概況*.html"):
                os.remove(file_path)
            return redirect(url_for('menu'))
        else:
            return 'ログイン失敗。ユーザー名またはパスワードが違います。'
    return render_template('login.html')

# メニュー画面の表示
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        selection = request.form['selection']
        if selection == 'wx':
            return redirect(url_for('get_wx'))
        elif selection == 'gaikyo':
            return redirect(url_for('get_gaikyo'))
        elif selection == 'metartaf':
            return redirect(url_for('get_metartaf'))
        elif selection == 'metartafs':
            return redirect(url_for('get_metartafs'))
    return render_template('menu.html')

# WX資料取得
@app.route('/get_wx',methods=['GET', 'POST'])
def get_wx():
    html_path = ""
    ret_path = ""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        location = request.form['airport']
        shorikbn = request.form['purpose']
        fileNames, err_msg = WL1M0000.kyotsu_shori(shorikbn ,location[0:4])
        #fileNames, err_msg,html_name = WX1M0000.kyotsu_shori(shorikbn ,location[0:4])
        if shorikbn == "1":
            return send_file(f"{fileNames[0]}", as_attachment=True, download_name=fileNames[0])
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for ix1 in range(2):
                    file_path = f"{fileNames[ix1]}"
                    zipf.write(file_path, arcname=fileNames[ix1])
            zip_buffer.seek(0)
            if err_msg == "":
                return send_file(zip_buffer, as_attachment=True, download_name='wx資料.zip')
        if err_msg == "":
            return render_template('get_wx.html',err_msg=err_msg)
        #else:
        #    return render_template('天気概況.html')
    return render_template('get_wx.html')
""""
# 概況取得
@app.route('/get_gaikyo',methods=['GET', 'POST'])
def get_gaikyo():
    try:
        os.remove("天気概況.html")
    except FileNotFoundError:
        pass
    err = ""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        postNo = request.form['postNo']
        city = request.form['city']
        print(f"{postNo},{city}",flush=True)
        if postNo != "" and city != "":
            err = "エラー：郵便番号か都市名の片方を入力してください。"
        elif postNo == "" and city == "":
                postNo = "360-0222"
                err = WX1M0100.main(postNo,1)
                out = postNo
        elif postNo != "":
            err = WX1M0100.main(postNo,1)
            out = postNo
        elif city != "":
            err = WX1M0100.main(city,2)
            out = city
        if err == "":
            os.rename('天気概況.html',f"天気概況_{out}.html")
            return render_template(f"天気概況_{out}.html")
    return render_template('get_gaikyo.html',err=err)
"""

# METARTAF取得翻訳
@app.route('/get_metartaf',methods=['GET', 'POST'])
def get_metartaf():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        location = request.form['airport']
        shorikbn = request.form['processType']
        metar = request.form['metar']
        taf = request.form['taf']
        fileName,err_msg = WL1M0200.main(shorikbn ,location,metar,taf)
        if err_msg == 0:
            return send_file(f"{fileName}", as_attachment=True, download_name=fileName)
        else:
            return render_template(fileName, err_msg=err_msg)
    return render_template('get_metartaf.html')

# METARTAF一括取得翻訳
@app.route('/get_metartafs',methods=['GET', 'POST'])
def get_metartafs():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        location = request.form.get('airport')
        shorikbn = request.form.get('dataType')
        taishoTime = request.form.get('time')
        if shorikbn is None:
            flash("データ種類を選択してください。")
        else:
            ret_cd,fileName = WL1M0300.main(shorikbn ,location[0:5], taishoTime)
            if ret_cd == 0:
                return send_file(f"{fileName}", as_attachment=True, download_name=fileName)
    return render_template('get_metartafs.html')

"""
#概況
@app.route('/gaikyo',methods=['GET', 'POST'])
def gaikyo():
    file_umu = 0
    err = "エラー：実行してから概況取得してください。"
    fileName = "天気概況*.html"
    files = glob.glob(fileName)
    if files:
        file_umu = file_umu + 1
    if file_umu != 0:
        err = ""
        return render_template('天気概況.html')
    else:
        return render_template('get_wx.html',err=err)
"""
    
# ログアウト
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)