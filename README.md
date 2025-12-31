本项目主要分为三部分：**数据获取**，**策略建立**，**策略回测**  

**数据获取**  

数据获取：获得2010年分钟线的BTC和ETH数据，在binance-public-data-master文件夹下调用获取k-lines数据，保存为BTCUSDT.csv以及ETHUSDT.csv 
在CreateFakeData.ipynb中介绍了如何生成人造数据，数据保存在FakeA.csv和FakeB.csv中

**策略建立**  
策略在local_strategy.py中，详细信息参加源代码

**策略回测**  
真实数据回测见backTest.ipynb，人造数据回测见simulation.ipynb  
回测结果包含：Pnl,Zscore,成交明细，净值/回撤曲线，费用占比
