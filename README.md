# Repositorium
# Table of Contents
- [Repositorium](#repositorium)
- [Table of Contents](#table-of-contents)
    - [API](#api)
      - [Users](#users)
    - [Getting Started](#getting-started)

### API
Repositorium have a lot of API's, you can see the [gettings started section](#getting_started) to start using it. All the resources availables are listed below:

1. [users](#users)
2. [systems](#systems)
3. [categories](#category)
4. [learning_objects](#learning_objects)
5. [recomendations](#recomender)

#### Users
The API for users are the ones who are responsible of creating and modifing a user. Additionaly, here is where you have the authentication mechanism.

**Public**:

- **`POST /api/v100/user/create/`**: Creates a user.

  The payload is:

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


**Auth Required**:

- **`GET /api/v100/user/current/`**: Get the info of the current user to be displayed.

    The response is:

    ```js
    Status: 200 OK
    {
        "email": "some_example@email.com",
        "first_name": "Cosme",
        "last_name": "Fulanito",
        "created_at": "1997-05-05T00:00:00Z", //YYYY-MM-DD format
    }
    ```

- **`PUT /api/v100/user/change_password/`**: Changes the password of the user which is logged in.

    The payload should look like:

    ```js
    {
        "current_password": "some_password",
        "new_password": "some_new_password",
        "confirm_new_password": "some_new_password",
    }
    ```

    The response is:

    ```js
    Status: 200 OK
    ```

- **`PUT /api/v100/user/update`**: Updates the basic information about the current user.

    The payload should be only the attributes that will change, an example:

    ```js
    {
        "first_name": "Homer",
        "last_name": "Simpson",
    }
    ```

    This are the only two attributes that you could change (for now).

    The response will be:
    ```js
    Status: 200 OK
    {
        "email": "some_example@email.com",
        "first_name": "Homer",
        "last_name": "Simpson",
        "created_at": "1997-05-05T00:00:00Z", //YYYY-MM-DD format
    }
    ```
    With the fields updated.

#####

### Getting Started
