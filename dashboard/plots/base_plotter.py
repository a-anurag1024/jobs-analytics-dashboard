from abc import ABC, abstractmethod
import pandas as pd
import plotly


class BasePlotter(ABC):
    def __init__(self):
        self.plots_list = []
    
    
    def return_plots(self, df: pd.DataFrame):
        plots = []
        for plot in self.plots_list:
            fig = plot(df)
            plots.append(fig)
        return plots