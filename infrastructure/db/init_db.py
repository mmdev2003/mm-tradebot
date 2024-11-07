import pandas as pd
from decimal import Decimal
from io import StringIO
from flask import Flask, jsonify, request, Response

import interface
import client

app = Flask('db_server')


@app.route("/db/get_account")
def get_account():
    account = interface.get_account().to_csv(index=False)
    return Response(account, mimetype="text/csv")


@app.route("/db/get_positions")
def get_positions():
    positions = interface.get_positions().to_csv(index=False)
    return Response(positions, mimetype="text/csv")


@app.route("/db/update_account", methods=['POST'])
def update_account():
    account_csv = StringIO(request.files['account_csv'].read().decode('utf-8'))
    account_data = request.form.to_dict()

    account = pd.read_csv(account_csv, index_col=0, dtype=str)

    account = interface.update_account(account, account_data).to_csv(index=False)
    return Response(account, mimetype="text/csv")


@app.route("/db/update_position", methods=['POST'])
def update_position():
    position_csv = StringIO(request.files['position_csv'].read().decode('utf-8'))
    position_data = request.form.to_dict()

    position = pd.read_csv(position_csv, index_col=0, dtype=str)

    position = interface.update_position(position, position_data).to_csv(index=False)
    return Response(position, mimetype="text/csv")


@app.route("/db/correct_account")
def correct_account():
    account_db = interface.get_account()

    balance = Decimal(client.get_account()['result']['list'][0]['coin'][0]['walletBalance'])
    balance_db = interface.get_value(account_db, 'balance')
    start_balance = interface.get_value(account_db, 'start_balance')

    profit_in_dollars_db = interface.get_value(account_db, 'total_profit_in_dollars')
    profit_in_percent_db = interface.get_value(account_db, 'total_profit_in_percent')

    profit_in_dollars = balance - start_balance
    profit_in_percent = profit_in_dollars / start_balance * Decimal('100')

    account_data = {
        "total_profit_in_dollars": -profit_in_dollars_db + profit_in_dollars,
        "total_profit_in_percent": -profit_in_percent_db + profit_in_percent,
        "balance": -balance_db + balance
    }

    account = interface.update_account(account_db, account_data)

    return jsonify({"status": 200})


@app.route("/db/reset_db")
def reset_db():
    try:
        interface.reset_db()
        return jsonify({"status": 200})
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import os
    current_directory = os.getcwd()
    print(f"Текущая директория: {current_directory}")

    app.run(port=5400)
