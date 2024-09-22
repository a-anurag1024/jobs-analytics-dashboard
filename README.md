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


## A Note on the Skills Ranking Weightage adjustment

-   While extracting the top 10 skills from a job post, the LLM was asked to rank the skills (most relevant to least relevant) using the contextual information in the job post.
-   The given Ranking Weightage adjustment is given to decide how much of relevance this ranking given by the LLM needs to be considered. 
-    A value of 0 will give no relevance to the ranking and a value of 1 will give highest possible relevance to the ranking.
-   This adjustment is used to calculate the weightage of an occurence of a skill in a job post as:-
$$ \text{Skill Weightage} = 1 - \left( \text{skill rank} - 1 \right) \times \text{Skill Ranking Weightage} \times 0.1 $$

