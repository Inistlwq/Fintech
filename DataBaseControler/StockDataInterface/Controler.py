#coding:utf-8
import os
from DataBaseControler.setting import database_path
class StockDataControler(object):

    def __init__(self,stock_database_path):
        self._stock_database_path = stock_database_path
        pass

    def stock_basis_init(self):
        stock_basis_path = os.path.join(self._stock_database_path,'stock_basis')
        if os.path.isdir(stock_basis_path):
            pass
        else:
            os.mkdir(stock_basis_path)

if __name__ == '__main__':
    c = StockDataControler(database_path())
    print database_path()
    c.stock_basis_init()
