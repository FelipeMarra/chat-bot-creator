# Chatbot Creator Backend
> This is a backend project in python with  <a href="https://fastapi.tiangolo.com/">FastAPI<a> and <a href="https://www.sqlalchemy.org/">SQLAlchemy<a>. It was deployed in <a href="https://www.heroku.com/postgres">Heroku with the PostgreSQL add-on<a>. The objective was to create an API to a chatbot based on a state machine model, where the `creator user` can create chatbots and share it with `final users`. The chatbot is created using different types of states and transitions between them. There's even an `Open Text State` with some AI algorithms applied to it.

  FastAPI already generates a documentation of the API routes based on the Pydantic models defined inside the project. For that reason the doc below will focous on explaining the system in general, mainly in the data structure, so one can make correct use of the routes.

# Database Model
  The database schema fully is presented in the images below and explained in detail along the next sections.

## Entity–relationship Model
<img src="https://github.com/FelipeMarra/chat-bot-creator-back/blob/f2024737e8a070442f53210144cade9b0c893fde/doc/Diagrama%20ER.png"/>

## Relational Model
<img src="https://github.com/FelipeMarra/chat-bot-creator-back/blob/f2024737e8a070442f53210144cade9b0c893fde/doc/Modelo%20Relacional.png"/>

# Data Models Part I: Creator User Flow
## Creator User Model
  First things first, our project needs a user. The `USER_CREATOR` model has an `ID`, a `name`, an `email` and `password`. The primary key is autoincremented for all models, for the user it could be the email, but it it would be bad for certain use cases like link generation - as we'll see later, the user's ID is used when generating a link to share the Chatbot.

  The model is named as `Creator` User, because this is the user that creates the Chatbots. The user that uses it it`s called Final User.

### Login
  The login route asks for a `OAuth2PasswordRequestForm` and returns user's info such as `name`, `email`, `id`, and also token data like `access_token`, `token_type`, and `expires_in`. When accessing the route `/creator_user/current` it will make use of the `oauth2_scheme` to identify the current user. This mean that if you use a midlewear, in the lib you use to make you requests, to inject the `oauth2_scheme` into the request, a empty call to this rout already retruns the user back to you.

  In `Flutter` you might wanna use the packege `oauth_dio` to hadle those configurations if you're using `dio` to consume the API. 

## Chatbot Model
  This is the class that's gona base the role system. The `CHAT_BOT` model has an `ID`, a `name`, a list of `states` a `initial_state`, a `share_link`, and the id of the `cretor` user.

  The chat `name` is unique for a user. In the db table names that are equal are allowed, because different users can create a chatbot with the same name, so the column is not setted as unique, but tryning to create two with the same name for the same user returns an `HTTP_406_NOT_ACCEPTABLE` exception.

  The list of `states` is a relation with the table responsable for the base state, and `initial_state` is the first state the state machine will run. 

  The `share_link` is generated automaticaly fllowing the pattern: CHATBOT_BASE_URL/creator_user.id/chatbot_name, where CHATBOT_BASE_URL is the path to the API endpoint.

## Base State Model
  As the name says this is the state that will be the base for every other one. Here we are basically emullating OOP's concept of inheritance, as this state works as the father of the others. That's the reason for the existence of the `type` propertie, wich indicates the type of state it will be

  Every state must create a state base setting it's type, and then add data to the tables tha contains the specific info about that type accordingly. Every table that specifies those specific infos will have an `state_base_id` reference.
  
  As one can see in the Relational Model, the MESSAGES and TRANSITIONS tables also have a reference to `state_base_id`. The state itself don't point to its messages and transitions, but everytime when recovering the state's data, those tables are consulted to return the proper result.
  
  The MESSAGES are table that store lists of messages that will be shown to the user. The type propertie indicate either it is plain text, or base64 images, or what ever type of data you can store as a string. The TRANSITIONS table in turn will store lists of transitions of this states, i.e., the states wich this one can go to.

  Ps: When I say lists I mean that when you look for the `state_base_id` reference the result will be a list of tuples - or rows - of that table.
  
## Single Choice State Model

