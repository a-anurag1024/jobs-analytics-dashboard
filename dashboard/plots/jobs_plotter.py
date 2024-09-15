from dashboard.plots.base_plotter import BasePlotter
import plotly.express as px
import pandas as pd

class JobsPlotter(BasePlotter):
    def __init__(self):
        super().__init__()
        self.df = None
        self.plots_list = [self.plot_seniority_level,
                           self.plot_employment_type,
                           self.plot_job_function,
                           self.plot_industries]
    
    
    def process_df(self, df):
        self.df = df
    
    
    def plot_seniority_level(self):
        fig = px.histogram(self.df, y="seniority_level", title="Seniority Levels")
        return fig
    
    
    def plot_employment_type(self):
        fig = px.pie(self.df, names="employment_type", title="Employment Type")
        return fig
    
    
    def plot_job_function(self):
        # Create a bubble chart
        sdf = self.df.groupby(['job_function']).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index(drop=True)
        fig = px.treemap(sdf, path=["job_function"], values="counts", title="Job Functions")
        return fig
    
    
    def plot_industries(self):
        # Create a bubble chart
        sdf = self.df.groupby(['industries']).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index(drop=True)
        fig = px.treemap(sdf, path=["industries"], values="counts", title="Job industries")
        return fig
    