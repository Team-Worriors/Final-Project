from interactive_trader.ibkr_app import ibkr_app
import threading
import time
from datetime import datetime
import pandas as pd
import numpy as np

# If you want different default values, configure it here.
default_hostname = '127.0.0.1'
default_port = 7497
default_client_id = 10645  # can set and use your Master Client ID
timeout_sec = 5


def fetch_managed_accounts(hostname=default_hostname, port=default_port,
                           client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))

    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_managed_accounts",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    while app.next_valid_id is None:
        time.sleep(0.01)
    app.disconnect()
    return app.managed_accounts


def fetch_current_time(hostname=default_hostname,
                       port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "next_valid_id not received"
            )

    app.reqCurrentTime()
    start_time = datetime.now()
    while app.current_time is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "current_time not received"
            )
    app.disconnect()
    return app.current_time


def fetch_historical_data(contract, endDateTime='', durationStr='30 D',
                          barSizeSetting='1 hour', whatToShow='MIDPOINT',
                          useRTH=True, hostname=default_hostname,
                          port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
    if (datetime.now() - start_time).seconds > timeout_sec:
        app.disconnect()
        raise Exception(
            "fetch_historical_data",
            "timeout",
            "couldn't connect to IBKR"
        )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_historical_data",
                "timeout",
                "next_valid_id not received"
            )
    tickerId = app.next_valid_id
    app.reqHistoricalData(
        tickerId, contract, endDateTime, durationStr, barSizeSetting,
        whatToShow, useRTH, formatDate=1, keepUpToDate=False, chartOptions=[])
    start_time = datetime.now()
    while app.historical_data_end != tickerId:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_historical_data",
                "timeout",
                "historical_data not received"
            )
    app.disconnect()
    return app.historical_data


def fetch_contract_details(contract, hostname=default_hostname,
                           port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "next_valid_id not received"
            )

    tickerId = app.next_valid_id
    app.reqContractDetails(tickerId, contract)

    start_time = datetime.now()
    while app.contract_details_end != tickerId:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "contract_details not received"
            )

    app.disconnect()

    return app.contract_details


def fetch_matching_symbols(pattern, hostname=default_hostname,
                           port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "next_valid_id not received"
            )

    req_id = app.next_valid_id
    app.reqMatchingSymbols(req_id, pattern)

    start_time = datetime.now()
    while app.matching_symbols is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "contract_details not received"
            )

    app.disconnect()

    return app.matching_symbols


def place_order(contract, order, hostname=default_hostname,
                port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, port, client_id)
    while not app.isConnected():
        time.sleep(0.01)

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    while app.next_valid_id is None:
        time.sleep(0.01)

    app.placeOrder(app.next_valid_id, contract, order)
    while not ('Submitted' in set(app.order_status['status'])):
        time.sleep(0.25)

    app.disconnect()

    return app.order_status


def enter_trade(n, prices_dataframe, Lambda):
    # calculate alpha ratio
    prices_dataframe['alpha'] = prices_dataframe['ko_Close'] / prices_dataframe['pep_Close']

    # calculate z_score
    def zscore(n):
        df_mean = prices_dataframe['alpha'].rolling(n, center=False).mean().shift(1)
        df_std = prices_dataframe['alpha'].rolling(n, center=False).std(ddof=1).shift(1)
        z_score = (prices_dataframe['alpha'] - df_mean) / df_std
        return z_score

    z_score = zscore(n)
    prices_dataframe['z_score'] = z_score

    # determine entry status for Y(ko)
    conditions = [
        (prices_dataframe['z_score'] > Lambda),
        (prices_dataframe['z_score'] <= Lambda) & (prices_dataframe['z_score'] >= -Lambda),
        (prices_dataframe['z_score'] < -Lambda)
    ]
    values = ['sell', 'do not enter', 'buy']
    prices_dataframe['action_y'] = np.select(conditions, values)
    prices_dataframe['date'] = prices_dataframe['Date'].shift(-1)
    prices_dataframe['price_y'] = prices_dataframe['ko_Open'].shift(-1)
    prices_dataframe['amount_y'] = 100  #####default enter amount is 100
    prices_dataframe['ticker_y'] = 'ko'

    # determine entry status for X(pep)
    conditions = [
        (prices_dataframe['action_y'] == 'sell'),
        (prices_dataframe['action_y'] == 'do not enter'),
        (prices_dataframe['action_y'] == 'buy')
    ]
    values = ['buy', 'do not enter', 'sell']
    prices_dataframe['action_x'] = np.select(conditions, values)
    prices_dataframe['price_x'] = prices_dataframe['pep_Open'].shift(-1)
    prices_dataframe['amount_x'] = prices_dataframe["price_y"] * prices_dataframe['amount_y'] / prices_dataframe[
        'price_x']
    prices_dataframe['ticker_x'] = 'pep'

    # create dataframe for Y(ko)
    df1 = prices_dataframe[['date', 'ticker_y', 'price_y', 'amount_y', 'action_y']]
    df_y = df1[(df1.action_y != '0') & (df1.action_y != 'do not enter')]
    df_y.rename(columns={'ticker_y': 'ticker', 'price_y': 'price', 'amount_y': 'quantity', 'action_y': 'action'},
                inplace=True)

    # create dataframe for X(pep)
    df2 = prices_dataframe[['date', 'ticker_x', 'price_x', 'amount_x', 'action_x']]
    df_x = df2[(df2.action_x != '0') & (df2.action_x != 'do not enter')]
    df_x.rename(columns={'ticker_x': 'ticker', 'price_x': 'price', 'amount_x': 'quantity', 'action_x': 'action'},
                inplace=True)

    # concat X and Y
    frames = [df_y, df_x]
    result = pd.concat(frames)
    result['trip'] = 'entry'
    result['status'] = 'FILLED'
    result['date'] = pd.to_datetime(result['date'])
    result.sort_values(by='date', inplace=True, ascending=True)
    return result


