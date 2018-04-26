#coding:utf-8
import pandas as pd
import tushare as ts
import os
import datetime
import time
from ControlerLib import StockDataControler
from StockDataInterfaceLib import *
class StockDataUpdater(object):

    def __init__(self):
        pass

    def stock_list_update(self,type='all'):
        '''
        股票基本面板更新
        :param type:
        :return:
        '''
        type_list =['all',
                    'industry',
                    'concept',
                    'area',
                    'sme',
                    'gem',
                    'st',
                    'hs300s',
                    'ss50s',
                    'zz500s',
                    'terminated',
                    'suspended']
        #输入类型检查
        if not isinstance(type,str):
            raise TypeError,'stock_type must be string'
        elif isinstance(type,str) and type not in type_list:
            raise ValueError,'%s is not a valid type' % (type)
        #更新数据
        if type == 'all':
            temp = ts.get_stock_basics()
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'global.csv')
            temp.to_csv(path)
            return temp
        if type == 'industry':
            temp = ts.get_industry_classified()
            #temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'industry.csv')
            temp.to_csv(path)
        if type == 'concept':
            temp = ts.get_concept_classified()
            #temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'concept.csv')
            temp.to_csv(path)
        if type == 'area':
            temp = ts.get_area_classified()
            #temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'area.csv')
            temp.to_csv(path)
        if type == 'sme':
            temp = ts.get_sme_classified()
            #temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'sme.csv')
            temp.to_csv(path)
        if type == 'gem':
            temp = ts.get_gem_classified()
            #temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'gem.csv')
            temp.to_csv(path)
        if type == 'st':
            temp = ts.get_st_classified()
            # temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'st.csv')
            temp.to_csv(path)
        if type == 'hs300s':
            temp = ts.get_hs300s()
            temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'hs300s.csv')
            temp.to_csv(path)
        if type == 'sz50s':
            temp = ts.get_sz50s()
            temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'sz50s.csv')
            temp.to_csv(path)
        if type == 'zz500s':
            temp = ts.get_zz500s()
            temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'zz500s.csv')
            temp.to_csv(path)
        if type == 'terminated':
            temp = ts.get_terminated()
            temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'terminated.csv')
            temp.to_csv(path)
        if type == 'suspended':
            temp = ts.get_suspended()
            temp['name'] = temp['name'].map(lambda x: x.encode('utf-8'))
            path = os.path.join(StockDataControler().stock_basis_init(),
                                'suspended.csv')
            temp.to_csv(path)
    def stock_history_data_update(self,security):
        '''
        股票历史数据更新
        :param security:
        :return:
        '''
        #输入检查
        controler = StockDataControler()
        stock_list = StockDataInterface().stock_basis().index
        if int(security) not in stock_list:
            path = controler.stock_init(security)
            print path
            if os.path.isdir(path):
                os.rmdir(path)
            raise ValueError,'stock not exsit'#目前不清楚终止上市的股票是否在列表中
        #数据更新
        path = os.path.join(controler.stock_init(security),'%s(history_data).csv' % security)
        temp = ts.get_hist_data(security)
        if isinstance(temp,pd.DataFrame):#数据正常
            temp.to_csv(path)
        else:
            return pd.DataFrame()
        #检查上市和停牌时间
        date_range =  pd.date_range(start=temp.index[-1],end = temp.index[0])
        stock_state_log = pd.DataFrame()
        for date in date_range:
            if pd.to_datetime(date) in pd.to_datetime(temp.index):
                stock_state_log = stock_state_log.append(pd.DataFrame(['Trade'],index = [date]))
            else:
                stock_state_log = stock_state_log.append(pd.DataFrame(['suspend'], index=[date]))
        path = os.path.join(controler.stock_init(security), '%s(state_log).csv' % security)
        stock_state_log.to_csv(path)
        return temp

    def stock_tick_data_update(self,security):
        controler = StockDataControler()

        stock_tick_path = controler.stock_tick_init(security)

        for date in StockDataInterface().stock_history_data(security).index:
            temp = ts.get_tick_data(code = security,date = date)
            path = os.path.join(stock_tick_path,'%s.csv'%(date))
            if path not in os.listdir(stock_tick_path):
                temp.to_csv(path)

if __name__ =='__main__':
    def auto_update_stok_history():
        updater = StockDataUpdater()
        stock_data_interface = StockDataInterface()
        goal = len(stock_data_interface.stock_basis().index)
        count = 0.
        for security in stock_data_interface.stock_basis().index:
            code = str(security)
            while len(code) < 6:
                code = '0'+code
            updater.stock_history_data_update(code)
            count +=1
            print u'当前更新进度%f.2%%'%(100*count/goal)
    def auto_update_classfy():
        updater = StockDataUpdater()
        type_list = ['all',
                     'industry',
                     'concept',
                     'area',
                     'sme',
                     'gem',
                     'st',
                     'hs300s',
                     'ss50s',
                     'zz500s',
                     'terminated',
                     'suspended']
        for type in type_list:
            updater.stock_list_update(type = type)
    def auto_update_tick():
        updater = StockDataUpdater()
        stock_data_interface = StockDataInterface()
        for security in stock_data_interface.stock_basis().index:
            try:
                print 'srawling %s......'%(security)
                updater.stock_tick_data_update(security)
            except IOError:
                time.sleep(30)
                updater.stock_tick_data_update(security)

    updater = StockDataUpdater()
    updater.stock_tick_data_update('600848')
    #auto_update_stok_history()
    #auto_update_classfy()
