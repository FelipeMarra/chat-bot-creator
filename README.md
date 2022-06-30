# Chatbot Creator Backend
> This is a backend project in python with  <a href="https://fastapi.tiangolo.com/">FastAPI<a> and <a href="https://www.sqlalchemy.org/">SQLAlchemy<a>. It was deployed in <a href="https://www.heroku.com/postgres">Heroku with the PostgreSQL add-on<a>. The objective was to create an API to a chatbot based on a state machine model, where the `creator user` can create chatbots and share it with `final users`. The chatbot is created using different types of states and transitions between them. There's even an `Open Text State` with some AI algorithms applied to it.

# Database Model
The database schema fully is presented in the images below and explained in detail along the next sections.

## Entity–relationship Model
<img src="https://github.com/FelipeMarra/chat-bot-creator-back/blob/f2024737e8a070442f53210144cade9b0c893fde/doc/Diagrama%20ER.png"/>

## Relational Model
<img src="https://github.com/FelipeMarra/chat-bot-creator-back/blob/f2024737e8a070442f53210144cade9b0c893fde/doc/Modelo%20Relacional.png"/>
