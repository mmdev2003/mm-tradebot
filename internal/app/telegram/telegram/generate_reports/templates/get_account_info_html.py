import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))

from src.services.database import db
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_UP
def get_account_info_html():
    account = db.get_account()
    count_closed_positions = db.get_value(account, 'count_closed_positions')
    count_active_positions = db.get_value(account, 'count_active_positions')
    count_profit_positions = db.get_value(account, 'count_profit_positions')
    count_loss_positions = db.get_value(account, 'count_loss_positions')
    total_profit_in_percent = db.get_value(account, 'total_profit_in_percent').quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN)
    total_profit_in_dollars = db.get_value(account, 'total_profit_in_dollars').quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN)
    balance = db.get_value(account, 'balance').quantize(Decimal('0.001'), rounding=ROUND_UP)
    start_balance = db.get_value(account, 'start_balance').quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN)
    
    html = f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&family=KoHo:wght@700&display=swap" rel="stylesheet">
    <style type="text/css" media="all">
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
main, menu, nav, output, ruby, section, summary,
time, mark, audio, video {{
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
	box-sizing: border-box;
	font-weight: 600;
	font-family: 'Inter', sans-serif;
}}
article, aside, details, figcaption, figure,
footer, header, hgroup, main, menu, nav, section {{
	display: block;
}}
*[hidden] {{
    display: none;
}}
body {{
	line-height: 1;
}}
menu, ol, ul {{
	list-style: none;
}}
    </style>
</head>
<body
    style="
    background-color: #1D192D;
    width: 1200px;
    padding: 0px;
    display: flex;
    margin: 0;
    align-items: center;
    flex-direction: column
    "
>
    <header
        style="
        margin-top: 0;
        "
    >
        <h1
        style="
        color: #FFFFFF;
        font-size: 36px;
        margin-top: 70px;
        "
        >ИНФОРМАЦИЯ ОБ АККАУНТЕ</h1>
    </header>
    <div
    style="
    width: 1030px;
    border-radius: 30px;
    background-image: linear-gradient(to bottom, rgba(61, 56, 78, 1), rgba(60, 56, 77, 0.58));
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: left;
    margin-top: 70px;
    padding: 60px 70px;
    
    font-family: 'KoHo', sans-serif;
    "
    >
        <h2
        style="
        font-size: 42px;
        color: white;
        "
        >Текущий баланс</h2>
        <span
        style="
        background-image: linear-gradient(to right, rgba(240, 71, 63, 1), rgba(240, 170, 98, 1));
        font-size: 90px;
        background-clip: text;
        color: transparent;
        display: inline-block;
        -webkit-background-clip: text;
        margin-top: 10px;
        font-weight: 700;
        font-family: 'KoHo', sans-serif;
        "
        >{balance}$</span>
        <div
        style="
        display: flex;
        flex-direction: column;
        align-self: flex-start;
        margin-top: 20px;
        "
        >
            <h4
            style="
            margin-bottom: 8px;
            font-size: 30px;
            color: white;
            opacity: 0.5;
            "
            >
                Стартовый баланс
            </h4>
            <span
            style="
            color: rgba(255, 255, 255, 1);
            font-size: 42px
            "
            >
                {start_balance}$
            </span>
        </div>
        <div
        style="
        display: flex;
        width: 80%;
        margin-top: 70px;
        justify-content: space-between;
        "
        >
            <div
            style="
            width: 450px;
            "
            >
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Количество закрытых позиций</h4>
                <span
                style="
                font-size: 42px;
                margin-top: 6px;
                color: white;
                font-weight: 600;
                "
                >{count_closed_positions}</span>
            </div>
            <div
            style="
            width: 450px;
            "
            >
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Количество открытых позиций</h4>
                <span
                style="
                font-size: 42px;
                margin-top: 6px;
                color: white;
                font-weight: 600;
                "
                >{count_active_positions}</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 80%;
        margin-top: 70px;
        "
        >
            <div
            style="
            width: 450px;
            "
            >
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(120, 219, 124, 1);
                "
                >Количество прибыльных сделок</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{count_profit_positions}</span>
            </div>
            <div 
            style="
            width: 450px;
            "
            >
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(223, 91, 91, 1);
                "
                >Количество убыточных сделок</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{count_loss_positions}</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        width: 70%;
        align-self: flex-start;
        justify-content: space-between;
        margin-top: 70px;
        "
        >
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Общая прибыль со сделок</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{total_profit_in_dollars}$ / {total_profit_in_percent}%</span>
            </div>
        </div>
    </div>
    <div
    style="
    width: 1030px;
    margin-top: 40px;
    margin-bottom: 40px;
    display: flex;
    justify-content: space-between;
    "
    >
    <img src="/root/mm-tradebot/telegram/generate_reports/img/logo.svg" alt="">
    <img src="/root/mm-tradebot/telegram/generate_reports/img/qr.svg" alt="">
    </div>
</body>
</html>
    """
    return html