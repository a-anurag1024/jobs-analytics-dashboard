A simple streamlit powered dashboard to show the analytics for the Data Science Job Market Demand Analysis Project. This Dashboard is linked with the data collected using the [Jobs Advertisement Scrapper](https://github.com/a-anurag1024/li_jobs_collector) and mined using [Jobs Data Mining](https://github.com/a-anurag1024/jobs-data-mining).


![](https://github.com/a-anurag1024/jobs-analytics-dashboard/blob/main/demo.gif)

# Structure:-

1. **Skills Analytics** :- Visualizes the Ranked Skill cluters and their weigthages for the given Job filters.
2. **Jobs Analytics** :- Basic EDA on the jobs data collected to get an understanding of the job filters.
3. **Clusters Analytics** :- Metadata on the skill clusters formed and being used in the skills analytics tab.


# Usage:-

-   The dashboard is dependent on the db created in [Jobs Advertisement Scrapper](https://github.com/a-anurag1024/li_jobs_collector) and modified in [Jobs Data Mining](https://github.com/a-anurag1024/jobs-data-mining). So, before starting the analytics dashboard application, this MySQL DB container has to be running.
-   To setup the environment, 

```bash
git clone https://github.com/a-anurag1024/jobs-analytics-dashboard.git
cd jobs-analytics-dashboard
pip install -e .
```

-   To start the dashboard,

```bash
streamlit run app.py
```