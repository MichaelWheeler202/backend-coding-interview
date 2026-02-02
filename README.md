# Clever's Backend Engineering Challenge - Michael Wheeler's Answer

👋 Hello to you too!

<details>
<summary style="font-size: 24px;"> My thoughts: Describing My Approach and Choices </summary>

<h3> Core Requirements: What to do? </h3>
<ul>
<li>Ingest and store the provided photo data (photos.csv)
    <ul>
    <li>Create DB and load the file into it. </li>
    </ul>
</li>

<li>Implement user authentication and authorization
    <ul>
    <li>I'm going to use Github SSO for this approach.  In general I'm a fan of SSO as it reduces our need to handle sensitive information like passwords.  I used github specifically because I know you guys reviewing this have github accounts already.  For a true prod app meant for everyday people google SSO may be better.  If we had to handle account creation ourselves I'd want to make sure we only stored a salted hash of the password and had two step verification for emails to ensure the user owns them.  If we were storing sensitive data such as healthcare related images, I would also want to add two-factor authentication for logging in.)</li>
    </ul>
</li>
<li>Provide API endpoints for managing and accessing photos</li>
<li>Include comprehensive API documentation</li>
<li>Write tests for your implementation</li>
</ul>

<h3> What We Want to See: My Goals </h3>
For developing this app whenever developing true production functionality would be difficult without having
the correct infrastructure available I will add a TODO with my explanation of what I would do to improve the design.

<h3> Technology Choices </h3>
Backend Framework: Although I'm most proficient in spring boot I'll be using Django for this as I am quite familiar
with python and would prefer to develop something more like what I would make in the workplace.  I also want to use
this as a chance to learn what the equivalents of my usual tech stack are in python.

Database: In this application it doesn't appear we have data assigned to users, we just need them to be signed in.  If we
can avoid storing any data on users themselves, that leaves us with the image related data.  Here are my observations and thoughts on the image data.
<ul>
<li>Our data is structured.</li>
<li>We are not storing the image itself, but rather urls to the images, this reduces our storage burden heavily.</li>
<li>We must provide endpoints for managing and accessing photos. This means we will have reads and writes, the ratio is unclear.</li>
<li>Our data doesn't have any complicated relations, or even relations at all.</li>
<li>It isn't clear from the requirements whether consistency is important.</li>
</ul>
My DB choice is PostgreSQL  -- TODO although PostgreSQL is chosen to get a demo up and running I'll start with SQLite
<ul>
<li>Tables hold structure data</li>
<li>Foreign keys can be used to relate photographers to photos instead of having redundant photographer data</li>
<li>ACID compliant</li>
</ul>

Documentation: Similar to my experience with java it looks like open api is an option here.  I will go with that as it's what
I am familiar with and does an effective job at documentation.

Testing - Used built in testing framework


What I would do if I had more time/resources list:
- Add Caching - if the data being fresh is critical I would use a distributed caching so that if one app makes a update/evicts a cache all instances will be impacted.  If the data being stale is ok however I would instead use local caching as it would be less complex and much faster as a http request would not be needed.
- Integrate Observability Tooling - A good observability tool can make life so much easier.  Datadog has been a huge help in debugging distributed systems at my current work place more times than I can recall or count.  It has also been a wonderful tool for collecting various metrics or answering questions about our system's architecture. Being able to set up automated alerts integrated wit PagerDuty also ensures we respond to issues ASAP.
- Setup CI Pipelines - Every time a commit is pushed we should automatically run tests on that branch to ensure a bug has not been introduced
- Use a real DB instead of sqlLite - As mentioned above, I would use PostgresSQL for a prod app with the given information we have.  Possible ways we can scale this are read replicas and using consistent hashing to shard data across multiple DB instances.
- Index DB columns - Depending on the searches we would expect to be common indexes can vastly speed up finding that data at the cost of maintaining an index.
- Security - Scan with pip-audit for vulnerable dependencies, this would be a good part of the CICD pipeline
- Containerization - Containerize the app to make deployment consistent
</details>

## Project Description

An API for users to create accounts and manage their collections of externally hosted photos.

## Setup

Start by installing Python if you do not have it installed already, this project was developed using version 3.13.1.
<details>
<summary style="font-size: 20px;">  If you are on windows... </summary>
run build_env.bat

.\.venv\Scripts\Activate.ps1 or .\.venv\Scripts\activate.bat
</details>


<details>
<summary style="font-size: 20px;">  If you are on Linux... </summary>
 <h3> Start by setting up your env </h3>
<ul>
    <li>Create a venv: python -m venv .venv</li>
    <li>activate venv: source venv/bin/activate</li>
    <li>upgrade pip: python -m pip install --upgrade pip</li>
    <li>Install requirements.txt: pip install -r requirements.txt</li>
</ul>
<p>Troubleshooting: May need to use python3 instead of python</p>
<p>ex: python3 -m venv .venv</p>
</details>

## Running

Navigate to the /photo_management_api folder

python manage.py runserver

<div style="">
<p style="display: inline; margin: 0;">Make sure you use </p>
<p style="display: inline; margin: 0; color:green; font-weight: 1000"> 127.0.0.1:8000 </p> 
<p style="display: inline; margin: 0;"> in your browser to view and </p>
<p style="display: inline; margin: 0; color:red; font-weight: 1000;"> not localhost:8000 </p> 
<p style="display: inline; margin: 0;">(Github SSO callback differentiates between the two!)</p>
</div>

Login: http://127.0.0.1:8000/admin/login/

Swagger: http://127.0.0.1:8000/schema/swagger-ui/

## Retrospective thoughts: My opinions on this assignment
### Overall Impression
As someone who has not only written code, but interviewed coding candidates, I wanted to add my thoughts on this assessment as well.
Overall I'm a big fan of practical assessments like this. I believe they do a better job of selecting for candidates that
can contribute to projects in comparison to leetcode assessments (Although I do personally like solving leetcode questions).

### Time 
Upon describing the criteria assignment to a friend of mine who is also a backend engineer 
he mentioned that this assignment was larger than he was willing to do. I think this assignment could add a bias
against engineers that have more out of work commitments than myself, such as he had with two young children.

There are two ideas I have that I think could help this assignment be more accessible to a wider range of candidates 
where a 6 hour commitment sounds too high.

The first is breaking down the assignment into smaller separate parts.  The first could be the raw API functionality.
The second authentication and authorization.  The third could be developing a test suite for this or another API.

The second idea (assuming this can be assigned any day of the week)  is extending the time frame to 5 business days to
give every candidate the weekend to have some time to work on it.

As for my own time commitment, it was probably close to 16 hours, however that is completely my fault as I choose Django instead of Spring Boot, 
a framework I am much more familiar with.  Since I'm already employed I figured I would use this as a learning opportunity to see how 
my skills would translate over to developing a python API.  Criticism and feedback on my choices, style, and errors is greatly appreciated.

### Cheating Vulnerability
I can see other candidates submissions when checking the main github.  This can lead to whoever submits last having the strongest submission
by adopting the taking ideas from other candidates submissions.
