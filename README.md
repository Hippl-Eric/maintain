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

Logging services performed is the main feature of the application.  Each service is associated with a date and mileage, as well as, parts and a reminder.  The reminder is used to notify the user to perform the service again after the designated time or mileage interval.

Additional features include tracking total miles driven over all vehicles.  This will prove helpful when shopping for vehicle insurance.  Users can also log mileage with fuel amounts.  When completed at each fuel stop, an accurate picture of a vehicle's fuel efficiency is developed.  Changes in fuel efficiency can be the first sign of a potential mechanical problem in vehicles.

### File Summary

#### Python

The application includes 2 *main* python files:
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

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#000000&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2020-12-16T14:47:04.082Z\&quot; agent=\&quot;5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36\&quot; etag=\&quot;_mMRzLgQZoIJtmIVCRIr\&quot; version=\&quot;14.0.4\&quot; type=\&quot;device\&quot;&gt;&lt;diagram id=\&quot;R2lEEEUBdFMjLlhIrx00\&quot; name=\&quot;Page-1\&quot;&gt;7Vxtc+I2EP41fEzGrxA+BgK96cA0k6S9u08dBQtbjbCoLBLor6+EJPyGAsHAmcQ3zI21llfS7iM9q5UmLbc/W/5GwTwakwDilmMFy5Z713Kc7o3N/xeClRT4TlsKQooCKbJTwSP6DyqhpaQLFMAkV5ERghma54UTEsdwwnIyQCl5y1ebEpxvdQ5CWBI8TgAuS7+jgEVK6lhW+uIbRGGkm27rN89g8hJSsohVgzGJoXwzA1qPqppEICBvuQbhkg1JzFTv7yGdgRjGjL8ZA/oCacsfRIwJI9y2nCH/TUXt65CQEEMwR8n1hMy4eJLwKsMpmCEsPJBR1FOKeHPuoOX2KSFMPs2WfYiFF7WHZDeHhrcbE1Ghd48PpuAfm0RP328tEIbe793Bvw83V77U8grwQpm+D6gyD1tpd3BLzcUjA89C1EsYoEyhxrW4gOOAARTzcbl39rqMMZgnaF1dSiKEgxFYkQXTinSpN0VLGDxI0Ii6HD8jrkwUhXJh40fVGfEaYBTG/HnCBy5a7FGY8L6MQMJUDTUoSBlcGq1lb3zAZxEkM8joildRH7gaUCs9M1T5LcVjV4miDBJdJQMKQ+FG86axBz5jQMwBk7ZmO4XWnHJr7T1aA5hbJAYM9sQMSLJ44A+ZcaaiNUo+gJh2CTFGuHBrMwRwOt4iMIR3A0rmT4CGkCnBnCDh18ErlBNxDQGEcZ9gIvC1ntGq2nrYfo//uCH61rXf8nkH+rxsp2X+E9Up65M4YZTjVDQFOVzeoIBMj5G5agfDqe4GVVYWz8+EMT6vZWEvcJknWxlxq7wvMy53/A8iLOfsj3q2U8mzhFtkitfraYSCAMZyWRD0AFJvb3HkVuvnLJ51xeHWb2+3fsbc7jmtfXMJ1tZLrazbS+ZgguJwJL9sn8Idy5ZxMjgnck//6nU1erFY/O3N/YuNx+F95/nKcUv++TOBn4UaSzy4xYcfoMaGGQWi7RJiGmYsw+2d2VZfanQuYbE+fC02zPdfRY3lpbeG1j4hNe5afs9Hjdu75+32Dwz4fl4V+foSkZDEAA9SqaQuyZM2H20vYjOsOArGwa1IIvDi4IH75omMQbySL4ZIdHbtAbhE7Id45ouZLP3UCvjz3TJT7W6lCzG3QOYjUfyZfZd+ti7p7+QAxaiMrlSihCzoRO+l34ssmF7aTXY2bBcyft9sSrN+3wgpxICh13yP32Hfe8EbZpovAUqOVH2VTTwUFG2Wak3hnp9XJC1RUnQ0Xi6H2mOEIQjh3yMSfpKI7rjJjm4T0knodJuY7mAWu6l5TGddQphRwf7dekV1TrX90ScI6wwOqUtcp/3RxHW7YzMdU+wIAGsZ1+nwS9Ovf6S4zvHPG9dtSdENF+IctAno7JuCazpNQCcxs8fetQno3ptvNQ7oyofZNQwwKtjfq1lAV+0o+PIDOpNDahPQlU90HyF9RRPYcKTjeE4+Dmo4UsOm2tH01+bITs05slpCq/4caUg6/bKjrItIMp2SIw0OqQtHuntkpY6X9JiBOPhj7SBTysOp61nWu2mQnfkS097hbEkP27q2Mv/sPPW7+bdWO69/34zIjla6BRCfOD/i7nGOfqJ83gbOnU8KZwPNnw3OnXw0efDZrFdQZBcVnRqj5XzMPadBI0d+of1JMU/rtpv9icRMtTzPl96fuIaURV32J+5F5JQq2H/34c959ycXcen/hPsTk0Nqsz8pJ2Me4AzFwae5i16JJH2rIcntuGluLh2+JtT85pJ3EUmlCvav2c0l76vfXDI5pC4k6Tm7HXTUJN5Ks2tJuv3y0ibZsTXz0TpeBsMU358xz5bnY7vg870TE4XLRZsrymdKTHhnTZ5l88KHZcEOSrkdEXj6rHln6sxErudCqNcuAMs5EKF+8fpbUdHBCOXF9M9CyOrpX/lwB/8D&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>

