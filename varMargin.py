from ns import best
import nsepy
from bokeh.plotting import figure, show
import pandas as pd
import pandas as pd
from bokeh.transform import factor_cmap
from bokeh.io import  show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import concurrent.futures
from bokeh.palettes import Spectral6
import nsepy

import concurrent.futures




def var_pchange(df):

  # df=pd.read_csv('user.csv')
  # print(df)
  x=df[df.exchange=='NSE'].symbol.unique()
  y=[]
  def d(symbol):
      if(len(nsepy.get_quote(symbol.replace("&","%26"))["data"])>0):
        data_nse=nsepy.get_quote(symbol.replace("&","%26"))["data"][0]
    #     print(data_nse)
        if(data_nse['varMargin']!='-' and data_nse['pChange']!='-'):
          y.append((float(data_nse['varMargin'].replace(',','')),float(data_nse['pChange'].replace(',',''))))
        else:
          y.append((9,20))
      else:
        
        y.append((9,20))
    

  def multi(x):

      with concurrent.futures.ThreadPoolExecutor() as executor:
        result=executor.map(d,x)
      
      # print(result) 

  multi(x)

# print(y)
  fruits=x

  data = {'fruits' : fruits,
        '2015'   : [],
        '2016'   : [],
        }
  for i in y:
      data['2015'].append(i[0])
      data['2016'].append(i[1])
    
    

  years=['var','pchange']
  x = [ (fruit, year) for fruit in fruits for year in years ]

  counts = sum(zip(data['2015'], data['2016']), ()) # like an hstack
  source = ColumnDataSource(data=dict(x=x, counts=counts))

  p = figure(x_range=FactorRange(*x), height=700,width=5000, title="Maximum Loss(VarMargin) % vs Change in Stock value (%) ",
           toolbar_location=None, tools="")
  p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",

       
       fill_color=factor_cmap('x', palette=Spectral6, factors=years, start=1, end=2))
  p.y_range.start = -10
  p.x_range.range_padding = 0.1
  p.xaxis.major_label_orientation = 1
  p.xgrid.grid_line_color = None
 
  # show(p)
  return p
#var_pchange()