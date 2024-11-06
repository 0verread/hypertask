## hypertask

REST APIs for TODO list using Django Rest Framework

#### Table of Contents
[Technologies Used](#technologies-used)<br>
[APIs](#apis)<br>


### Technologies Used

- Python3
- Django Rest Framework
- Postgreql Database
- Fly.io for deployment

### APIs

|  Endpoint | Description |
| :-------- | :----------- |
| `POST /api/v1/users/login` | Authenticate and obtain a JWT token for accessing protected resources. |
| `POST /api/v1/users/register` | Register a new account. |
| `POST /api/v1/tasks` | Add a new task. |
| `GET /api/v1/tasks/all` | Retrieve all tasks associated with the authenticated user. |
| `GET /api/v1/tasks/:id` | Retrieve task details associated with the id and the authenticated user. |
| `POST /api/v1/tasks` | Toggle a task's completed status. |

### TODO:

- [] Test /change-pass, login/refresh apis

- [] document users/views.py, users/auth/api.py

- [] requirement.text