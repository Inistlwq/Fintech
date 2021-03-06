#coding:utf-8
import os
from DataBaseControler.setting import database_path
class StockDataControler(object):

    def __init__(self,stock_database_path=database_path()):
        self._stock_database_path = stock_database_path
        pass

    def stock_basis_init(self):
        '''
        股票总览初始化
        :return:
        '''
        stock_basis_path = os.path.join(self._stock_database_path,'stock_basis')
        if os.path.isdir(stock_basis_path):
            pass
        else:
            os.mkdir(stock_basis_path)
        return stock_basis_path

    def stock_init(self,security):
        '''
        股票文件夹初始化
        :param security:
        :return:
        '''
        stocks_path = os.path.join(self._stock_database_path, 'stocks')
        if os.path.isdir(stocks_path):
            pass
        else:
            os.mkdir(stocks_path)

        stock_path = os.path.join(self._stock_database_path, 'stocks',security)
        if os.path.isdir(stock_path):
            pass
        else:
            os.mkdir(stock_path)
        return stock_path

    def stock_tick_init(self,security):
        '''
        初始化股票分笔数据文件夹
        :param security:
        :return:
        '''
        stock_path = self.stock_init(security)
        stock_tick_path = os.path.join(stock_path,'stock_tick')
        if os.path.isdir(stock_tick_path):
            pass
        else:
            os.mkdir(stock_tick_path)
        return stock_tick_path



if __name__ == '__main__':
    c = StockDataControler()
    print database_path()
    c.stock_basis_init()
