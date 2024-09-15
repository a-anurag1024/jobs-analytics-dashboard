import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from dashboard.db import DataFetcher, DBCreds
from dashboard.plots.jobs_plotter import JobsPlotter
from dashboard.plots.skills_plotter import SkillsPlotter
from dashboard.filter_data import FilterDBs


# MySQL datafetcher
db_creds = DBCreds(
    host="localhost",
    port="3306",
    user="local",
    password="local",
    database="jobs_data"
)
db_data = DataFetcher(db_creds)


# Plotters
jobs_plotter = JobsPlotter()
skills_plotter = SkillsPlotter()


# Streamlit application
def main():
    # Set page title
    st.set_page_config(page_title="Jobs Analytics Dashboard")
    
    # Get tabs
    tab1, tab2, tab3 = st.tabs(['Skills Analytics', 'Jobs Analytics', 'Clusters Analytics'])

    # Date Range
    with st.sidebar.expander("Data Collection Date Range"):
        start_date = st.date_input("Start Date", pd.to_datetime('2021-01-01'))
        end_date = st.date_input("End Date", pd.to_datetime('2025-12-31'))

    # Fetch data from MySQL table
    jobs_data = db_data.fetch_jobs_bw_dates(start_date, end_date)
    skills_data = db_data.fetch_skills_bw_dates(start_date, end_date)
    clusters_data = db_data.fetch_skill_clusters()
    
    # Jobs Filters and filter the data
    Filter = FilterDBs(jobs_data, skills_data)
    st.sidebar.title("Jobs Filters")
    filters = {}
    filters['Seniority Level'] = st.sidebar.multiselect("Seniority Level", Filter.get_options('seniority_level'), default=['All'])
    filters['Employment Type'] = st.sidebar.multiselect("Employment Type", Filter.get_options('employment_type'), default=['All'])
    filters['Job Function'] = st.sidebar.multiselect("Job Function", Filter.get_options('job_function'), default=['All'])
    filters['Industries'] = st.sidebar.multiselect("Industries", Filter.get_options('industries'), default=['All'])
    jobs_db, skills_db = Filter.get_filtered_dbs(filters)
    
    # skills ranking weightage
    st.sidebar.title("Skills Ranking Weightage")
    ranking_weightage = st.sidebar.slider("Ranking Weightage", 0.0, 1.0, 0.1)
    
    
    
    # Plot jobs metadata histograms
    with tab2:
        jobs_plotter.process_df(jobs_db)
        job_charts = jobs_plotter.generate_plots()
        for fig in job_charts:
            st.plotly_chart(fig)
        top_k_sliders = {}
        for i, func in enumerate(jobs_plotter.treemaps_list):
            top_k_sliders[i] = st.slider(f"Top N {func.__name__.replace('plot_top', '').replace('function', '')}", 1, 100, 50)
            fig = func(top_n=top_k_sliders[i])
            st.plotly_chart(fig)


    # Plot skills plots
    skills_plotter.process_df(skills_db, 
                              clusters_data,
                              ranking_weightage)
    skill_charts = skills_plotter.generate_plots()
    with tab1:
        st.plotly_chart(skill_charts[0])
        st.dataframe(skill_charts[1], hide_index=True, use_container_width=True)

    with tab3:
        st.write("Wordclouds for each Skills cluster")
        cluster_id = st.selectbox("Select Cluster ID", clusters_data['cluster_id'])
        st.pyplot(skills_plotter.plot_cluster_wordcloud(cluster_id, skills_db))
        st.write("Cluster-ids and their tags for reference")
        st.dataframe(skill_charts[2], hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()