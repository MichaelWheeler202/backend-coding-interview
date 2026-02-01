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
    <li>I'm going to use Github SSO for this approach.  In general I'm a fan of SSO as it reduces our need to handle sensitive information like passwords.  If I was to allow account creation with usernames and passwords I'd want to make sure we only stored a salted hash and had two step verification for emails to ensure the user owns them.</li>
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
A good DB choice is: PostgreSQL  -- TODO although PostgreSQL is chosen to get a demo up and running I'll start with SQLite
<ul>
<li>TODO</li>
</ul>

Documentation: Similar to my experience with java it looks like open api is an option here.  I will go with that as it's what
I am familiar with and does an effective job at documentation.

Additional Tools: 
<ul>
<li>Unit Testing: TODO</li>
<li>Integration Testing: TODO</li>
<li>Security Analysis: TODO</li>
</ul>
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

## Retrospective thoughts: My opinions on this assignment

TODO


