## hypertask

REST APIs for TODO list using Django Rest Framework

Try here: https://hypertask.fly.dev

#### Table of Contents
[Technologies Used](#technologies-used)<br>
[APIs](#apis)<br>
[Tests](#tests)<br>
[Tradeoffs for time](#tradeoffs-for-time)<br>
[Design Decision](#design-decision)<br>
[Deployment](#deployment)<br>
[Local Development](#local-development)<br>

### Technologies Used

- Python3
- Django Rest Framework
- Postgreql Database (Supabase for DB hosting)
- Fly.io for deployment

### APIs

Base URL : https://hypertask.fly.dev

|  Endpoint | Description | payload |
| :-------- | :----------- | :----------- |
| `POST /api/v1/users/register` | Register a new account. | {"name": "name", "email": "you@email.com", "password": "password"} |
| `POST /api/v1/users/login` | Authenticate and obtain a JWT token for accessing protected resources. | {"email": "you@email.com", "password": "password"}
| `POST /api/v1/users/login/token-refresh` | Get new access token from provided refresh toekn. | {"refresh" : "you refresh token"} |
| `POST /api/v1/users/logout` | logout the current logged in user |{"refresh" : "you refresh token"} |
| `POST /api/v1/users/change-pass` | Change current password of the authenticated user. | {"old_password": "your current password", "new_password":"new password", "new_password": "retype your new password"} |
| `GET /api/v1/users/me` | Get information of current logged in user. | |
| `POST /api/v1/tasks` | Create a new task for the authenticated user | {"title": "task title"} |
| `GET /api/v1/tasks` | Get all tasks for the authenticated user | |
| `POST /api/v1/tasks/bulk-update-status` | Update status of multiple tasks with to the provided status. | {"task_ids": ["taskid_1", "taskid_2"],"status": "COMPLETED"} |
| `DELETE /api/v1/tasks/bulk-delete` | Delete multiple tasks belong to authenticated user. | {"task_ids": ["taskid_1", "taskid_2"]} |
| `GET /api/v1/tasks/:task_id` | Retrieve task details associated with the id and the authenticated user. | |
| `POST /api/v1/tasks/:task_id` | Update task details associated with the id and the authenticated user. |{"status": "PENDING","title": "updated title gaina","description": "best desc 1"} |
| `DELETE /api/v1/tasks/:task_id` | Delete task details associated with the id and the authenticated user. | |
| `POST /api/v1/tasks/:task_id/status` | Toggle a task's status. | {"status": "COMPLETE"}

### Tests

to run test, run

```sh
python3 manage.py test
```

### Tradeoffs for time

Note that I time boxed myself 1 day to complete this task. So it will be easy evaluate whole better way.

- **Imperfect Authentication**

    I wanted to have a simple JWT authentication system that protects my tasks APIs from unauthorized access. Even though I ended up creating couple of extra APIs such as */change-pass*, */logout*. 
    
    This authentication system is no way perfect, it's missing some logical mistakes like password strength check, email format check, verify email address and */change-pass* allows to have old password as new password. 

    I focused more on building all the necessary APIs for tasks operations.

- **Test coverage** 

    Time didn't allow to write end-to-end test coverage. I was able to write some unittests for */tasks* API. you can run them using `python3 manage.py test` . code for that lives in *tasks/tests.py* file.

    To test entire system for basic operations against every breaking changes, I wrote a test bash script that you can find in scrips dir. run `./scripts/test.sh`

### Design Decision

I wanted to make this application as close as a production level app, that's why I chose to have my own custom id ( primary key) taht is generated based Stipe's custom Id convention [link](https://gist.github.com/fnky/76f533366f75cf75802c8052b577e2a5)

26 uppercase letters (A-Z), 26 uppercase letters (A-Z), 10 digits (0-9) so there are a total of 62 choices for each character, that gives 62^10 = 839 quadrillion unique ids for users and 62^12 > 3 sextillion unique ids for tasks. so we will fine , not to think about collision for near future

### Deployment

Entire app is deployed on [fly.io](https://fly.io). I've created **Dockerfile** so the app can be deployed to anywhere and a **fly.toml** for deployment on fly.

The app is accessible at : https://hypertask.fly.dev (Base URL)

To deploy on fly, run

```sh
fly deploy
```

> make sure you set all the environment variable on fly platform using  ```fly secrets set ``` command

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
