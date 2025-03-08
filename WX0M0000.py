import streamlit as st
import WX1M0000


# セッションステートを使ってログイン状態を管理
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ログイン画面
if not st.session_state.logged_in:
    st.title("ログイン")

    # ユーザー名とパスワード入力
    password = st.text_input("パスワードを入力してください。", type="password")

    if st.button("ログイン"):
        password_correct = st.secrets["general"]["open_pass"]
        if password == password_correct:
            st.session_state.logged_in = True  # ログイン成功
            st.rerun()  # 画面を更新してメイン画面へ
        else:
            st.error("パスワードが違います")

if st.session_state.logged_in:
    # 空港リスト
    airportList = [
        "なし",
        "RJAA:成田国際空港",
        "RJBB:関西国際空港",
        "RJCC:新千歳空港",
        "RJOO:大阪国際空港(伊丹空港)",
        "RJTT:東京国際空港(羽田空港)",
        "RJAH:百里飛行場(茨城空港)",
        "RJAF:松本空港",
        "RJBD:南紀白浜空港",
        "RJBE:神戸空港",
        "RJBT:但馬空港",
        "OEJN:キング・アブドゥルアズィール国際空港(Saudi Arabia)",
        "OEMA:プリンス・モハンマド・ビン・アブドゥルアズィーズ国際空港(Saudi Arabia)",
        "OPIS:イスラマバード国際空港(Pakistan)",
        "OPKC:ジンナー国際空港(Pakistan)",
        "OPLA:アッラーマ・イクバール国際空港(Pakistan)",
        "OPPS:バシャ・カーン国際空港(Pakistan)",
        "VIDP:インディラ・ガンディー国際空港(India)",
        "WSSS:チャンギ国際空港(Singapore)",
        "RJCH:函館空港",
        "RJCK:釧路空港",
        "RJCM:女満別空港",
        "RJCO:丘珠空港",
        "RJEB:紋別空港",
        "RJEC:旭川空港",
        "RJFC:屋久島空港",
        "RJFE:福江空港",
        "RJFF:福岡空港",
        "RJFG:種子島空港",
        "RJFK:鹿児島空港",
        "RJFM:宮崎空港",
        "RJFO:大分空港",
        "RJFR:北九州空港",
        "RJFS:佐賀空港",
        "RJFT:熊本空港",
        "RJFU:長崎空港",
        "RJGG:中部国際空港(セントレア)",
        "RJKA:奄美空港",
        "RJNG:岐阜飛行場",
        "RJNK:小松空港",
        "RJNS:静岡空港",
        "RJNT:富山空港",
        "RJNY:静浜飛行場",
        "RJOA:広島空港",
        "RJOB:岡山空港",
        "RJOC:出雲空港",
        "RJOH:美保飛行場(米子空港)",
        "RJOI:岩国空港(米軍)",
        "RJOK:高知空港",
        "RJOM:松山空港",
        "RJOR:鳥取空港",
        "RJOS:徳島空港",
        "RJOT:高松空港",
        "RJOW:山口宇部空港",
        "RJOW:石見空港",
        "RJOY:八尾飛行場",
        "RJSA:青森空港",
        "RJSC:山形空港",
        "RJSF:福島空港",
        "RJSH:八戸航空基地",
        "RJSI:花巻空港",
        "RJSM:三沢飛行場",
        "RJSN:新潟空港",
        "RJSS:仙台空港",
        "RJSY:庄内空港",
        "RJTF:調布飛行場",
        "RJTI:東京ヘリポート",
        "ROAH:那覇空港",
        "RODN:嘉手納飛行場(米軍)",
        "ROIG:新石垣空港",
        "ROMD:南大東空港",
        "RORK:北大東空港",
        "RORS:下地島空港",
        "ROTM:普天間飛行場(米軍)",
        "ROYN:与那国空港",
        "EGLL:ヒースロー空港(United Kingdom)",
        "LTBA:アタテュルク国際空港(Turkey)",
        "OERK:キング・ハーリド国際空港(Saudi Arabia)",
        "OIFM:シャヒード・ベヘシュティー国際空港(Iran)",
        "OIIE:エマーム・ホメイニー国際空港(Iran)",
        "OMDB:ドバイ国際空港(U.A.E.)",
        "RKSI:仁川国際空港(Korea)",
        "RKSS:金浦国際空港(Korea)",
        "VABB:チャトラパティ・シヴァージー国際空港(India)",
        "VTBS:スワンナプーム国際空港(Thailand)",
        "VTCC:チェンマイ国際空港(Thailand)",
        "WIII:スカルノ・ハッタ国際空港(Indonesia)",
        "WMKJ:スルタン・イスマイル空港(Malaysia)",
        "WMKK:クアラルンプール国際空港(Malaysia)"
    ]

    st.title('法政航空部気象ツール')

    # 処理区分選択
    shori_kbn = st.radio('処理区分を選択してください。', ['自家用', '教証'])

    # 空港選択
    airport = st.selectbox("使用するMETAR/TAFの地点略号を選択してください。", airportList)
    if airport == "なし":
        mt_location = ""
    else:
        mt_location = airport[0:4]

    # セッションステートで処理結果を管理
    if "result" not in st.session_state:
        st.session_state.result = None
        st.session_state.fileName = None

    if st.button("OK"):
        msg, fileName = WX1M0000.main(shori_kbn, mt_location)
        st.session_state.result = msg
        st.session_state.fileName = fileName

    if st.session_state.result is not None:
        if st.session_state.fileName is not None:
            if shori_kbn == '自家用':
                with open(st.session_state.fileName[0], 'rb') as file:
                    pdf_data = file.read()
                    st.download_button(
                        label="ダウンロード",
                        data=pdf_data,
                        file_name=st.session_state.fileName[0],
                        mime='application/pdf',
                    )
            elif shori_kbn == "教証":
                with open(st.session_state.fileName[0], 'rb') as file:
                    pdf_data = file.read()
                    st.download_button(
                        label="ダウンロード[ファイル統合版]",
                        data=pdf_data,
                        file_name=st.session_state.fileName[0],
                        mime='application/pdf',
                    )
                with open(st.session_state.fileName[1], 'rb') as file:
                    pdf_data = file.read()
                    st.download_button(
                        label="ダウンロード[予報支援資料]",
                        data=pdf_data,
                        file_name=st.session_state.fileName[1],
                        mime='application/pdf',
                    )

        if st.session_state.result == "":
            st.success("処理が完了しました。ダウンロードボタンから資料を取得してください")
        else:
            st.error(st.session_state.result)
