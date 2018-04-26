#coding:utf-8
from code.CommonLib import Cache,TimeSequenceLib
import datetime
import pandas as pd

def Pearson_correlation_coefficient(x,y,start,end,period=1,method='pearson'):
    '''
    使用股票不同日的价格，基于pandas的自带功能实现股票之间的皮尔逊相关系数
    :param x:股票代码
    :param y:股票代码
    :return: 股票之间的皮尔逊相关系数
    '''
    #try:
    #获取数据
    start = TimeSequenceLib.standard_time_input(start)
    end = TimeSequenceLib.standard_time_input(end)
    x_data = Cache.GetStockHistory(str(x),start,end)
    y_data = pd.DataFrame()
    date_range = list(x_data.index)
    print date_range
    for i in range(1,len(date_range)):
        date = date_range[i-1]
        print date_range[i],date
        temp = Cache.GetStockHistory(str(y),start = date,end = date)
        print temp
        temp = temp.reset_index()
        temp.date_index = date_range[i]
        print temp
    print 'y',y_data['p_change']#,y_data['p_change']
    #计算相关系数
    if isinstance(x_data,pd.DataFrame) and isinstance(y_data,pd.DataFrame):
        #pearson : standard correlation coefficient
        #kendall : Kendall Tau correlation coefficient
        #spearman : Spearman rank correlation
        r =  x_data['p_change'].corr(y_data['p_change'],method=method)
        #print r,type(r)
        if r==r:#判断是否是nan
            return r
        else:
            return 0
    else:
        return False
    #except:
        #return 0

if __name__ == '__main__':
    print Pearson_correlation_coefficient('600848','600847',start = '2018-01-01',end = '2018-01-10')