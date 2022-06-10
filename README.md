# Repositorium
# Table of Contents
- [Repositorium](#repositorium)
- [Table of Contents](#table-of-contents)
    - [API](#api)
      - [**Users**](#users)
      - [**Authentication**](#authentication)
      - [**Systems**](#systems)
      - [**Categories**](#categories)
      - [**Learning Objects**](#learning-objects)
      - [**Recomendation System**](#recomendation-system)
    - [**Getting Started**](#getting-started)

### API
Repositorium have a lot of API's, you can see the [gettings started section](#getting_started) to start using it. All the resources availables are listed below:

1. [users](#users)
2. [systems](#systems)
3. [categories](#category)
4. [learning_objects](#learning_objects)
5. [recomendations](#recomender)

#### **Users**
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

#### **Authentication**

The authentication endpoints are responsible to log in an anonymous request to receive a bearer token to be provided on the authentications of each request, and to invalidate a token of an authenticated request.

Once you get an authentication token, you must provided on the headers as shown:

```js
    Headers: {
        //....
        "Authorization": "Token <token_value>",
        //....
    }
```

**NOTE:** Assume that each endpoint described on *Auth Required* sections must provide this header in order to function. If not, you will receive a `HTTP 401 Unauthorized` response.

**Public**:

- **`POST /api/v100/auth/login/`**: Creates a bearer token to use in the requests.

    The payload should be:

    ```js
        {
            "email": "cosme@fulanito.com",
            "password": "iamnothomer",
        }
    ```

    The response of this will be:

    ```js
    Status: 200 OK
    {
        "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    }
    ```

    If there are any errors, all responses will be `HTTP 400 Bad Request` in order to avoid enumeration.

**Auth Required**:
- **`POST /api/v100/auth/logout/`**: In order to invalidate the token provided, you just POST to this endpoint. No payload and the response should always be 200 OK.

#### **Systems**
The system api is responsible to keep track of all the systems that the repositorium recognizes. This is important to upload new content from the users and start collaborating with each other.

**Important!!**

All of the important operations need the `uuid` of the system. You could retrieve all the systems afterwards (which I don't recomend) in order to retrieve it, but it's best to keep it as an environment variable in the project you want to connect to repositorium. This will be provided when you create your system, so I strongly recommend to keep it when this is performed.

**Auth Required**:

- **`POST /api/v100/system/`**: This endpoint create a system in our database.

    The payload should be:
    ```js
    {
        "name": "Easy-Study",
    }
    ```

    The response if it was successfull:
    ```js
    Status: 201 CREATED
    {
        "uuid": "1214a0fb-0d73-4a0b-93be-5690e8acbb0e",
        "created_at": "1997-05-05T00:00:00Z",
        "name": "Easy-Study"
    }
    ```

- **`GET /api/v100/system/`**: Get the systems you have created on repositorium. This has some paginations included, and you can include `per_page` and `page_number` with the get request in order to change how many created entities you want per page and what page number you want.

    The expected response should be:
    ```js
    Status: 200 OK
    {
        "systems": [{"uuid": "1214a0fb-0d73-4a0b-93be-5690e8acbb0e","created_at": "1997-05-05T00:00:00Z","name": "Easy-Study"},]
        "page_number": 1,
        "has_next_page": false,
    }
    ```

- **`GET /api/v100/system/<system_uuid>`**: Get the information of a specific system, the response is exactly the same as the creation one but it returns a `200 OK` instead of a `201 CREATED` status.

    The expected response looks like:
    ```js
    Status: 200 OK
    {
        "uuid": "1214a0fb-0d73-4a0b-93be-5690e8acbb0e",
        "created_at": "1997-05-05T00:00:00Z",
        "name": "Easy-Study"
    }
    ```

#### **Categories**

Categories, also known as *tags* , is a short one liner description of a *learning object* that enhance the definition and description of it.

**Auth Required**

All the endpoints of this resource will need authorization tokens to access them.

- **`POST /api/v100/category/`**: Creates a category on the database.

    The expected body will be:
    ```js
        {
            "name": "Category Awesome Name",
        }
    ```
    The expected result is:
    ```js
        Status: 201 CREATED
        {
            "uuid": "5cd36a1c-6ebc-451e-8c01-86e25d891131",
            "created_at": "1997-05-05T00:00:00Z"
            "name": "Category Awesome Name",
        }
    ```
- **`GET /api/v100/category/`**: Get a list of all the categories with pagination. It can have `page_number` and `per_page` attributes through the URL.

    A response example should be:
    ```js
        {
            "categories": [{"uuid": "5cd36a1c-6ebc-451e-8c01-86e25d891131","created_at": "1997-05-05T00:00:00Z","name": "Category Awesome Name"},]
            "page_number": 1,
            "has_next_page": false,
        }
    ```

- **`GET /api/v100/category/<category_uuid>`**: Retrieve the data of a specific category.

    A response example should be:
    ```js
        Status: 200 OK
        {
            "uuid": "5cd36a1c-6ebc-451e-8c01-86e25d891131",
            "created_at": "1997-05-05T00:00:00Z"
            "name": "Category Awesome Name",
        }
    ```

#### **Learning Objects**

A learning object is a atomic piece of collaboration that a user submit into the system. With these data, you should give your users the power of collaboration between them. The recommendation systems are completely tied
with this data.

This API is divided in two, one for the learning objects as an entity and another for the file management of a given learning object (if applicable).


#### **Recomendation System**

(TODO: Create the API documentation for this)

### **Getting Started**
