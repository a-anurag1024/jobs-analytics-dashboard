import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from wordcloud import WordCloud, STOPWORDS

from dashboard.plots.base_plotter import BasePlotter

class SkillsPlotter(BasePlotter):
    def __init__(self):
        super().__init__()
        self.df = None
        self.cluster_df = None
        self.wordcloud = WordCloud(width = 800, height = 800, 
                                   background_color ='white', 
                                   stopwords = set(STOPWORDS), 
                                   min_font_size = 10)
        self.plots_list = [self.plot_ranked_skill_clusters,
                           self.get_ranked_skills_df,
                           self.get_cluster_tags_df]
    
    
    def process_df(self, df, cluster_df, ranking_weightage=0.2):
        """
        
        Parameters:
        -----------
        df: pd.DataFrame
            dataframe containing job_id, skill, skill_rank, cluster_id
        cluster_df: pd.DataFrame
            dataframe containing cluster_id, cluster_tags, cluster_head_tag
        ranking_weightage: float (0-1)
            amount of weightage to give to the skill_rank. If 0, only cluster_id will be considered.
            If 0.2, then rank-1 skill will have 1.0 weightage and rank-10 will have 0.8 weightage.
            Defaults to 0.2
        """
        df['skill_weightage'] = 1 - (df['skill_rank'] - 1) * ranking_weightage / 10
        cluster_name_map = dict(zip(cluster_df['cluster_id'], cluster_df['cluster_head_tag']))
        df['cluster_name'] = df['cluster_id'].apply(lambda x: cluster_name_map[int(x)])
        gdf = df.groupby(['cluster_name']).agg({'skill_weightage': 'sum'}).reset_index()
        self.df = gdf
        self.cluster_df = cluster_df
    
    
    def plot_ranked_skill_clusters(self):
        fig = px.pie(self.df, names="cluster_name", values="skill_weightage", title="Ranked Skill Clusters")
        return fig
    
    
    def json_to_commasep(self, x):
        lis = json.loads(x)
        return ', '.join(lis)
    
    
    def get_ranked_skills_df(self):
        self.cluster_df['cluster_tags'] = self.cluster_df['cluster_tags'].apply(self.json_to_commasep)
        self.cluster_df['cluster_name'] = self.cluster_df['cluster_head_tag']
        return self.df.merge(self.cluster_df, left_on='cluster_name', right_on='cluster_name', how='left')[['cluster_name', 'cluster_tags', 'skill_weightage']].sort_values(by='skill_weightage', ascending=False).drop_duplicates(subset='cluster_name').reset_index(drop=True)
    
    
    def get_cluster_tags_df(self):
        return self.cluster_df[['cluster_id', 'cluster_head_tag', 'cluster_tags']]

    
    def plot_cluster_wordcloud(self, cluster_id: int, skills_df: pd.DataFrame):
        skills = ", ".join(skills_df[skills_df['cluster_id'] == str(cluster_id)]['skill'].values.tolist())
        fig, ax = plt.subplots(figsize = (12, 8))
        if len(skills) == 0:
            return fig
        wc_fig = self.wordcloud.generate(skills)
        ax.imshow(wc_fig)
        plt.axis("off")
        return fig