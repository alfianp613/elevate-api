import investpy
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import datetime
import pyrebase

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

    regressor = SVR(kernel='rbf', C=20.211818181818185, epsilon=0.3, gamma=1)
    regressor.fit(x, y.ravel())

    pred_ss = regressor.predict(xpred).reshape(-1, 1)
    pred_svr = ss_y.inverse_transform(pred_ss)
    a = [float(i) for i in pred_svr]
    
    date_3 = pd.date_range(today, periods=3, freq='D')
    date_3_rev = date_3.strftime('%Y-%m-%d').tolist()
    
    now = datetime.datetime.now()
    tanggal = f'{now.day}/{now.month}/{now.year}'
    time = f'{now.strftime("%H")}:{now.strftime("%M")}'
    
    svr_output = {'tanggal':date_3_rev,
                  'close':a,
                  'date':tanggal,
                  'jam':time}
    
    config = {'apiKey': "AIzaSyBF9zZqQBt2h0RJZN3Xubugse5Ba3qJLdw",
          'authDomain': "elevate-66775.firebaseapp.com",
          'projectId': "elevate-66775",
          'databaseURL': "https://elevate-66775-default-rtdb.asia-southeast1.firebasedatabase.app/",
          'storageBucket': "elevate-66775.appspot.com",
          'messagingSenderId': "1008765930388",
          'appId': "1:1008765930388:web:5ad1f3c8464d8f8d859d81",
          'measurementId': "G-0Q4Y5MFCVD"}
    firebase = pyrebase.initialize_app(config)
    # Get a reference to the auth service
    auth = firebase.auth()

    email = 'alfianp613@gmail.com'
    password = 'DummyDummy631'
    # Log the user in
    user = auth.sign_in_with_email_and_password(email, password)
    database = firebase.database()
    a = database.child("Forecast").child(koin).set(svr_output,user['idToken'])
    return print(f'forecast {koin} Selesai')
