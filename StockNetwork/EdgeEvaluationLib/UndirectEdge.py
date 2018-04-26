#coding:utf-8
from DataBaseControler.StockDataInterface.StockDataInterface import StockDataInterface
import pandas as pd
import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.join(BASE_DIR,'CommonLib'))
sys.path.append(BASE_DIR)
print sys.path
def Pearson_correlation_coefficient(x,y,start,end,method='pearson'):
    '''
    使用股票同日价格，基于pandas的自带功能实现股票之间的皮尔逊相关系数
    :param x:股票代码
    :param y:股票代码
    :return: 股票之间的皮尔逊相关系数
    '''
    stock_data_interface = StockDataInterface()
    try:
        #获取数据
        x_data = stock_data_interface.stock_history_data(str(x),start,end)
        y_data = stock_data_interface.stock_history_data(str(y),start,end)
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
    except:
        return 0