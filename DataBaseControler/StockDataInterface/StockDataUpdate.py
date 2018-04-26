#coding:utf-8
import pandas as pd
import tushare as ts
class StockDataUpdater(object):

    def __init__(self):
        pass

    def stock_list_update(self,type='all'):
        type_list =['all']
        #输入检查
        if not isinstance(type,str):
            raise TypeError,'stock_type must be string'
        elif isinstance(type,str) and type not in type_list:
            raise ValueError,'%s is not a valid type' % (type)
        #更新数据
        if type == 'all':
            return ts.get_stock_basics()

if __name__ =='__main__':
    updater = StockDataUpdater()
    print updater.stock_list_update()
