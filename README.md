Document Links: [about](#about) / [install](#install) / [usage](#usage) / [demo](#demo)


# CSCI-4317-SEII-Project

<img width="1760" height="1211" alt="image" src="https://github.com/user-attachments/assets/696a4c0d-1b97-4491-950a-6885c7f18821" />




<a name="about"></a>
## Definition of the problem:
- Students are likely to miss assignments as they have to search through classroom pages & documents to find their assignments. All while relying on clunky built-in calendars (eg, Blackboard)
- Instead of doing that, we’re creating a single place where you can track due dates and other important milestone dates, make notes of priorities for assignments, and get notifications for approaching due dates.

## Who are the users?
- HighSchool Students - A place to transition away from manual planners and start managing multiple subjects and extracurriculars effectively
- Higher Education Students - These users require a tool that can track complex milestones and due dates that are often buried in a syllabus or external documents 


## Why it matters:
- This matters as many students try to rely on built-in learning platform trackers for assignments when some instructors keep due dates in documents that are untracked. This app is for people who have a lot on their plate and want a place that will keep track of these dates for them.


## Work Break-down:
- Front-End - Focusing mostly on visual elements where users can view assignment information and interact with the web app.

- Back-End - Communication with the front-end team will ensure that the app meets the requirements listed in the functional requirements document.

- Hybrid - This role will help bridge the gap and make sure notifications and events are handled accordingly.


## Functional Requirements
- Users are able to enter assignment info, including due dates, priority, and details on assignment (what class it’s for, if it’s a group project, etc.)

- User is able to view a dashboard with all assignment information readily viewable

- Users allowed to mark assignments as completed.

- User will get notifications for impending due dates

- User can edit assignment info and update due dates if needed

- Users can adjust timing for due date notifications (number of days out to notify, how many times to notify, when to notify, etc.)



## Non-Functional Requirements
- System will be reasonably responsive under different network traffic loads

- System will be intuitive to use with minimal instructions or guides

- User logins will be stored securely, passwords hashed

- The application should support more users and assignments as they are added



## Use Cases:
- “As a user, I want a place to track due dates for my classes, including due dates of projects, single assignments, or papers or due dates for milestones for group projects.”
 
- “As a user, I want to be notified a set amount of days before due dates for assignments.”

- “As a user, I want to use a secure, responsive platform with an interactive dashboard for ease of viewing.”

- “As a user,  I want to mark assignments as completed so I can track my progress.”

- “As a user,  I want to filter assignments by class to focus on one class at a time.”



<img width="3149" height="1373" alt="image" src="https://github.com/user-attachments/assets/09cfb075-674e-41e4-bf96-0df4120b04ef" />

<a name="install"></a>
# Installation:
- ``` apt install python3.13-venv ``` # install the virtual environment module for Python 3.13
- ``` apt install git ```             # install Git
- ```python3 -m venv venv```          # create virtual environment
- ```source venv/bin/activate```      # activate it
- ```git clone https://github.com/OrangeXR/CSCI-4317-SEII-Project/```
- ```cd CSCI-4317-SEII-Project```
- ```pip install -r requirements.txt```   # installs all packages listed



<a name="usage"></a>
# Usage:
Navigate to the application's root folder and run app.py
- ``` python3 src/app.py```
- <img width="327" height="32" alt="image" src="https://github.com/user-attachments/assets/5f7631e7-997d-4a52-a383-58dd4faab684" />
- A Flask instance will be started.  Click on the ip to launch a browser window for the GUI
- <img width="835" height="89" alt="image" src="https://github.com/user-attachments/assets/470fa7a0-e67e-45c2-b8d2-04260a7cf058" />
- Login or create an account
- <img width="144" height="193" alt="image" src="https://github.com/user-attachments/assets/5b918fe1-f2a8-4761-a25c-37e58c10d780" />
- Once logged in you will be taken to the dashboard showing assignments due this, next week, and list of your assignments.  The list is sorted by due date by default.
- <img width="893" height="382" alt="image" src="https://github.com/user-attachments/assets/abbac92a-b1fe-4758-be5b-08e6ebbf7c50" />
- Assignment Notes can be viewed by clicking on the Show Details button
- <img width="205" height="338" alt="image" src="https://github.com/user-attachments/assets/05c31adc-e2fe-40fb-a335-23f944486c29" />
- The main menu is along the left of the window.  From here there is an option to add an assignment
- <img width="77" height="149" alt="image" src="https://github.com/user-attachments/assets/ed58aea7-e4e6-4675-afed-d47f8530cd5e" />
- Fields are provided for the assignment information as well as an option to include notes and files related to each assignment
- <img width="431" height="387" alt="image" src="https://github.com/user-attachments/assets/97173d72-80a9-4c58-9013-0f6c6dad13d3" />
- The profile page allows users to change their profile picture as well as seeing their completed assignments
- <img width="756" height="386" alt="image" src="https://github.com/user-attachments/assets/6e24bab8-9a42-40b0-8e8d-2ccbd98412cd" />


<a name="demo"></a>
# Demo:

<center>
The Phasers:
<br>
<a href="https://github.com/OrangeXR" title="Luis M"><img width="50" height="50" alt="profile image" src="https://avatars.githubusercontent.com/u/77978673?s=64&v=4" /></a><a href="https://github.com/soldudo" title="Nico G"><img width="50" height="50" alt="A graphic-heavy logo" src="https://avatars.githubusercontent.com/u/88810277?s=64&v=4" /><a href="https://github.com/nere-var" title="Emma W"><img width="50" height="50" alt="profile image" src="https://avatars.githubusercontent.com/u/58350011?v=4" /></a><a href="https://github.com/A-perez2265" title="Augustine P"><img width="50" height="50" alt="A graphic-heavy logo" src="https://avatars.githubusercontent.com/u/192671553?v=4" /><a href="https://github.com/bfier98" title="Ben F"><img width="50" height="50" alt="profile image" src="https://avatars.githubusercontent.com/u/220130367?v=4" /></a></center>
