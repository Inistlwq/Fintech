#coding:utf-8

import networkx as nx
import matplotlib.pylab as plt
import pandas as pd
import os
import datetime
import tushare as ts
import math
import numpy as np
from code.CommonLib import Cache
from code.CommonLib import TimeSequenceLib
from EdgeEvaluationLib import DirectEdge

class DirectStockMarket(object):

    def __init__(self,current_time = datetime.datetime.today()):
        self._current_time = TimeSequenceLib.standard_time_input(current_time)
        self._base_path = os.path.split(os.path.abspath(__file__))[0]
        self._time_length = 60
    @property
    def time_length(self):
        return self._time_length
    def generate_path(self,start,end,folder_name,base_name):
        '''
        标准化存储文件生成路径和名称
        :param start:开始时间
        :param end: 结束时间
        :param folder_name:文件夹名称
        :param base_name: 文件基类名
        :return:
        '''
        #标准化输入输出时间
        start = TimeSequenceLib.standard_time_input(start)
        end = TimeSequenceLib.standard_time_input(end)
        #print start,end
        #存储路径检查
        folder_path = os.path.join(self._base_path,'Graphs',folder_name)
        if os.path.isdir(folder_path):
            pass
        else:
            os.mkdir(folder_path)
        file_name = '%s(%s to %s).gml'%(base_name,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'))
        path = os.path.join(folder_path,file_name)
        return path

    def GeneratingCompeleteGraph(self,stock_list,start=None,end=None,folder_name=None,file_name = None):
        '''
        讲股票列表中包括的所有股票当做节点，生成这些节点构成的完全图
        :param stock_list:股票列表
        :param start:数据开始时间
        :param end:数据结束时间
        :return:
        '''
        '''输入检查'''
        if start and end:
            self._time_length = (end - start).days
        if end == None:
            end = datetime.datetime.today().strftime('%Y-%m-%d')
        if start == None:
            start,end= TimeSequenceLib.standard_trading_section(end = end,time_length=self._time_length)
        start = TimeSequenceLib.standard_time_input(start)
        end = TimeSequenceLib.standard_time_input(end)
        '''构建网络图(完全图)'''
        #生成模块
        i = 0.
        length = len(stock_list)*(len(stock_list)-1)
        G = nx.Graph(name='%s(%s to %s)' %(file_name,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d')))
        for stock in stock_list:
            G.add_node(stock)
        for x in stock_list:
            for y in stock_list:
                if x != y:
                    r = DirectEdge.Pearson_correlation_coefficient(x, y,start,end)
                    # if temp and temp > 0.8 or temp< 0.:
                    if r:
                        i += 1
                        print x, y, r,u'进度：%.4f%%' %(100*i/length)
                        G.add_edge(x, y, weight=r)
                    else:
                        print x,y,'fail'

        '''网络图保存(gml)'''
        path = self.generate_path(start = start,end = end,folder_name=folder_name,base_name='hz300s')
        nx.write_gml(G,path)

        '''网络图输出'''

        #nx.draw_networkx(G)
        #plt.show()
        return G


    def ReadInGraph(self,path):
        if os.path.isfile(path):
            G = nx.read_gml(path)
            return G

    def GraphAnalysisByEdge(self,G):
        '''
        生成边上权值的统计直方图
        :param G:
        :return:
        '''
        '''绘制统计直方图进行分析'''
        fig = plt.figure()
        data = [G[x][y]['weight'] for x,y in G.edges()]
        plt.hist(data,bins = 10)
        plt.show()
        pass

    def StockMarketCommunity(self,G,pos_threshold,neg_threshold):
        '''
        将网络进行筛选处理，保证边的权值在某个区间中
        :param G:
        :param pos_threshold:
        :param neg_threshold:
        :return:
        '''
        remove_list = []
        for x, y in G.edges():
            if G[x][y]['weight'] > pos_threshold or G[x][y]['weight'] < neg_threshold:
                pass
            else:
                remove_list.append((x, y))
        for x, y in remove_list:
            G.remove_edge(x, y)
        remove_list = []
        for node, degree in nx.degree(G):
            if degree == 0:
                remove_list.append(node)
        G.remove_nodes_from(remove_list)
        return G


if __name__ == '__main__':
    '''
    生成完全图的实验数据
    '''
    stock_list = list(Cache.GetStockClassied('hs300s').code)
    print stock_list
    s = DirectStockMarket()
    end = datetime.datetime.today()
    for i in range(365):
        start, end = TimeSequenceLib.standard_trading_section(end=end, time_length=s.time_length)
        path = s.generate_path(start=start, end=end, folder_name='DirectStockMarket', base_name='hz300s')
        if os.path.isfile(path):
            print 'get',path
        else:
            s.GeneratingCompeleteGraph(stock_list = stock_list,
                                       end=end,
                                       folder_name='DirectStockMarket',
                                       file_name = 'hs300s')
        end -= datetime.timedelta(days=1)
        while end.weekday() == 5 or end.weekday() == 6:
            end -= datetime.timedelta(days=1)

