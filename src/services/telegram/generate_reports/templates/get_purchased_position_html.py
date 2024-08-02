from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN

def get_purchased_position_html(position_data):
    
    symbol = position_data['symbol']
    open_price = Decimal(position_data['open_price']).normalize()
    size = position_data['size']
    leverage = position_data['leverage']
    position_side = position_data['position_side']
    
    stop_in_percent = Decimal(position_data['stop_in_percent']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    stop_price = Decimal(position_data['stop_price']).normalize()
  
    take_in_percent = Decimal(position_data['take_in_percent']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    take_price = Decimal(position_data['take_price']).normalize()
    
    open_time = str(datetime.now())[:-7]
    
    position_sum = (Decimal(size) * Decimal(open_price) / Decimal(leverage)).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_profit_in_percent = Decimal(position_data['potential_profit_in_percent']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_profit_in_dollars = Decimal(position_data['potential_profit_in_dollars']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_profit_in_percent_from_account = Decimal(position_data['potential_profit_in_percent_from_account']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_loss_in_percent = Decimal(position_data['potential_loss_in_percent']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_loss_in_dollars = Decimal(position_data['potential_loss_in_dollars']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    potential_loss_in_percent_from_account = Decimal(position_data['potential_loss_in_percent_from_account']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    prev_balance = Decimal(position_data['prev_balance']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
    current_balance = Decimal(position_data['current_balance']).quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN).normalize()
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
        >ДОБРАЛИ ПОЗИЦИЮ</h1>
    </header>
    <div
    style="
    width: 1030px;
    border-radius: 30px;
    background-image: linear-gradient(to bottom, rgba(61, 56, 78, 1), rgba(60, 56, 77, 0.58));
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 70px;
    padding: 60px 70px;
    
    font-family: 'KoHo', sans-serif;
    "
    >
        <h2
        style="
        background-image: linear-gradient(to right, rgba(240, 71, 63, 1), rgba(240, 170, 98, 1));
        font-size: 90px;
        background-clip: text;
        color: transparent;
        display: inline-block;
        -webkit-background-clip: text;
        line-height: 90px;
        font-weight: 700;
        font-family: 'KoHo', sans-serif;
        "
        >{symbol}</h2>
        
        <h3
        style="
        font-size: 42px;
        line-height: 42px;
        color: white;
        margin-top: 10px;
        "
        >{position_side}</h3>
        <div
        style="
        display: flex;
        width: 100%;
        align-items: start;
        flex-direction: column;
        margin-top: 70px;
        "
        >
            <h4
            style="
            margin-bottom: 8px;
            font-size: 30px;
            color: white;
            opacity: 0.5;
            "
            >Цена открытия</h4>
            <span
            style="
            font-size: 42px;
            margin-top: 6px;
            color: white;
            font-weight: 600;
            "
            >{open_price}$</span>
            
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 70px;
        "
        >
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(120, 219, 124, 1);
                "
                >Take</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{take_price}$ / {take_in_percent}%</span>
            </div>
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(223, 91, 91, 1);
                "
                >Stop</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{stop_price}$ / {stop_in_percent}%</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 100%;
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
                >Количество</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{size} {symbol}</span>
            </div>
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Плечо</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{leverage}</span>
            </div>
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Сумма позиции</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{position_sum}$</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 70px;
        "
        >
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(120, 219, 124, 1);
                "
                >Потенциальная прибыль</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{potential_profit_in_dollars}$ / {potential_profit_in_percent}%</span>
            </div>
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: rgba(223, 91, 91, 1);
                "
                >Потенциальный убыток</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{potential_loss_in_dollars}$ / {potential_loss_in_percent}%</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 100%;
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
                >Потенциальная прибыль/убыток аккаунта</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{potential_profit_in_percent_from_account}% / {potential_loss_in_percent_from_account}%</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        width: 100%;
        margin-top: 70px;
        "
        >
            <div
            style="
            margin-right: 100px;
            "
            >
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Прошлый баланс</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{prev_balance}$</span>
            </div>
            <div>
                <h4
                style="
                margin-bottom: 8px;
                font-size: 30px;
                color: white;
                opacity: 0.5;
                "
                >Текущий баланс</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{current_balance}$</span>
            </div>
        </div>
        <div
        style="
        display: flex;
        justify-content: space-between;
        width: 100%;
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
                >Время</h4>
                <span
                style="
                font-size: 42px;
                color: white;
                "
                >{open_time}</span>
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