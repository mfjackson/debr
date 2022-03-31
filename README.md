# debr - a basic Python API wrapper for randomuser.me

## 0. How to use

This library assumes the user already has Python 3 installed. To run the primary data extraction step, install the 
libraries in the `requirements.txt` and run the following code from `debr` root directory:

```
python ./debr/etl/extract.py
```

## 1. Data Model

### Tables
I chose to split up the randomuser.me data into the following tables:

1. `users`
2. `logins`
3. `media`
4. `timezones`
5. `countries`
6. `altids`

See erd.pdf for a document displaying the tables and their relationships.

### Design Rationale

- Kept location data paired with user attribute data because the user's address information can largely be 
  considered as occupying the same level of granularity as the other attributes. One could make an argument for cities
  and/or countries to be placed in a separate table, but replacing these attributes with `int` codes in the `users` 
  table would make it more difficult for analysts who want to run queries against the `users` table with respect to 
  cities or countries given that there could be over 100 country codes and thousands of city codes.
- I did separate out timezone attributes into a separate table given that there are a limited number of these codes
- Not including plain text passwords in the `logins` table.
- Only including SHA256 because it's the most secure of the three hashing algorithms. Can include the others if 
  necessary.
- Separated out the alternative IDs from the `users` table because some ID types seem sensitive (e.g. SSN).
- Assuming `login_uuid` is a UUID that mimics Branch having created a UUID for each individual. In the case that 
  this was an external UUID, we would want to have the database that we're loading users to generate a branch 
  specific UUID (and/or a serializable primary key) and change the randomuser.me column name to `login_external_uuid`

## 2. End to End Pipeline

### RandomUser Class

I created a `RandomUser` class containing methods to make GET requests to randomuser.me and return a pandas 
DataFrame. This class is called in the `extract.py` file located in the etl folder.

#### Potential considerations and improvements

- This assumes we're handling relatively small amounts of data. If we were handling larger data, PySpark may be 
  advantageous to use over pandas.
- Primary keys should typically be created by the database itself, but we're creating an artificial `timestamp_code` 
  primary key for the `timestamps` table.

## 3. ETL in production

### Design

#### ETL vs. ELT

- ETL with Python allows for more complex transformations.
- ELT does better with larger datasets.
- Decision also depends on who is responsible for translating the business logic to code within the organization.

#### Batch Processing

- Would lean towards using Airflow for orchestration.
- Depending on who's responsible for implementation of data transformations, decide whether to use DBT, e.g. if 
  analysts, then use DBT because business logic can be more easily translated to code by those who work with it 
  every day.
- Create Docker images that can be spun up as containers when used in conjunction with Airflow's 
  `KubernetesPodOperator`. This would allow for a scalable process, as well as more rigorous dependency management.

#### Loading output data to a database

- The choice of a database and how its tables are configured are largely dependent upon the database's use case (e.g. 
  analytics vs. serving as an API endpoint for external users). 
- If setting up a produciton DB such as MySQL or PostgreSQL from scratch, I would use Python and sqlalchemy to 
  create the schema described in the ERD (assuming this was agreed upon as the best methodology by the rest of the 
  team).
- If loading data to an existing database where the schema is created by something other than Python, I would ensure 
  that a process exists whereby Pydantic classes are updated when the externally defined schema is updated.

#### Backing up our data

- Should have a regular nightly backup process to dump database (e.g. `pg dump`) to some form of cloud storage (e.g. 
  S3 or GCS)

### Testing, Data Validation, and Alerts

#### Testing

- If given more time, I would write a full library of unit tests and would build integration tests if written for a 
  production pipeline.
- Use sample data for local testing. 
- Create script to run `pytest` when creating a PR.

#### Data Validation

- Validating data within an ETL/ELT process ensures (to a large degree) that silent failures won't occur and affect 
  downstream processes such as dashboards or data fed to a web application.
- In addition to using Pydantic, I would use [Great Expectations](https://greatexpectations.io/) in production to 
  perform intermediate data validations within the structure of the DAG. This validation framework has a number of 
  built-in data validations, as well as the ability to create custom expectations surrounding data quality.

#### Alerts

- Alerting Data Engineers to the failure of a DAG task is crucial to quickly resolving the issue that causes the 
  failure. If using Airflow (and assuming Branch uses Slack), I would recommend setting up a Slack.
