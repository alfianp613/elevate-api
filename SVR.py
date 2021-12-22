import investpy
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import datetime

def forecast_SVR(koin):
    today = date.today()
    now = today.strftime("%d/%m/%Y")

    n = 4
    past_date = today - relativedelta(months=n)
    date_format = '%d/%m/%Y'
    past_date_str = past_date.strftime(date_format)

    data = investpy.get_crypto_historical_data(crypto=koin,
                                               from_date=past_date_str,
                                               to_date=now,
                                               interval='daily')

    series = data['Close']

    value = series.values.tolist()
    tanggal = series.index
    t = tanggal.strftime('%Y-%m-%d')

    dict_tgl = {'ds': t,
                'y': value}
    df_tgl = pd.DataFrame(dict_tgl)

    ss_x = StandardScaler()
    ss_y = StandardScaler()

    m = df_tgl.iloc[:, 0:1].values
    n = df_tgl.iloc[:, 1:2].values

    d2 = np.array([123, 124]).reshape(-1, 1)
    d = []
    for i in range(len(m)):
        d.append(i)
    d = np.array(d).reshape(-1, 1)

    d_train_pred = ss_x.fit_transform(np.concatenate((d, d2)))

    xpred = d_train_pred[-3:]

    x = d_train_pred[:-2]
    y = ss_y.fit_transform(n)

    regressor = SVR(kernel='rbf')
    regressor.fit(x, y.ravel())

    pred_ss = regressor.predict(xpred).reshape(-1, 1)
    pred_svr = ss_y.inverse_transform(pred_ss).tolist()

    date_3 = pd.date_range(today, periods=3, freq='D')
    date_3_rev = date_3.strftime('%Y-%m-%d').tolist()
    
    now = datetime.datetime.now()
    tanggal = f'{now.day}/{now.month}/{now.year}'
    time = f'{now.hour}:{now.minute}'
    
    svr_output = {'tanggal':date_3_rev,
                  'close':pred_svr,
                  'date':tanggal,
                  'jam':time}
    import json
    with open(f'forecasting/forecasting {koin}.json', 'w') as f:
      json.dump(svr_output, f)
    
    return print(f'{koin} Selesai')
  
koin = ['bitcoin','ethereum','binance coin','tether','solana',
        'cardano','xrp','usd coin','polkadot','dogecoin']
for i in koin:
      forecast_SVR(i)
