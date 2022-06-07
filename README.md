# Repositorium
# Table of Contents
1. [API](#api)
2. [Getting Started](#getting_started)

### API
Repositorium have a lot of API's, you can see the [gettings started section](#getting_started) to start using it. All the resources availables are listed below:

1. [users](#users)
2. [systems](#systems)
3. [categories](#category)
4. [learning_objects](#learning_objects)
5. [recomendations](#recomender)

#### Users
The API for users are the ones who are responsible of creating and modifing a user. Additionaly, here is where you have the authentication mechanism.

##### `/api/v1/user`
**Public**:
    * `POST`: Creates a user. The payload is:

    ```js
    Headers: {}
    {
        "email": "some_example@email.com",
        "first_name": "Cosme",
        "last_name": "Fulanito",
        "password": "one_cup_please",
    }
    ```

    The response of this will be:

    ```js
    Status: 201 CREATED
    {
        "email": "some_example@email.com",
        "first_name": "Cosme",
        "last_name": "Fulanito",
        "created_at": "1997-05-05T00:00:00Z", //YYYY-MM-DD format
    }
    ```

**Auth Required**
    * `

#####

### Getting Started
