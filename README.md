## hypertask

REST APIs for TODO list using Django Rest Framework

#### Table of Contents
[Technologies Used](#technologies-used)<br>
[APIs](#apis)<br>
[Local Development](#local-development)<br>
[Deployment](#deployment)<br>
[Tests](#tests)<br>
[Traidoffs](#traidoffs)<br>


### Technologies Used

- Python3
- Django Rest Framework
- Postgreql Database
- Fly.io for deployment

### Deployment

Entire app is deployed on [fly.io](https://fly.io). I've created **Dockerfile** so the app can be deployed to anywhere and a **fly.toml** for deployment on fly.

The app is accessible at : https://hypertask.fly.dev (Base URL)

To deploy on fly, run

```sh
fly deploy
```

> make sure you set all the environment variable on fly platform using  ```fly secrets set ``` command


### APIs

|  Endpoint | Description |
| :-------- | :----------- |
| `POST /api/v1/users/register` | Register a new account. |
| `POST /api/v1/users/login` | Authenticate and obtain a JWT token for accessing protected resources. |
| `POST /api/v1/tasks` | Add a new task for the authenticated user |
| `GET /api/v1/tasks` | Get all tasks for the authenticated user |
| `POST /api/v1/tasks/bulk-update-status` | Retrieve all tasks associated with the authenticated user. |
| `GET /api/v1/tasks/:id` | Retrieve task details associated with the id and the authenticated user. |
| `POST /api/v1/tasks` | Toggle a task's completed status. |

### Local Development

To run and test the app on local machine, follow the instruction bellow -

1. Clone the repo

    ```sh
    git clone https://github.com/0verread/hypertasks
    cd hypertasks
    ```

2. Create a virtual env and activate it

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install all the dependencies from *requirements.txt*

    ```sh
    pip3 install -r requirements.txt
    ```

4. Configure Environment Variables
    - copy all the necessary env variable from *.env.example*
        ```sh
        cp .env.example .env.dev
        ```
    - replace the Database values with real ones. you can use [Supabase](https://supabase.com) to create a postgres database
    - replace the Django secrect value with a real one. you can create one using,
        ```py
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ```
5. Run all the migrations. If database config is correct, this will create necessary tables
    ```sh
    python3 manage.py migrate
    ```

6. finally, run the app

    ```sh
    python3 manage.py runserver
    ```

    Visit http://localhost:8000 to test apis


### TODO:

- [] Test /change-pass, login/refresh apis

- [] document users/views.py, users/auth/api.py