def exit_trade(n, prices_dataframe, entry_trade, rho, L, X):
    # copy entry_trade 作为exit修改的基础

    first_index = entry_trade.first_valid_index()
    last_index = entry_trade.index[-1]

    exit_order = entry_trade.copy(deep=True)

    # 遍历 entry_trade 修改action和trip的状态
    exit_order['trip'] = 'exit'

    # change LMT price
    price2 = [
        (exit_order['action'] == 'sell'),
        (exit_order['action'] == 'buy')
    ]
    # create a list of values we want to assign for each condition
    price2_values = [exit_order['price'] * (1 + rho), exit_order['price'] * (1 - rho)]
    # create a new column and use np.select to assign values to it using our lists as arguments
    exit_order['price_exit'] = np.select(price2, price2_values)

    # create a list of action2 to change action
    action2 = [
        (exit_order['action'] == 'sell'),
        (exit_order['action'] == 'buy')
    ]
    # create a list of values we want to assign for each condition
    action2_values = ['buy', 'sell']
    # create a new column and use np.select to assign values to it using our lists as arguments
    exit_order['action_exit'] = np.select(action2, action2_values)

    del exit_order['action'], exit_order['price']
    order = ['date', 'ticker', 'price_exit', 'quantity', 'action_exit', 'trip', 'status']
    exit_order = exit_order[order]
    exit_order.columns = ['date', 'ticker', 'price', 'quantity', 'action', 'trip', 'status']

    # 判断status
    exit_order['date_exit'] = ''
    exit_order['status_exit'] = ''

    for i in range(83, 1313):
        if i in exit_order.index:
            if exit_order['ticker'][i].values[0] == 'ko' and exit_order['action'][i].values[0] == 'buy':
                for j in range(i + 1, i + X+1):  # x=60
                    Loss = ((prices_dataframe['ko_Close'][j] - exit_order['price'][i].values[0]) /
                            exit_order['price'][i].values[0]) * 100
                    if Loss > L:  # L=20
                        exit_order['status_exit'][i] = 'STOPLOSS'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    elif exit_order['price'][i].values[0] > prices_dataframe['ko_Close'][j]:
                        exit_order['status_exit'][i] = 'FILLED'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    else:
                        if i + X+1 > 1312:
                            exit_order['status_exit'][i] = 'OPEN'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
                        else:
                            exit_order['status_exit'][i] = 'TIMEOUT'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
            elif exit_order['ticker'][i].values[0] == 'ko' and exit_order['action'][i].values[0] == 'sell':
                for j in range(i + 1, i + X+1):
                    Loss = -((prices_dataframe['ko_Close'][j] - exit_order['price'][i].values[0]) /
                             exit_order['price'][i].values[0]) * 100
                    if Loss > L:  # L=20
                        exit_order['status_exit'][i] = 'STOPLOSS'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    elif exit_order['price'][i].values[0] < prices_dataframe['ko_Close'][j]:
                        exit_order['status_exit'][i] = 'FILLED'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    else:
                        if i + X+1 > 1312:
                            exit_order['status_exit'][i] = 'OPEN'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
                        else:
                            exit_order['status_exit'][i] = 'TIMEOUT'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
            elif exit_order['ticker'][i].values[0] == 'pep' and exit_order['action'][i].values[0] == 'buy':
                for j in range(i + 1, i + X+1):
                    Loss = ((prices_dataframe['pep_Close'][j] - exit_order['price'][i].values[0]) /
                            exit_order['price'][i].values[0]) * 100
                    if Loss > L:  # L=20
                        exit_order['status_exit'][i] = 'STOPLOSS'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    elif exit_order['price'][i].values[0] > prices_dataframe['pep_Close'][j + 1]:
                        exit_order['status_exit'][i] = 'FILLED'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    else:
                        if i + X+1 > 1312:
                            exit_order['status_exit'][i] = 'OPEN'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
                        else:
                            exit_order['status_exit'][i] = 'TIMEOUT'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
            else:
                for j in range(i + 1, i + X+1):
                    Loss = -((prices_dataframe['pep_Close'][j] - exit_order['price'][i].values[0]) /
                             exit_order['price'][i].values[0]) * 100
                    if Loss > L:  # L=20
                        exit_order['status_exit'][i] = 'STOPLOSS'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    elif exit_order['price'][i].values[0] < prices_dataframe['pep_Close'][j + 1]:
                        exit_order['status_exit'][i] = 'FILLED'
                        exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                        break
                    else:
                        if i + X+1 > 1312:
                            exit_order['status_exit'][i] = 'OPEN'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
                        else:
                            exit_order['status_exit'][i] = 'TIMEOUT'
                            exit_order['date_exit'][i] = prices_dataframe['Date'][j + 1]
                            break
        else:
            continue

    # format the dataframe
    del exit_order['date'], exit_order['status']
    order = ['date_exit', 'ticker', 'price', 'quantity', 'action', 'trip', 'status_exit']
    exit_order = exit_order[order]
    exit_order.columns = ['date', 'ticker', 'price', 'quantity', 'action', 'trip', 'status']
    exit_order['date'] = pd.to_datetime(exit_order['date'])

    # concat X and Y
    frames = [exit_order, entry_trade]
    result = pd.concat(frames)
    result['date'] = pd.to_datetime(result['date'])
    result.sort_values(by='date', inplace=True, ascending=True)
    return result

