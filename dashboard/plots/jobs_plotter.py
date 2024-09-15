from dashboard.plots.base_plotter import BasePlotter
import plotly.express as px
import pandas as pd

from wordcloud import WordCloud, STOPWORDS

class JobsPlotter(BasePlotter):
    def __init__(self):
        super().__init__()
        self.df = None
        self.wordcloud = WordCloud(width = 800, height = 800, 
                                   background_color ='white', 
                                   stopwords = set(STOPWORDS), 
                                   min_font_size = 10)
        self.plots_list = [self.plot_seniority_level,
                           self.plot_employment_type,
                           self.plot_job_title_wordcloud
                           ]
        self.treemaps_list = [self.plot_top_job_function,
                              self.plot_top_industries,
                              self.plot_top_companies]
    
    
    def process_df(self, df):
        self.df = df
    
    
    def plot_seniority_level(self):
        fig = px.histogram(self.df, y="seniority_level", title="Seniority Levels")
        return fig
    
    
    def plot_employment_type(self):
        fig = px.pie(self.df, names="employment_type", title="Employment Type")
        return fig
    
    
    def plot_top_job_function(self, top_n=50):
        # Create a bubble chart
        sdf = self.df.groupby(['job_function']).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index(drop=True)
        fig = px.treemap(sdf.head(top_n), path=["job_function"], values="counts", title=f"Top {top_n} Job Functions")
        return fig
    
    
    def plot_top_industries(self, top_n=50):
        # Create a bubble chart
        sdf = self.df.groupby(['industries']).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index(drop=True)
        fig = px.treemap(sdf.head(top_n), path=["industries"], values="counts", title=f"Top {top_n} Job industries")
        return fig
    
    
    def plot_job_title_wordcloud(self):
        job_titles = ", ".join(self.df['job_title'].values.tolist())
        if len(job_titles) == 0:
            # return an empty figure
            return px.imshow(pd.DataFrame())
        wc_fig = self.wordcloud.generate(job_titles)
        fig = px.imshow(wc_fig)
        fig.update_layout(title="Job Titles Wordcloud")
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(showlegend=False)
        return fig
    
    
    def plot_top_companies(self, top_n=50):
        # Create a bubble chart
        sdf = self.df.groupby(['company']).size().reset_index(name='counts').sort_values(by='counts', ascending=False).reset_index(drop=True)
        fig = px.treemap(sdf.head(top_n), path=["company"], values="counts", title=f"Top {top_n} Companies")
        return fig