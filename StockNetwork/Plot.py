#coding:utf-8
from code.CommonLib import Cache
import matplotlib.pyplot as plt

stock_list = ['600369',
              #'600958',
              '601788',
              #'600030',
              #'601901',
              #'601555',
              #'601688',
              #'600837',
              #'600999',
              #'601099',
              '601377']
# 创建子图
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()
plt.title(r"test")
plt.xlabel(r"time")
plt.ylabel(r"p_change")
plt.grid()
for stock in stock_list:
    print stock
    stock_data = Cache.GetStockHistory(stock_id = stock,start = '2018-02-17',end = '2018-04-18')['p_change']
    plt.plot(stock_data,label = stock)
    plt.legend()
plt.show()