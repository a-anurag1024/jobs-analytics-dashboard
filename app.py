import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.db import DataFetcher, DBCreds
from dashboard.plots.jobs_plotter import JobsPlotter



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


# Streamlit application
def main():
    # Set page title
    st.set_page_config(page_title="Jobs Analytics Dashboard")

    # Add sidebar
    st.sidebar.title("Date Range")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    # Fetch data from MySQL table
    data = db_data.fetch_data_bw_dates(start_date, end_date)

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Plot histogram
    job_charts = jobs_plotter.return_plots(df)
    for fig in job_charts:
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()