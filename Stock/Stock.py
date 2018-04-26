#coding:utf-8
import pandas as pd
import tushare as ts

class Stock(object):
    def __init__(self,security,name,current_state = 'Trading',trading_date = [],suspend_date = []):
        '''

        :param security:
        :param name:
        :param current_state:默认股票正在上市
        :param trading_date: 默认为空
        :param suspend_date: 默认为空
        '''
        self._securty = security#股票代码
        self._name = name#股票名称
        self._current_state =current_state#当前状态：上市/停牌/终止上市
        self._trading_date = trading_date#交易日期
        self._suspend_date = suspend_date#停牌日期
        self._history_data = pd.DataFrame()#历史数据
        self._tick_data = {}#默认为空字典，字典中键值对为：日期（str）:pd.DataFrame()

    @property
    def code(self):
        return self._securty

    @property
    def name(self):
        return self._name

    @property
    def current_state(self):
        return self._current_state

    @property
    def trading_date(self):
        return self._trading_date

    @property
    def suspend_date(self):
        return self._suspend_date

    @property
    def history_data(self):
        return self._history_data

    @property
    def tick_data(self):
        return self.tick_data

if __name__ == '__main__':
    pass