- Command for initial django-project in docker-container:
    ```commandline
    docker-compose run --rm backend-app sh -c "django-admin startproject config ."
    ```
- Command for apply base django migrations:
    ```commandline
    docker-compose run --rm backend-app sh -c "python manage.py migrate"
    ```
- Move to shell in container for development:
  ```commandline
  docker compose exec backend-app sh
  ```