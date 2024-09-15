import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from dashboard.db import DataFetcher, DBCreds
from dashboard.plots.jobs_plotter import JobsPlotter
from dashboard.plots.skills_plotter import SkillsPlotter



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

    # Add sidebar
    # Date Range
    st.sidebar.title("Date Range")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    # skills ranking weightage
    st.sidebar.title("Skills Ranking Weightage")
    ranking_weightage = st.sidebar.slider("Ranking Weightage", 0.0, 1.0, 0.1)

    # Fetch data from MySQL table
    jobs_data = db_data.fetch_jobs_bw_dates(start_date, end_date)
    skills_data = db_data.fetch_skills_bw_dates(start_date, end_date)
    clusters_data = db_data.fetch_skill_clusters()
    
    # To do: Add Jobs Filters and filter the data
    
    
    # Plot jobs metadata histograms
    with tab2:
        jobs_plotter.process_df(jobs_data)
        job_charts = jobs_plotter.generate_plots()
        for fig in job_charts:
            st.plotly_chart(fig)


    # Plot skills plots
    skills_plotter.process_df(skills_data, 
                              clusters_data,
                              ranking_weightage)
    skill_charts = skills_plotter.generate_plots()
    with tab1:
        st.plotly_chart(skill_charts[0])
        st.dataframe(skill_charts[1], hide_index=True, use_container_width=True)

    with tab3:
        st.write("Wordclouds for each Skills cluster")
        cluster_id = st.selectbox("Select Cluster ID", clusters_data['cluster_id'])
        st.pyplot(skills_plotter.plot_cluster_wordcloud(cluster_id, skills_data))
        st.write("Cluster-ids and their tags for reference")
        st.dataframe(skill_charts[2], hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()