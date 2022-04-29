[![Python 3.10.4](https://img.shields.io/badge/python-3.10-blue.svg?style=flat&logo=python)](https://www.python.org/downloads/release/python-314/)
[![CI](https://github.com/bobokrut/e1900288-final-project/actions/workflows/ci.yml/badge.svg)](https://github.com/bobokrut/e1900288-final-project/actions)

# Simple Gallery
https://e1900288-final-project.herokuapp.com
### Egor Evlampiev (e1900288)

### Contents
1. [Analysis](#analysis)
   1. [Case description](#case-description)
      1. [Actors of solution](#actors-of-the-solution)
      2. [Roles of actors](#roles-of-actors)
      3. [Tasks the actors would like to do](#tasks-the-actors-would-like-to-do)
      4. [Data input](#data-input)
      5. [Output data type](#output-data-type)
      6. [What kind of algorithms there are](#what-kind-of-algorithms-there-are)
   2. [Functional requirements](#functional-requirements)
   3. [Project schedule](#project-schedule)
   4. [Project plan](#project-plan-document)
   5. [Use case diagram](#use-case-diagram-drawn-with-visual-paradigm)
   6. [Test plan](#test-plan)
2. [Design](#design)
   1. [Sequence diagrams](#sequence-diagrams-one-from-client-side-one-from-server-side)
   2. [Package diagram](#package-diagram-drawn-with-visual-paradigm)
   3. [Class diagram](#class-diagrams-only-for-server-because-client-is-the-browser)
   4. [User stories](#two-user-stories)
3. [Implementation](#implementation)
4. [Testing](#testing)
   1. [Server test cases](#server-test-cases-pytest)
5. [Documentation](#documentation)
6. [Deployment](#deployment)

## Analysis

### Case description

This is the simple web gallery project for myself to be able to view local photos on all devices

#### Actors of the solution:
Egor Evlampiev (e1900288)
#### Roles of actors
Egor Evlampiev:
* Backend developer
* Database Architect

#### Tasks the actors would like to do:
* develop the backend for the application
* design the database

#### Data input:
* HTTP requests
* Images

#### Output data type:
* HTTP Response
* Images 

#### What kind of algorithms there are?
* **SHA256** for password hash generation
    
### Functional requirements
* Passwords in the database must be encrypted
* Each user should have its own account
* Each user should be able to log in
* Each user should only see its own images
* Each user should be able to upload a photo
* Each user should be able to log out
* Each row in the Image table should have:
  * ID
  * Image name
  * Image width
  * Image height
  * ID of the uploader
  * image
  * image thumbnail
* Each row in the User table should have:
  * ID
  * username
  * encrypted password
  * email
  * images

### Project schedule
| Project stage   | Date          |
|-----------------|---------------|
| Analysis        | 19.05 - 19.05 |
 | Design          | 20.05 - 22.05 | 
 | Implementation  | 23.05 - 27.05 | 
 | Testing         | 28.05 - 29.05 | 
 | Documentation   | 30.05 - 30.05 | 
 | Deployment      | 30.05 - 30.05 | 

### Project plan document 
[Project plan can be seen here](Project%20Plan.md)
### Use case diagram drawn with Visual Paradigm
![Use case diagram](.github/images/Client_Use_Case_Diagram.jpg?raw=true "Use case")


### Test plan
* Test that user can't open pages without logged in
* Test that user can't create account with the username which already exists
* Test that user can upload a photo
* Test that user can view images
* Test that user can't log in with the wrong password

## Design

### Sequence diagrams (one from client side one from server side)
![Sequence Server](.github/images/View_Gallery_Server.jpg?raw=true "Sequence Server")
![Sequence Client](.github/images/View_Gallery_User.jpg?raw=true "Sequence Client")
### Package diagram drawn with Visual Paradigm
![Package](.github/images/Server_Package_Diagram.jpg?raw=true "Package")
### Class diagrams (only for server, because client is the browser)
![Class](.github/images/Server_Class_Diagram.jpg?raw=true "Class")

### Two user stories
[Both of the user stories can be found here](https://github.com/bobokrut/e1900288-final-project/projects/1)
* As a user I want to have my own account, be able to log in and register
* As a user I want to be able to upload photos to the website and see them on the main page

## Implementation

* Server: for the server implementation I chose Flaks framework for backend development
* Database: for database I chose Heroku PostgreSQL

## Testing

### Server test cases (pytest)
* Test that user can't open pages without logged in
* Test that user can't create account with the username which already exists
* Test that user can upload a photo
* Test that user can view images
* Test that user can't log in with the wrong password
* Test that user can't log in with unexisting username
* Test that user can open main page while logged in
* Tet that user can open image page while logged in

## Documentation
For documentation, I chose code comments since this is small project and only for myself 

## Deployment

This project is deployed to Heroku
