import os
import time
import shutil

from sendtotelegram import send_graph

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import numpy as np


plt.style.use('dark_background')

def send_plot(plt,cid,product):
    if not os.path.exists('./temp/'):
        os.makedirs('./temp/')

    ts = int(time.time())
    image_path = './temp/'+str(ts)+'.png'

    plt.savefig(image_path, dpi=400)
    send_graph(cid,image_path,product)
    shutil.rmtree('./temp/')

def plot_graph(values,cid,product):
    predf = []
    for value in values:
        result = value.split('_')
        result = [result[0],float(result[1])]
        predf.append(result)

    df = pd.DataFrame (predf, columns = ['Date','Values'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Values'] = df['Values'].replace(0, np.nan)
    print(df)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.plot(df['Date'], df['Values'], color='blue')
    ax.set(xlabel="Date", ylabel="Price", title="Product Price Chart")

    date_form = DateFormatter("%b %d")
    ax.xaxis.set_major_formatter(date_form)
    
    send_plot(plt,cid,product)
