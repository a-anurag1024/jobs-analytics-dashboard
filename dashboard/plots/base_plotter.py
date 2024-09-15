from abc import ABC, abstractmethod
import pandas as pd
import plotly


class BasePlotter(ABC):
    def __init__(self):
        self.plots_list = []
    
    
    @abstractmethod
    def process_df(self):
        """
        Process the dfs and cache them for plotting
        """
        pass
    
    
    def generate_plots(self):
        plots = []
        for plot in self.plots_list:
            fig = plot()
            plots.append(fig)
        return plots