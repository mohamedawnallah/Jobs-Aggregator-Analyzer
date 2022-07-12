# ✨ Background
We're looking to better understand what **skills**, **expected market salary** for **data jobs based on seniority level** to learn the most in-demand ones and to be fairly paid too also see **if the given data job are going more in-demand** and **how positively or negatively people talking about on twitter platform**. We felt the best places to start are job search platforms and twitter, so this is our start at this project.

# 💡 Data Jobs Research Features
- Getting the latest data jobs based on the given job title [Duplication in Consideration] and many other filters criteria(country,remote,seniority, ...etc).
- Getting the latest data job requirements based on the given job title and many other filter criterias.
- Analyzing the jobs skills/degrees requirements through visualizations📈📉.
- Implementing APIs for our project so end-users/BI-users can implement their own analysis and getting other insights📊
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
- As a BI/frontend user, I want to get the latest data jobs based on my given inputs(e.g: job_title) and the available search filters from the available APIs so that I keep aware of available jobs in my area.
- As a BI/Data-Science/frontend user, I want to get the most in-demand job skills/degree required for my given job title and the available search filters from the available APIs so that I keep my data skills up-to-date and always in-demand.
- As a BI/Frontend user, I want to see good documented APIs and hosted somewhere(e.g: our frontend website, github, ...etc) so that I can make most use of the available functionalities provided by the APIs also use it properly.
- As a(an) User/Employer/Company, I want to see interactive visualizations regards data job skills on a frindly, user-experienced, fast connection website so that I'm aware about current market research in data area also if employer/company I could hire the most in-demand skills so there are no shortage of talents who have these skills.
- As a User, I want to see interactive visualizations regards  data jobs which are in-demand so that I keep on top of the market and keep up-to-date to the market demand.
- As a User/Data-Geek, I want to subscripe to data jobs email newsletter so that I keep aware of the latest jobs posted in my data area.
- As a User/Data-Geek/Employer/Company, I want to subscripe to data skills email newsletter so that I keep aware of the most in-demand job skills required in my specific data area.
- As a User, I want to share visualizations that are interesting for me in a good represented way and the link's meaningful/shortened as possible on my social media accounts so that I could help other people with the given insights inside the visualizations also to grow my community.
- As a User/Data-Geek, I want to see professional people's opinions about my career (positively and negatively) and its expected growth so that I get insights from these opinions and build on top of that.
- As a Business-User, I want to see use case diagrams so that I get idea what are use cases available in this system without exposure to tehnical stuffs.
- As a Talents-Recruiter/(Data)Hiring-Manager/Data-Engineer, I want to see usecase diagrams, classes and relationships diagrams(if applicable for business users), data visualizations, skills used, APIs, Frontend-Website, Data Quality last but not the least running all tests fast and efficently (Hopefully all's passed).

# 🏗 Architecture
![Architecture](https://github.com/mhmdawnallah/Data-Jobs-Research/blob/feature/diagrams/Architecture.png)

# 🏢 Data Warehouse Schema Design
![Data Warehouse Schema Design](https://github.com/mhmdawnallah/Data-Jobs-Research/blob/feature/diagrams/Data%20Warehouse%20Schema%20Design.png)


Collect Requirements (Brainstorming):
    - Oxford Definition: a thing that is needed or wanted.
    - Identify the problems we wanna solve
    - Clarify the functionality required to solve the problems
    - Document important decisions
    - Functional Requirements:
        - Represent the Features
        - Define how to react to an input
        - Determine the expected behavior
    - Non-Functional Requirements:
        - Are not directly related to the features of the system but important nonetheless
        - Performance Requirements
        - Legal/Regulations Requirements (e.g:Does the app collect sensitive data)
        - Documentation
Descripe the Software from the user prospective:
    - Agile Or Waterfall
    - Create wireframes and prototypes if needed
Identify the classes:
    - Playing Entities
Create Diagrams:
    - Use Case Diagrams for business people
    - Class Diagrams for technical people
    - Sequence daigrams for dynamic ones and interaction between objects
    - Activity Diagrams
    - Statechart Diagrams