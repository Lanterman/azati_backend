# Azati - test
Added a quick sort algorithm to sort current candidates and vacancies.

The project is 99% covered by tests.

### Launch of the project

#### 1) Clone repositories
```
git clone https://github.com/Lanterman/azati_backend.git
```
#### 2) Go to the 'azati_backend' directory
```
cd azati_backend
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
    or
   ```
    http://0.0.0.0:8000/swagger/
    ```
 - ##### to launch the drf openapi:
    ```
    http://127.0.0.1:8000/api/v1/
    ```
    or
   ```
    http://0.0.0.0:8000/api/v1/
    ```
   
P.S.
Before resetting "auth/reset_password/{email}/{secret_key}/" password, you must request it from "/auth/profile/try_to_reset_password/" endpoint.

P.S.S.
Test data is also loaded into the project. 
If you don't want to add them, remove line 24 in 'docker-compose.yaml' ('python manage.py loaddata ./config/test/test_data.json &&').
