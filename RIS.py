import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
from math import pi
from datetime import date

import pandas as pd
from bokeh.layouts import row

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from bokeh.plotting import figure, show

def ris(df):
    # df=pd.read_csv('user.csv')
    # print(df)

    # import pandas as pd
    # import numpy as np

    # # df = pd.DataFrame({'close':[4724.89, 4378.51,6463.00,9838.96,13716.36,10285.10,
    # #                           10326.76,6923.91,9246.01,7485.01,6390.07,7730.93,
    # #                           7011.21,6626.57,6371.93,4041.32,3702.90,3434.10,
    # #                           3813.69,4103.95,5320.81,8555.00,10854.10]})
    # df=pd.read_csv('/content/tradebook-JC9287_conv.csv')
    # print(df)
    n = 14


    def rma(x, n, y0):
        a = (n-1) / n
        ak = a**np.arange(len(x)-1, -1, -1)
        return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

    df['change'] = df['price'].diff()
    df['gain'] = df.change.mask(df.change < 0, 0.0)
    df['loss'] = -df.change.mask(df.change > 0, -0.0)
    df['avg_gain'] = rma(df.gain[n+1:].to_numpy(), n, np.nansum(df.gain.to_numpy()[:n+1])/n)
    df['avg_loss'] = rma(df.loss[n+1:].to_numpy(), n, np.nansum(df.loss.to_numpy()[:n+1])/n)
    df['rs'] = df.avg_gain / df.avg_loss
    df['rsi_14'] = 100 - (100 / (1 + df.rs))

    
    # fig, (ax1, ax2) = plt.subplots(2)
    # ax1.get_xaxis().set_visible(False)
    # df['price'].plot(ax=ax1)
    # ax1.set_ylabel('Price (Rs)')
    # df['rsi_14'].plot(ax=ax2)
    # ax2.set_ylim(0,100)
    # ax2.axhline(30, color='r', linestyle='--')
    # ax2.axhline(70, color='r', linestyle='--')
    # ax2.set_ylabel('RSI')

    # plt.show()

    x=[]
    for i in range(len(df['price'])):
        x.append(i)
    s1 = figure(width=200, height=200, background_fill_color="#fafafa")
    s1.line( x,df['price'])

    s2 = figure(width=500, height=500, background_fill_color="#fafafa")
    s2.line(x,df['rsi_14'])
    s2.circle(x,30,color="firebrick")
    s2.circle(x,70,color="firebrick")
    
    

    df2=df.copy(deep=True)
    df2['total cost']=df2['quantity']*df2['price']

    df2.loc[df2['trade_type'] == 'buy', 'total cost'] = 0 - df2.loc[df2['trade_type'] == 'buy', 'total cost']

    


    df2.drop(df2.columns.difference(['trade_date','total cost']), 1, inplace=True)
    df2['trade_date']=pd.to_datetime(df2['trade_date'])

    subset = df2[['trade_date', 'total cost']]

    subset1 = subset.groupby("trade_date").sum("total cost")

    all_days = pd.date_range(subset1.index.min(), subset1.index.max(), freq='D')
    subset2 = subset1.reindex(all_days, fill_value=0)

    # subset2.head(693)["total cost"].agg(np.irr)

    

    cap=pd.read_csv('MCAP31032021_0_conv.csv')

    cap=cap.head(1793)

    cap['Market capitalization \n(Rs in Lakhs)']=cap['Market capitalization \n(Rs in Lakhs)'].astype(int)

    bins = [0, 50000, 700000, 2000000]
    names = ['Small Cap', 'Medium Cap', 'Large Cap', 'Mega Cap']

    d = dict(enumerate(names, 1))

    cap['Market_Cap'] = np.vectorize(d.get)(np.digitize(cap['Market capitalization \n(Rs in Lakhs)'], bins))

    cap.rename(columns={'Symbol': 'symbol'}, inplace=True)

    stockdf=df.copy(deep=True)

    stockdf=stockdf.join(cap.set_index("symbol"), how='left', on='symbol', lsuffix='x', rsuffix='y')

    stockdf['Market_Cap']=stockdf['Market_Cap'].fillna('Other Cap')

    stockdf['total_cost']=stockdf['quantity']*stockdf['price']
    stockdf.loc[stockdf['trade_type'] == 'sell', 'total_cost'] = 0 - stockdf.loc[stockdf['trade_type'] == 'sell', 'total_cost']

    stockdf=stockdf.groupby("Market_Cap").sum("total_cost")

    stockdf=stockdf.reset_index()

    
    stockdf['angle'] = stockdf['total_cost']/stockdf['total_cost'].sum() * 2*pi
    stockdf['color'] = Category20c[len(stockdf)]
    plot = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@Market_Cap: @total_cost")

    plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Market_Cap', source=stockdf)

    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None
    # show(plot)
    return row(plot,s2)
# ris()