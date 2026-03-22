# Overview
Project: Fihrist\
Purpose: Minimal CMS demonstrating CRUD backend architecture, built with
backend-first in mind\
Stack:
- Backend: Flask
- Database: PostgreSQL - Flask SQLAlchemy ORM
- Templates: server-side render
- Frontend helpers: HTMX + Bootstrap


# Request Flow
```
HTTP Request
a browser or another client sends an HTTP request to the application
   |
Flask
the flask framework receives the request and routes it to the
dedicated view function
   |
View Function
handles the incoming request, might have conditional for handling
submitted forms or GET/POST requests, handles exceptions thrown
   |
Service Layer
the application logic, all operations that require the collaboration
of multiple models or logic heavy or operations that require
external dependencies goes here
   |
Database ORM
responsible for querying database, database models should be thin, 
and should only contain operations that are tightly related to the model
   |
Database
```
