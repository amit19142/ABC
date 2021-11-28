import pandas as pd
from bokeh.transform import factor_cmap
from bokeh.io import  show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import concurrent.futures
from bokeh.palettes import Spectral6
import nsepy

import pandas as pd
import numpy as np
from bokeh.io import output_notebook ,show
from bokeh.plotting import figure
from bokeh.models import CustomJS, Dropdown
import pandas as pd
import datetime
from bokeh.transform import factor_cmap
from bokeh.io import show,output_notebook
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.palettes import Spectral6

def gold_comp(df2,s):
  df1=pd.read_excel("IMP_PRICE.xlsx")
  # print(df1.head())
  df1['Date']=df1['Name'].dt.date


  # df2=pd.read_csv('user.csv')
  df2['Date']=pd.to_datetime(df2.order_execution_time)
  df2['Date']=df2['Date'].dt.date

  # print(df1.head(5))
  # print(df2.head(5))


  df2.drop(['trade_date','exchange','segment',	'series','isin','trade_id',	'order_id', 'order_execution_time'],axis=1,inplace=True )
  stocks=dict()
  golddata=dict()

  for i in range(len(df1)):
    key=df1.iloc[i,2]
    golddata[key]=df1.iloc[i,1]

  # print(golddata)

  name=df2.symbol.unique()
  gold=dict()
  for i in range(len(name)):
    stocks[name[i]]=[]
    gold[name[i]]=[]

  for i in range(len(df2)):
    key=df2.iloc[i,0]
    
    ttype=df2.iloc[i,1]
    if(ttype=='buy'):
      qunatity=df2.iloc[i,2]
      price=df2.iloc[i,3]
      Date=df2.iloc[i,4]
      amount=qunatity*price
      stocks[key].append((Date,price, qunatity,amount))
  
  

  if(s in name):
    select=stocks[s]
    y=set()
    for i in select:
      y.add(i[0])
    dates=[]
    for i in y:
      dates.append(i)
    dates.sort()
    quantity=[]
    amount=[]
    price=[]
    ngram=[]
    goldprice=[]

    for i in range(len(dates)):
      a=0
      q=0
      p=0
      for j in range(len(select)):
        if(dates[i]==select[j][0]):
          a=a+select[j][3]
          q=q+select[j][2]
          p=select[j][1]
      
      amount.append(a)
      price.append(p)
      quantity.append(q)
      ngram.append(a/golddata[dates[i]])
      goldprice.append(golddata[dates[i]])
    
  
    for i in range(len(dates)):
      if(i!=0):
        amount[i]=amount[i]+amount[i-1]
        quantity[i]=quantity[i]+quantity[i-1]
        ngram[i]=ngram[i]+ngram[i-1]
  
    benifit_stock=[]
    benifit_gold=[]

    for i in range(len(amount)):
      benifit_stock.append(quantity[i]*price[i])
      benifit_gold.append(ngram[i]*goldprice[i])
      dates[i]=pd.to_datetime(dates[i])

  
  


    f=figure(x_axis_label="Date",y_axis_label=" Net Worth ",x_axis_type='datetime',title=" Total Wealth",plot_height=500,plot_width=1000)
    f.circle(dates,benifit_stock, size = 5, color = 'red')
    f.line(x=dates,y=benifit_stock,line_color='red',legend_label="STOCK Net Worth ")
    f.circle(dates,benifit_gold, size = 5, color = 'blue')
    f.line(x=dates,y=benifit_gold,line_color='blue',legend_label="GOLD Net Worth")
    f.circle(dates,amount, size = 5, color = 'green')
    f.line(x=dates,y=amount,line_color='green',legend_label="INVESTMENT")
   
    return f
  else:
     f=figure(x_axis_label="Date",y_axis_label=" Net Worth ",x_axis_type='datetime',title=" Total Wealth",plot_height=500,plot_width=1000)
     return f
  





  
  



    
    


  
    

  
  
 
  
  



# gold_comp('TATAMOTORS')



