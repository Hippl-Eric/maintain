# Capstone Project
CS50's Web Programming with Python and JavaScript

## Application Name: Maintain
Maintain is a Django application built to log and track a user's vehicle maintenance.<br>

Key Features:
- Log vehicle services, parts, and fuel consumption
- Remind user of upcoming and overdue maintenance intervals
- Plot vehicle mileage
- Allow user to download service data to csv

### Table of Contents

- [Background](#background)
- [File Summary](#file-summary)
    - [Python](#python)
    - [JavaScript](#javascript)
    - [HTML](#HTML)
    - [CSS](#CSS)
- [What I Learned](#what-i-learned)
- [Contact](#contact)

### Background
As someone who enjoys working with my hands, I complete most of my own vehicle maintenance.  I am not, however, someone who enjoys tracking or remembering to complete this maintenance.  Maintain was built as a solution to each of these issues.

Logging services performed is the main feature of the application.  Each service is associated with a date and mileage, as well as, parts and an optional reminder.  The reminder is used to notify the user to check or perform the service again after the designated time or mileage interval.

Additional features include tracking total miles driven over all vehicles.  This will prove helpful when shopping for vehicle insurance.  Users can also log mileage with fuel amounts.  When completed at each fuel stop, an accurate picture of a vehicle's fuel efficiency is developed.  Changes in fuel efficiency can be the first sign of a potential mechanical problem in vehicles.

### File Summary

#### Python

The application includes 2 main python files (other than Django files):
1. models.py
2. views.py


**models.py**<br>
By far the most time was spent planning the application's models and relationships (as expected).  A graphical diagram is provided of the apps seven (7) models:
1. User
2. Car
3. Mileage_Log
4. Fuel
5. Service
6. Part
7. Reminder

TODO Diagram

User:<br>
Django's Abstract User model is used to handel authenticating users.  Each User is allowed to own multiple Cars.

Car:<br>
Many-to-one relationship with User.  The app is built around the concept of a "default car" which makes the Car model the main access point for data.  Multiple properties and methods were built to easily access a car's logs and reminders (both upcoming and overdue), and return a car's current and starting mileages.

Mileage_Log:<br>
Many-to-one relationship with Car.  A Mileage_Log can be associated with either a Fuel amount, or a Service.  The Mileage_Log model is the only model tied directly to Car.  For example a Service cannot be assigned to a Car, rather a service is assigned to a Mileage_Log which is associated with a vehicle.  This provides numerous advantages:
- Prevent unnecessarily storing time and mileage data for services, parts, and fuel amounts separately.  All data is centralized.
- Fuels and Services can be looked up (and ordered) by date or mileage, grouped together or separately.

Fuel:<br>
One-to-one relationship with Mileage_Log.  A one-to-one was used instead of assigning an optional attribute to Mileage_Log.  This prevents returning empty columns for Mileage_Logs associated with Services only.

Service:<br>
Many-to-one relationship with Mileage_Log
Optionally, can also be associated with Parts and a Reminder.

Part:<br>
Many-to-many relationship with Services.  This allows one part to be assigned to multiple Services (or even Cars/Users) to be stored only once.  Django handles this relationship by creating an "an intermediary join table". (https://docs.djangoproject.com/en/3.1/ref/models/fields/#id1)

Reminder:<br>
One-to-one relationship to service.  Like Fuel to Mileage_Log, every Service may not have a Reminder.  This prevents unnecessary empty columns when querying.

**views.py**<br>
Django's main application routing.  

Authentication:<br>
Login, register, and logout views follow the authentication methods provided in the Django documentation.  

POST Requests:<br>
The index, car_mileage_view, and car_service_view allow post requests from the user to add a new car, log a fuel/mileage stop, and submit a new service respectively.  Post request data is parsed and submitted to the database.  Django's get_or_create() method was used to add parts to a service without creating duplicates.

PUT Requests:<br>
The mileage_logs and service_data functions receive PUT requests from the site JavaScript.  The mileage_logs request specifies whether all cars' or just the default car's data should be returned.  Mileage data is returned in JSON for plotting.  The service_data request is used to pre-fill the service form based upon a reminder.  A serializer method was created on the Reminder model to return reminder data in JSON.

In addition to the main views, helper functions were created.  As stated, the site is built around the concept of a "default car".  To make manipulating the default car easier, functions to set, update, and get the default car were created.  

#### Javascript

The application includes 2 JavaScript files:
1. maintain.js
2. siteplots.js

**maintain.js**<br>
The site's main JavaScript source, written mostly in vanilla JavaScript (some jQuery).  Fetch, then methods are used to make calls to the backend.  The site design isThe default vehicle is then set in the Django session and database.  This preserves the data.  Additional features include: adding parts to the "Log Service" form, pre-filling the service form when clicking on a reminder, and resetting the form when the Bootstrap model is closed (hidden).

**siteplots.js**<br>
Charts for plotting mileage data is an essential feature of the site, allowing users to visualize their data.  The [Charts.js](#https://www.chartjs.org/) library was used to accomplish this.  A single chart plotting function was used for the site's two (2) different charts.  Using HTML data attributes, canvases are set with parameters to determine the type of chart to plot.  This data is parsed and used to query the backend for appropriate plot data.

#### HTML

The application includes 8 HTML files:
1. layout.html
2. register.html
3. login.html
4. index.html
5. car_mileage.html
6. car_service.html
7. service-block.html
8. reminder-block.html


**layout.html**<br>
Includes the page structure, all required meta tags, and site's navigation bar. A second navbar was used to inform the user of the current default car when viewing each page.  The layout is extended to all other HTML pages.

**register.html**<br>
Register.html posts information to the register view.  Register allows users to register for the site and relies on Django's User model for authentication.  The user is then routed to the index page.

**login.html**<br>
Like the register page, login.html posts information to the login view.  After logging in, user is routed to the index view.

**index.html**<br>
Displays all cars owned by the user and a chart which plots each cars mileage vs time.  Allows user to choose one of their cars or add a new car.  The new car form is displayed in a Bootstrap modal.  After clicking on a car, that car is set as the default car for the session.  If no default car is set, the navbar links are not available to access the mileage or service views.

**car_mileage.html**<br>
The main landing page after a default car is selected.  Displays an overview of the default car and a chart which plots the car's mileage.  User can log fuel/mileage logs by clicking the "Log Mileage" banner.  The form is displayed in a Bootstrap modal.

**car_service.html**<br>
Allows a user to post a new service performed.  The log service form is displayed in a Bootstrap modal.  All past services completed are displayed in reverse chronological order.  Also displayed are both overdue and upcoming service reminders.

**service-block.html**<br>
Utilizing Django's "include" template tag, the service_block displays information for each service.  Breaking this block of html into a separate file makes this code more readable and dry.

**reminder-block.html**<br>
Similar to the service-block, the reminder block displays displays reminder information.  This block is used in 2 locations, and a template variable modifies the styling for overdue vs upcoming.

#### CSS

The application includes 1 css file:
1. styles.css

**styles.css**<br>
The sites styling is basic and mainly uses Bootstrap components.  The "car buttons" displayed on the index page are styled based on the car-button class.  The site has been checked to be mobile-responsive and functional for screen widths down to 320 pixels.

### What I Learned
- Designing Django models to satisfy application architecture - A lot of time was spent before any code, writing down and visualizing the final application.  Coming up with a list of requirements, led to the model structure used for the app.

- More advanced filtering in Django - The get_reminders_upcoming property of the Car model in models.py utilizes reverse relationships, chaining, and "or" logic requiring the Django Q object.

- Reinforced knowledge of data structures - Parsing query sets into JSON format for plotting.

- Better understanding of the POST data object returned from HTML forms - The log service form allows the user to add parts to the form.  The backend needed to be able to handel a variable number of parts for a service.  Iterating through the POST dictionary-like object was required.

- Using the datetime module in python and sending to a date object in JavaScript.

### Contact

Eric Hippler, [LinkedIn](#https://www.linkedin.com/in/eric-hippler/)