User:<br>
Django's Abstract User model is used to handel authenticating users.  Each User is allowed to own multiple Cars.

Car:<br>
Many-to-one relationship with User.  The app is built around the concept of a "default car" which makes the Car model the main access point for data.  Multiple properties and methods were built to easily access a car's logs and reminders (both upcoming and overdue), and return a car's current and starting mileages.

Mileage_Log:<br>
Many-to-one relationship with Car.  A Mileage_Log can be associated with either a Fuel amount, or a Service.  The Mileage_Log model is the only model tied directly to Car.  For example a Service cannot be assigned to a Car, rather a Service is assigned to a Mileage_Log which is associated with a Car.  This provides numerous advantages:
- Prevent unnecessarily storing time and mileage data for services, parts, and fuel amounts separately.  All data is centralized.
- Fuels and Services can be looked up (and ordered) by date or mileage, grouped together or separately.

Fuel:<br>
One-to-one relationship with Mileage_Log.  A one-to-one was used instead of assigning an optional attribute to Mileage_Log.  This prevents returning empty columns for Mileage_Logs associated with Services only.

Service:<br>
Many-to-one relationship with Mileage_Log.  Requires only a service name but can optionally be tied to multiple parts and one reminder.

Part:<br>
Many-to-many relationship with Services.  This allows one part to be assigned to multiple Services (tied to multiple Cars and Users) to be stored only once.  Django handles this [relationship](https://docs.djangoproject.com/en/3.1/ref/models/fields/#id1) by creating an "an intermediary join table".

Reminder:<br>
One-to-one relationship to Service.  Like Fuel to Mileage_Log, every Service may not have a Reminder.  This prevents unnecessary empty columns when querying.

**views.py**<br>
Django's main application routing.  

Authentication:<br>
Login, register, and logout views follow the authentication methods provided in the Django [documentation](https://docs.djangoproject.com/en/3.1/topics/auth/default/#using-the-django-authentication-system).

POST Requests:<br>
The index, car_mileage_view, and car_service_view allow post requests from form submissions to add a new car, log a fuel/mileage stop, and submit a new service respectively.  Post request data is parsed and submitted to the database.  Django's get_or_create() method was used to add parts to a service without creating duplicates.

PUT Requests:<br>
The mileage_logs and service_data functions receive PUT requests from the site JavaScript.  The mileage_logs request specifies whether all cars' or just the default car's data should be returned.  Mileage data is returned in JSON for plotting.  The service_data request is used to pre-fill the service form based upon a reminder.  A serializer method was created on the Reminder model to return reminder data in JSON.

Export CSV Data:<br>
The user has the option to export their service logs to csv.  The csv_data view parses the user's service logs in reverse chronological order, and writes a csv file using Python's csv module.  Django's FileResponse returns an attachment, and the user's browser prompts the user to save the file.

Helper Functions:<br>
In addition to the main views, helper functions were created.  As stated, the site is built around the concept of a "default car".  To make manipulating the default car easier, functions to set, update, and get the default car were created.  

#### Javascript

The application includes 2 JavaScript files:
1. maintain.js
2. siteplots.js

**maintain.js**<br>
The site's main JavaScript source, written mostly in vanilla JavaScript (some jQuery).  Fetch, then methods are used to make calls to the backend.  The site design relies on setting a default car which is referenced on each HTML page.  The setDefaultCar function grabs the vehicle clicked by the user and sends it to the backend to be set in the Django session and database.

Additional features include: adding parts to the service form, pre-filling the service form when clicking on a reminder, and resetting the form when the Bootstrap model is closed (hidden).

**siteplots.js**<br>
Charts for plotting mileage data is an essential feature of the site, allowing users to visualize their data.  The [Charts.js](https://www.chartjs.org/) library was used to accomplish this.  A single chart plotting function was used for the site's two (2) different charts.  Using HTML data attributes, canvases are set with parameters to determine the type of chart to plot.  This data is parsed and used to query the backend for appropriate plot data.

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
Utilizing Django's "include" template tag, the service_block displays information for each service.  Breaking this block of html into a separate file makes this code more readable and DRY.

**reminder-block.html**<br>
Similar to the service-block, the reminder block  displays reminder information.  This block is used in 2 locations, and a template variable modifies the styling for overdue vs upcoming.

#### CSS

The application includes 1 css file:
1. styles.css

**styles.css**<br>
The sites styling is basic and mainly uses Bootstrap components.  The "car buttons" displayed on the index page are styled based on the car-button class.  The site has been checked to be mobile-responsive and functional for screen widths down to 320 pixels.

### What I Learned
- Designing Django models to satisfy application architecture - A lot of time was spent before any code, writing down and visualizing the final application.  Coming up with a list of requirements, led to the model structure used for the app.

- More advanced filtering in Django - The get_reminders_upcoming property of the Car model in models.py utilizes reverse relationships, chaining, and "or" logic requiring the Django Q object.

- Reinforced knowledge of data structures - Parsing database query sets into JSON and csv format.

- Better understanding of the POST data object returned from HTML forms - The log service form allows the user to add parts to the form.  The backend needed to be able to handel a variable number of parts for a service.  Iterating through the POST dictionary-like object was required.

- Using the datetime module in python and sending to a date object in JavaScript.

### Contact

Eric Hippler, [LinkedIn](https://www.linkedin.com/in/eric-hippler/)