# def gold_comp():
#   df1=pd.read_excel("IMP_PRICE.xlsx")
#   print(df1.head())
#   df1['Date']=df1['Name'].dt.date


#   df2=pd.read_csv('user.csv')
#   df2['Date']=pd.to_datetime(df2.order_execution_time)
#   df2['Date']=df2['Date'].dt.date

#   # print(df1.head(5))
#   # print(df2.head(5))


#   df2.drop(['trade_date','exchange','segment',	'series','isin','trade_id',	'order_id', 'order_execution_time'],axis=1,inplace=True )
#   stocks=dict()
#   golddata=dict()

#   for i in range(len(df1)):
#     key=df1.iloc[i,2]
#     golddata[key]=df1.iloc[i,1]

#   # print(golddata)

#   name=df2.symbol.unique()
#   gold=dict()
#   for i in range(len(name)):
#     stocks[name[i]]=[]
#     gold[name[i]]=[]

#   for i in range(len(df2)):
#     key=df2.iloc[i,0]
  
#     ttype=df2.iloc[i,1]
#     qunatity=df2.iloc[i,2]
#     price=df2.iloc[i,3]
#     Date=df2.iloc[i,4]
#     amount=qunatity*price
#     stocks[key].append((ttype,Date,qunatity,amount,price))
#     ngram=amount/golddata[Date]
#     # print(ngram)
#     gold[key].append((Date,ngram))


#   # print(stocks['IBREALEST'])
#   # print(gold['IBREALEST'])
#   benifits_stock=dict()
#   benifits_gold=dict()
#   for i,j in stocks.items():
#     benifits_stock[i]=()
#     qs=0
#     am=0
#     for k in j:
#       qs=qs+k[2]
#       am=am+k[3]
#     benifits_stock[i]=(qs,am)
#   for i,j in gold.items():
#     tg=0
#     for k in j:
#       tg=tg+k[1]
    
#     benifits_gold[i]=tg

#   # print(benifits_gold)
#   # print(benifits_stock)
#   td_gold_price=154177
#   stock=stocks.keys()
#   td_stock_price=dict()
#   def c(i):
    
#       if(len(nsepy.get_quote(i.replace("&","%26"))["data"])>0):
#         data_nse=nsepy.get_quote(i.replace("&","%26"))["data"][0]
#         td_stock_price[i]=float(data_nse['dayHigh'].replace(',',''))
      
#       else:
      
#         td_stock_price[i]=100
#   def multi(stock):

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#       result=executor.map(c,stock)
      
     

#   multi(stocks)
    
    

#   print(td_stock_price)

#   main_output=dict()
#   for i,j in benifits_stock.items():
#     main_output[i]=((benifits_stock[i][0]*td_stock_price[i]),benifits_stock[i][1],(benifits_gold[i]*td_gold_price))
#     print(main_output[i])
#   # print(main_output)

#   fruits=stocks.keys()
#   data = {'fruits' : fruits,
#         '2015'   : [],
#         '2016'   : [],
#         '2017'   : []}
#   for i in main_output.values():
#     data['2015'].append(i[0])
#     data['2016'].append(i[1])
#     data['2017'].append(i[2])

#   years=['STOCK WEALTH','AMOUNT INVESTED','GOLD WEALTH']
#   x = [ (fruit, year) for fruit in fruits for year in years ]
#   # print(main_output.values())






#   counts = sum(zip(data['2015'], data['2016'], data['2017']), ()) # like an hstack

#   source = ColumnDataSource(data=dict(x=x, counts=counts))

#   p = figure(x_range=FactorRange(*x), height=700,width=5000, title="GOLD vs STOCK ",
#            toolbar_location=None, tools="")

#   p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",

       
#        fill_color=factor_cmap('x', palette=Spectral6, factors=years, start=1, end=2))
#   p.y_range.start = 0
#   p.x_range.range_padding = 0.1
#   p.xaxis.major_label_orientation = 1
#   p.xgrid.grid_line_color = None
 
#   show(p)
# gold_comp()

