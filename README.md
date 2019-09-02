# 💠 RESP - Responsive Emotional Support Protocols ![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)
The app is live at https://resp-angelhack.herokuapp.com. 

## API Endpoints
`/api/survivors`

`GET`: Returns a list of all survivors checked in

`POST`: (Private) Checks in a new survivor to the database


## What I learned
* Collaborated with a team of UI/UX designers, a frontend developer, and two backend developers
* Developed an API with Node + Express and MongoDb with integrated Typeform webhooks
* Implemented a frontend with React and React Router with an embedded Typeform 


## Description
In the aftermath of natural disasters, the mental and emotional health of survivors  is overlooked and undercovered.  A set of digital tools for first responders to provide effective, ethical mental health intervention in the immediate aftermath of a disaster and diagnostics for long-term prevention. 

RESP is meant to be an extension of a first responder's toolkit, adhering to the guidelines established by the World Health Organization's Psychological First Aid Kit. It is built with Django REST Framework and React with Machine Learning powered by IBM Watson and custom logistical regression classifiers trained on post-disaster psychiatric data. 

There are three modules for RESP - Survey, Status, and Services. Survey provides a series of questionaires intended for the first responder to fill out, inspired by the recommended questions asked for Psychological First Aid. This information is not only intended to establish a rapport with the disaster survivor, but populated an anonymous database to allow the custom ML models to consume. 

Once first responders fill out a survey for a survivor, they are added to the Catalog and considered 'checked-in'. The survivor may also state that they are seeking family members or friends, and if a match is found between their query and the Catalog, the survivor can be notified and reassured. The catalog keeps track of a census, geolocation, and the survivor's current risk of mental health symptoms based on their responses. 

The final module is Services, which uses offline geolocating to find nearby shelters and health facilities. RESP will synchronize with other users when internet connectivity is restored, and is intended to bounce off of Project OWL's mesh network to synchronize catalog data and update list of available services. 

## Team
Ava Biery - Backend, Machine Learning
Adam Rahman - Backend (Django Rest), geolocating, Machine Learning
Alex Guevara - Frontend (React), UI Design
Juliana Mercer Fogg - UI/UX Design, Frontend
Jessica Peng - UI/UX Design
