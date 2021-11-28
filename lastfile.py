import pandas as pd
import numpy as np
from bokeh.layouts import row
from bokeh.plotting import figure, show
from bokeh.palettes import Dark2_8
import itertools
def last(stockpd):
    # stockpd=pd.read_csv('user.csv')
    # stockpd=stockpd.drop(['order_id','trade_id'], axis=1)
    # stockpd
    # stockpd=pd.read_csv('user.csv')
    # stockpd=stockpd.drop(['order_id','trade_id'], axis=1)
    stockpd3=stockpd.set_index('symbol').drop(['isin','order_execution_time',], axis=1)
    metadata=pd.read_csv('sec_bhavdata_full.csv')
    metadata=metadata[["SYMBOL"," CLOSE_PRICE"]]
    metadata.rename(columns={'SYMBOL': 'symbol', ' CLOSE_PRICE': 'today_close_price'}, inplace=True)
    category_stock=pd.read_csv('NSE-Stock-LIST-1411-Stocks-Generated-on-25may2017.csv')
    category_stock=category_stock[["Symbol","Sector"]]
    category_stock.rename(columns={'Symbol': 'symbol'}, inplace=True)
    metadata=metadata.join(category_stock.set_index("symbol"), how='left', on='symbol')
    # print(metadata)
    stockpd3=stockpd3.join(metadata.set_index("symbol"), how='left', on='symbol')
    stockpd3=stockpd3.reset_index()
    stockpd3[["Sector"]]=stockpd3[["Sector"]].fillna('Others')
    stockpd3=stockpd3.set_index("Sector")
    # print(stockpd3)
    types_of_stocks=list(stockpd3.index.unique())
    p=figure(x_axis_type='datetime',tools='pan,wheel_zoom,box_zoom,reset')
    # colours=list(Dark2_8)
    allgraph=[]
    for i in range(len(types_of_stocks)):
    
        stockpd_x=stockpd3.loc[types_of_stocks[i]]
    
        if len(stockpd_x.shape)<2:
            stockpd_x=stockpd_x.to_frame().transpose()
            # print(stockpd_x)
        stockpd_x.drop(columns=["exchange","segment","series"],inplace=True)
        stockpd_x.reset_index(inplace=True)
    
    
        stockpd_x["bought/sold cost"]=stockpd_x["quantity"]*stockpd_x["price"]
    
        stockpd_x.loc[stockpd_x['trade_type'] == 'sell', 'bought/sold cost'] = 0 - stockpd_x.loc[stockpd_x['trade_type'] == 'sell', 'bought/sold cost']
    
        stockpd_x['cumulative']=stockpd_x["bought/sold cost"].cumsum()
        stockpd_x['total_stocks']=stockpd_x["quantity"].cumsum()
        stockpd_x["total_investment"]=stockpd_x["total_stocks"]*stockpd_x["today_close_price"]
        stockpd_x.reset_index()
        stockpd_x['year']= stockpd_x['trade_date'].apply(lambda x: x.split("-")[2])
        stockpd_x['month']= stockpd_x['trade_date'].apply(lambda x: x.split("-")[1])
        grp5=stockpd_x.groupby(['year','month']).sum()
        if grp5.shape[0]==1:
            # print('true')
            grp5=stockpd_x.copy(deep=True)
            grp5=grp5.reset_index()
            grp5=grp5.set_index(["trade_date"])
        
            # print(grp5)
        
        grp6=grp5.drop(['quantity','price','today_close_price','bought/sold cost','total_stocks'],axis=1)
    
        #  grp6.rename(columns={'cumulative': 'Invested'}, inplace=True)
        # grp6.rename(columns={'total_investment': 'current_investment'}, inplace=True)
        # print(grp6)
        grp6=grp6.reset_index()
        grp6['Date']=pd.to_datetime('01-'+grp6['month']+'-'+grp6['year'])
        grp6.set_index(['Date'],inplace=True)
        p=figure(x_axis_type='datetime',tools='pan,wheel_zoom,box_zoom,reset')
        p.line(x=grp6.index,y=grp6['cumulative'],line_color='red',legend_label='cumulative')
        p.line(x=grp6.index,y=grp6['total_investment'],line_color='green',legend_label='total_investment')
        p.title=types_of_stocks[i]
        
        # show(p)
        
        allgraph.append(p)
    
    return row(allgraph)
 

# last(df)