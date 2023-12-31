
from AlgorithmImports import *

class EMAMomentumUniverse(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2020, 1, 7)
        self.SetEndDate(2023, 4, 1)
        self.SetCash(25000)

        # brokerage
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        # universe
        self.symbols = self.AddEquity("AMZN", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Raw
        self.AddUniverseSelection(ManualUniverseSelectionModel(self.symbols))

        # indicator
        fast_period = self.GetParameter("ema-fast", 18)
        slow_period = self.GetParameter("ema-slow", 59)

        self.fast = self.SMA(self.symbols, fast_period, Resolution.Daily)
        self.slow = self.SMA(self.symbols, slow_period, Resolution.Daily)

        self.SetExecution(ImmediateExecutionModel())


    def OnData(self, data):

        self.Plot("Levels", "Asset Price", self.Securities["AMZN"].Price)
        #self.PlotIndicators("Levels", self.fast, self.slow)

        if not self.fast.IsReady and not self.slow.IsReady:
            return

        fast = self.fast.Current.Value
        slow = self.slow.Current.Value

        if fast > slow:
            self.Log("BUY  >> {0}".format(self.Securities[self.symbols].Price))
            self.MarketOrder("AMZN", 3)

        if fast < slow:
            self.Log("SELL >> {0}".format(self.Securities[self.symbols].Price))
            self.MarketOrder("AMZN", -3)
