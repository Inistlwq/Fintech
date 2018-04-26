#coding:utf-8
import os
import networkx as nx
import matplotlib.pyplot as plt
from UndirectStockMarket import UndirectStockMarket

def EdgeDistributionAnalysis():
    '''
    使用频度直方图分析无向股票市场中股票间相关系数总体变化的趋势
    :return:
    '''
    #文件夹路径初始化
    base_path = os.path.split(os.path.abspath(__file__))[0]
    folder_path = os.path.join(base_path,'Graphs','UndirectStockMarket')

    tag = 6#窗口中的子图数量
    graphs = sorted(os.listdir(folder_path),key = lambda item:os.path.getctime(os.path.join(folder_path, item)))
    while graphs:
        temp = graphs[:tag]
        graphs = graphs[tag:]
        pos = 1
        fig = plt.figure()
        for file_name in temp:
            path = os.path.join(folder_path,file_name)
            G = nx.read_gml(path)

            ax = fig.add_subplot(tag,1,pos)
            ax.set_title(G.name)
            data = [G[x][y]['weight'] for x, y in G.edges()]
            plt.hist(data, bins=10)
            pos+=1
            #s.GraphAnalysisByEdge(G)
            #G = s.StockMarketCommunity(G,pos_threshold=0.9,neg_threshold=-0.5)
            #nx.draw_networkx(G)
        plt.show()

    #s.ReadInGraph()
if __name__ =='__main__':
    EdgeDistributionAnalysis()