#coding:utf-8
import pandas as pd
import os
import datetime
import numpy as np
from Controler import *
from StockDataUpdate import *
from CommonLib.TimeSequenceLib import standard_time_input

class StockDataInterface(object):
    def __init__(self):
        self._stock_database_path = StockDataControler().stock_basis_init()

    def stock_basis(self,type='all'):
        type_list = ['all']
        # 输入类型检查
        if not isinstance(type, str):
            raise TypeError, 'stock_type must be string'
        elif isinstance(type, str) and type not in type_list:
            raise ValueError, '%s is not a valid type' % (type)
        #数据接口
        path = os.path.join(StockDataControler().stock_basis_init(),'%s.csv' % datetime.datetime.today().strftime('%Y-%m-%d'))
        if os.path.isfile(path):
            temp = pd.read_csv(path,header=0,index_col=0)
            return temp
        else:
            return StockDataUpdater().stock_list_update()
    def stock_statue_log(self,security):
        path = os.path.join(StockDataControler().stock_init(security), '%s(state_log).csv' % security)
        if os.path.isfile(path):
            temp = pd.read_csv(path,index_col=0)
        else:
            temp = StockDataUpdater().stock_history_data_update(security)
        return temp

    def stock_history_data(self,security,start=None,end=None):
        #输入检查
        if start:
            start = standard_time_input(start).strftime('%Y-%m-%d')
        else:
            start = standard_time_input(datetime.datetime.today()).strftime('%Y-%m-%d')
        if end:
            end = standard_time_input(end).strftime('%Y-%m-%d')
        else:
            end = standard_time_input(datetime.datetime.today()).strftime('%Y-%m-%d')
        #计算合法的数据查询区间（排除休市和停牌）
        state_log = self.stock_statue_log(security)
        if start in state_log.index :
            if state_log.loc[start][0] == 'Trade':#如果时交易日
                pass
            elif state_log.loc[start][0] == 'suspend':
                while state_log.loc[start][0] != 'Trade':
                    start = datetime.datetime.strptime(start,'%Y-%m-%d')+datetime.timedelta(days=1)
                    start = start.strftime('%Y-%m-%d')

        elif start not in state_log.index:#说明数据缺省
            StockDataUpdater().stock_history_data_update(security)
        else:
            raise ValueError

        if end in state_log.index :
            if state_log.loc[end][0] == 'Trade':#如果时交易日
                pass
            elif state_log.loc[end][0] == 'suspend':
                while state_log.loc[end][0] != 'Trade':
                    end = datetime.datetime.strptime(end,'%Y-%m-%d')-datetime.timedelta(days=1)
                    end = end.strftime('%Y-%m-%d')

        elif end not in state_log.index:#说明数据缺省
            StockDataUpdater().stock_history_data_update(security)
        else:
            raise ValueError
        #数据抓取
        path = os.path.join(StockDataControler().stock_init(security), '%s(history_data).csv' % security)
        if os.path.isfile(path):
            temp = pd.read_csv(path,index_col='date')
        else:
            temp = StockDataUpdater().stock_history_data_update(security)
        history_data = pd.DataFrame()
        for date in pd.date_range(start = start,end = end):
            x = date.strftime('%Y-%m-%d')
            if x in temp.index:
                history_data = history_data.append(temp.loc[x])
        return history_data

if __name__ =='__main__':
    s = StockDataInterface()
    print s.stock_history_data('600848',start = '2018-4-15',end = '2018-4-22')