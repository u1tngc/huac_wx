#PGM-ID:WK0S0301
#PGM-NAME:[P]気象ユーザー認証・DB読込み

import datetime
#import mysql.connector

"""
ret_cd 11:認証 12:パスエラー 13:登録なし 14:有効期限切れ
"""
def user_admin(input_user, input_pass,kino_code):
    ret_cd = 0

    #ここから暫定処理
    today_date = datetime.date.today()
    limit_date = datetime.date(2025, 3, 31)
    if input_user == "kyosho" and input_pass == "honda":
        if limit_date < today_date:
            return 14
        else:
            return 11
    elif input_user != "kyosho":
        return 13
    elif input_pass != "honda":
        return 12


