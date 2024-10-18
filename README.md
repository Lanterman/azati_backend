# Azati - test

The project is 98% covered by tests.

### Launch of the project

#### 1) Clone repositories
```
git clone https://github.com/Lanterman/azati_backend.git
```
#### 2) Go to the 'indors_backend' directory
```
cd indors_backend
```
#### 2) Create and run docker-compose
```
docker-compose up -d --build
```
##### 2.1) To create a superuser, run the following instruction:
```
docker exec -it <backend_container_ID> python manage.py createsuperuser
```

#### 3) Follow the link in the browser:
 - ##### to launch the swagger openapi:
    ```
    http://127.0.0.1:8000/swagger/
    ```
 - ##### to launch the drf openapi:
    ```
    http://127.0.0.1:8000/api/v1/
    ```
   
P.S.
Before resetting "auth/reset_password/{email}/{secret_key}/" password, you must request it from "/auth/profile/try_to_reset_password/" endpoint.
