# ✨ Background
We're looking to better understand **what skills, expected market salary for jobs based on seniority level?** to learn the most in-demand ones and to be fairly paid too also see **if the given data job title is going more in-demand?** and **how positively or negatively people talking about on twitter platform?**. We felt the best places to start are job search platforms and twitter, so this is our start at this project.

# 💡Jobs Aggregator Analyzer Features
- Getting the latest jobs based on the given job title [Duplication in Consideration] and many other filters criteria(country,remote,seniority, ...etc).
- Getting the latest job requirements based on the given job title and many other filter criterias.
- Analyzing the jobs skills/degrees requirements through visualizations 📈 📉.
- Implementing APIs for our project so end-users/BI-users can implement their own analysis and getting other insights 📊
- Seeing if the given job title in-demand's increasing or not through many criterias(e.g: jobs posted on different times, ...etc)
- Seeing people's opinions about the given job title specially on twitter platform through its given third party API.
- Implementing a wonderful landing page on our frontend website.
- Adding our APIs docs on our frontend website.
- Implementing email subscription newsletter so user could get the latest updates of his registered job title also his seniority level on regular basis in a generated pdf report.
- Implementing selection sites feature in our frontend website so use choose specific websites he wants to aggregate jobs from.
- Implementing url-shortener so user could share interesting visualizations, jobs on his social media platforms (e.g: Linkedin, ...etc).
- Implementing powerful search program on our frontend website to filter jobs based on user input e.g:(year,country,salary,company_reviews, ...etc).
- Submitting feedback feature about our service in our frontend website.
- Forecasting, if possible, the skills that will be in greater or lesser demand in the next year.
- Documenting our project along the way.

# 🎯 End-Goals (User-Stories)
- As a BI/frontend user, I want to get the latest jobs based on my given inputs(e.g: job_title) and the available search filters from the available APIs so that I keep aware of available jobs in my area.
- As a BI/Data-Science/frontend user, I want to get the most in-demand job skills/degree required for my given job title and the available search filters from the available APIs so that I keep my job skills up-to-date and always in-demand.
- As a BI/Frontend user, I want to see good documented APIs and hosted somewhere(e.g: our frontend website, github, ...etc) so that I can make most use of the available functionalities provided by the APIs also use it properly.
- As a(an) User/Employer/Company, I want to see interactive visualizations regards data job skills on a frindly, user-experienced, fast connection website so that I'm aware about current market research in data area also if employer/company I could hire the most in-demand skills so there are no shortage of talents who have these skills.
- As a User, I want to see interactive visualizations regards  data jobs which are in-demand so that I keep on top of the market and keep up-to-date to the market demand.
- As a User/Data-Geek, I want to subscripe to data jobs email newsletter so that I keep aware of the latest jobs posted in my data area.
- As a User/Data-Geek/Employer/Company, I want to subscripe to data skills email newsletter so that I keep aware of the most in-demand job skills required in my specific data area.
- As a User, I want to share visualizations that are interesting for me in a good represented way and the link's meaningful/shortened as possible on my social media accounts so that I could help other people with the given insights inside the visualizations also to grow my community.
- As a User/Data-Geek, I want to see professional people's opinions about my career (positively and negatively) and its expected growth so that I get insights from these opinions and build on top of that.
- As a Business-User, I want to see use case diagrams so that I get idea what are use cases available in this system without exposure to tehnical stuffs.
- As a Talents-Recruiter/(Data)Hiring-Manager/Data-Engineer, I want to see usecase diagrams, classes and relationships diagrams(if applicable for business users), data visualizations, skills used, APIs, Frontend-Website, Data Quality last but not the least running all tests fast and efficently (Hopefully all's passed).

<!-- # Contents

- [The Data Set](#the-data-set)
- [Data Pipeline Architecture](#⇔-data-pipeline-architecture)
- [Data Warehouse Schema Design](#🏢-data-warehouse-schema-design)
- [Used Tools](#used-tools)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
- [Pipelines](#pipelines)
  - [Stream Processing](#stream-processing)
    - [Storing Data Stream](#storing-data-stream)
    - [Processing Data Stream](#processing-data-stream)
  - [Batch Processing](#batch-processing)
  - [Visualizations](#visualizations)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)
- [Appendix](#appendix)

# Pipelines
- Explain the pipelines for processing that you are building
- Go through your development and add your source code -->
# ⇔ Data Pipeline Architecture
![Data Pipeline Architecture](assets/data-pipeline-architecture.png)
# 🏢 Data Warehouse Schema Design Process
The schema design process is a crucial step in the development of a database. It involves creating a blueprint for how data will be organized and stored in the database. This process typically starts with a conceptual data model and progresses through logical and physical data models.

## Conceptual Data Model
The conceptual data model is the highest level of abstraction in the schema design process. It defines the main entities and relationships within the system, without worrying about specific details such as data types or constraints. The conceptual data model is typically created using a diagramming tool such as Entity-Relationship (ER) diagrams.

![Conceptual Data Model](assets/conceptual-data-model.png)

In this example, the conceptual data model consists of three entities: "Job Dimension," "Job Platform Dimension", "Date Dimension", "Location Dimension", and "Company Dimension" The relationships between the entities are represented by the lines connecting them, with the labels indicating the nature of the cardinality (minimum cardinality, maximum cardinality) (e.g., "1,N" for minimum cardinality 1 and maximum cardinality many).

The attributes of each entity's represented by an oval for the following entities:

### Job Data Model
![Job Data Model](assets/job-data-model.png)

### Company Data Model

![Company Data Model](assets/company-data-model.png)

### Location Data Model

![Location Data Model](assets/location-data-model.png)

### Date Data Model

![Date Data Model](assets/date-data-model.png)


## Logical Data Model

Jobs Factless Fact Table Data Model

![Jobs Factless Fact Table Data Model](assets/jobs-factless-fact-table-data-model.png)

## Physical Data Model
# Conclusion
- How did this project turn out
- What major things have you learned
- What were the biggest challenges

<!-- ## Connect
## Buffer
## Processing
## Storage
## Visualization
## Stream Processing
### Storing Data Stream
### Processing Data Stream
## Batch Processing
## Visualizations

# Demo
- You could add a demo video here
- Or link to your presentation video of the project

# Conclusion
Write a comprehensive conclusion.
- How did this project turn out
- What major things have you learned
- What were the biggest challenges

# Follow Us On
Add the links to our LinkedIn Profiles
https://www.linkedin.com/in/mohamedawnallah/

# Appendix -->
