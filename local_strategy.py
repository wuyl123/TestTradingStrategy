from typing import List, Dict
from datetime import datetime

from vnpy.trader.utility import ArrayManager
from vnpy.trader.object import BarData
from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine
from vnpy_portfoliostrategy.utility import PortfolioBarGenerator

import numpy as np

import statsmodels.api as sm 
from statsmodels.tsa.stattools import adfuller
import pandas as pd

import csv

def cal_beta(x,y):
    model = sm.OLS(x, sm.add_constant(y)).fit()  
    beta = model.params[1]
    return beta

# 协整检验  
def cointegration_test(series1, series2):  
    model = sm.OLS(series1, sm.add_constant(series2)).fit()  
    residuals = model.resid  
    adf_result = adfuller(residuals)  
    return adf_result[1] 


class LocalStrategy(StrategyTemplate):
    '''编制自己的策略'''

    # 策略作者
    author = "Yuelin Wu"
    current_spread = 0.0

    def __init__(
        self,
        strategy_engine: StrategyEngine,
        strategy_name: str,
        vt_symbols: List[str],
        setting: dict
    ):
        """"""
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)
        self.ams: Dict[str, ArrayManager] = {}
        for vt_symbol in self.vt_symbols:
            self.ams[vt_symbol] = ArrayManager(size=3000)
        self.pbg = PortfolioBarGenerator(self.on_bars)
        self.beta: float = None
        self.spread_data: np.ndarray = np.zeros(3100)
        self.signal: int = 0
        # Obtain contract info
        self.leg1_symbol, self.leg2_symbol = vt_symbols
        self.Zscore: float = None

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bars(10)

    def on_start(self) -> None:
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self) -> None:
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")
        
        self.put_event()

    def on_bars(self, bars: Dict[str, BarData]):

        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            am.update_bar(bar)

            if not am.inited:
                return

        # 获取期权腿K线
        leg1_bar = bars.get(self.leg1_symbol, None)
        leg2_bar = bars.get(self.leg2_symbol, None)

        # 必须两条期权腿行情都存在
        if not leg1_bar or not leg2_bar:
            return
        # 每4小时重置一次
        if (leg1_bar.datetime.hour + 1) % 4 == 0 or self.beta is None:
            self.beta = cal_beta(self.ams[self.leg1_symbol].close,self.ams[self.leg1_symbol].close)

        # 计算当前spread
        self.current_spread = leg1_bar.close_price - self.beta*leg2_bar.close_price 

        # 更新到价差序列
        self.spread_data[:-1] = self.spread_data[1:]
        self.spread_data[-1] = self.current_spread

        # 计算Z-score  
        lookback = 3000
        Mean = self.spread_data[lookback:].mean()  
        Std = self.spread_data[lookback:].std()  
        self.Zscore = (self.current_spread - Mean)/ Std 

        # z_score = round(spread-self.mu)
        # 每五天显示一次z_score
        if (leg1_bar.datetime.day + 1) % 5:
            # print(f'当前标准差为{self.sigma}')
            # print(f'z_score汇报: 当前z_score为{z_score}, bete = {self.beta}, spread = {spread}, A = {leg1_bar.close_price},B = {leg2_bar.close_price}')
            # print(f'当前持仓为{self.get_pos(self.leg1_symbol)}')
            pass
        current_pos = self.get_pos(self.leg1_symbol)
        if not current_pos:
            if self.Zscore >= 2.0:
                self.signal = -1
                # self.pos_data()
                self.set_target(self.leg1_symbol,-1)
                self.set_target(self.leg2_symbol,self.beta)
            elif self.Zscore <= -2.0:
                self.signal = -1
                # print(f'当前z_score为{z_score},开始调仓')
                self.set_target(self.leg1_symbol,1)
                self.set_target(self.leg2_symbol,-self.beta)
            else:
                self.signal = 0
        else:
            self.signal = 0
            # print(f'current pos is {self.leg1_symbol}:{self.get_pos(self.leg1_symbol)},  {self.leg2_symbol}:{self.get_pos(self.leg2_symbol)}')
            if abs(self.Zscore)<0.5:
                # print(f'当前z_score为{z_score},开始平仓')
                self.set_target(self.leg2_symbol,0)
                self.set_target(self.leg1_symbol,0)  

        
        # 写入CSV文件
        with open('plt_data.csv', 'a+', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            data = [self.Zscore.tolist(),self.signal]
            writer.writerow(data)        
        self.rebalance_portfolio(bars)
        self.put_event()
