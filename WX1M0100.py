#PGM-ID:WX1M0100
#PGM-NAME:WX天気概要取得メイン

import os

import WX0S0100


def main(input,kinocd):
    err = ""
    if kinocd == 1:
        post,err = inp_check(input,1)
        if err != "":
            return err
        try:
            html_name = WX0S0100.getWx("2",post, "", "")
        except KeyError:
            err = "エラー：存在しない郵便番号です。"
    if kinocd == 2:
        try:
            html_name = WX0S0100.getWx("3",input, "", "")
        except KeyError:
            err = "エラー：都市名が不正です。"
    return err


def inp_check(input,kinocd):
    err_flg = 0
    err = ""
    ret = ""
    if kinocd == 1:
        if input[3:4] == "-":
            post_chk = input.split("-")
            try:
                dummy = int(post_chk[0])
                dummy = int(post_chk[1])
            except ValueError:
                err_flg = 1
            if len(input) != 8:
                err_flg = 1
            if err_flg == 0:
                ret = f"{input},JP"
        else:
            try:
                dummy = int(input)
            except ValueError:
                err_flg = 1
            if len(input) != 7:
                err_flg = 1
            if err_flg == 0:
                ret = f"{input[0:3]}-{input[3:7]},JP"
    if err_flg == 1:
        err = "エラー：郵便番号が不正です。"
    return ret, err


    

