import nsepy
import pprint
import concurrent.futures
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap


def best():
  data=dict()
  temp=dict()



  df=pd.read_excel('All DATA (1).xlsx')
# print(df.head(10))
  sector=df['Sector'].unique()
  stocks=df['Symbol'].unique()
# print(df.columns)


  for i in sector:
    data[i]=[]
  for i in range(len(df)):
    temp[df.iloc[i,1]]=df.iloc[i,0]

  def d(symbol):
    if(len(nsepy.get_quote(symbol.replace("&","%26"))["data"])>0):
      data_nse=nsepy.get_quote(symbol.replace("&","%26"))["data"][0]
      sec=temp[symbol]
      if(data_nse['change']!='-'):
        data[sec].append((float(data_nse['change'].replace(',','')),symbol,float(data_nse['varMargin'].replace(',',''))))
  
# d('TVSMOTOR')
# print(data)
  # for i in stocks:
  #   d(i)
  def multi(stocks):

    with concurrent.futures.ThreadPoolExecutor() as executor:
      result=executor.map(d,stocks)
      
      # print(result) 

  multi(stocks)
  # print(data)
  

  fruits=[]
  counts=[]

  for i in sector:
    k=data[i]
    max=-100
    name=''
    for j in k:
    
      if(j[0]>=max):
        max=j[0]
        name=j[1]
    b=(i,max,name)
    fruits.append(''+i+'-'+name)
    counts.append(max)
    # print(b)
  source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))

  p = figure(x_range=fruits, height=500, width=1900, toolbar_location=None, title="HOT STOCKS-SECTOR WISE")
  p.vbar(x='fruits', top='counts', width=0.3, source=source, legend_field="fruits",
       line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))
  p.line(x=fruits, y=counts, color="red", line_width=2)
  p.xgrid.grid_line_color = None
  p.y_range.start = -50
  p.y_range.end = 50

  p.legend.orientation = "horizontal"
  p.legend.location = "top_center"





  # show(p)
  return p,data

# best()