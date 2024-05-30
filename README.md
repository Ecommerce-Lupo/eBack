# eBack

## Commands

- Makemigrations: Crea las migraciones
```
docker compose run --rm app sh -c 'python manage.py makemigrations'
```
- Migrate: Hace el amago de hacer las migraciones
```
docker compose run --rm app sh -c 'python manage.py migrate'
```