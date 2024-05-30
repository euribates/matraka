set export

# Ejecutar test (Omitiendo los lentos)
test *args='.': clean check
    python -m pytest -m "not slow" -x --reuse-db --no-migrations --failed-first {{ args }}


# Ejecutar ctags
tags:
    cd {{justfile_directory()}} && ctags -R  --exclude=media/*  --exclude=*/static/* --exclude=static/* .


# Ejecutar django check
check:
    python ./manage.py check


# Cambiar el título de la terminal
[unix]
termtitle *args='Terminal':
    echo -en "\033]0;{{ args }}\007";


# Ejecutar django collectstatic
static:
    python ./manage.py collectstatic --no-input


# Borrar ficheros compilados de python
clean:
    sudo find . -type d -name "__pycache__" -exec rm -rf "{}" +
    sudo find . -type d -name ".mypy_cache" -exec rm -rf "{}" +
    sudo find . -type f -name "*.pyc" -delete
    sudo find . -type f -name "*.pyo" -delete


# Mostrar migraciones Django
showmigrations $APP='': check
    python3 manage.py showmigrations {{APP}}

alias sm := showmigrations

# Crear nuevas migraciones Django
makemigrations $APP='': check
    python3 manage.py makemigrations {{APP}}

alias mm := makemigrations

# Ejecutar migraciones Django
migrate $APP='': check
    python3 manage.py migrate {{APP}}


# Ejecutar un run server en modo desarrollo
rundev: check static 
    python ./manage.py runserver_plus 0.0.0.0:8801 --nopin --insecure --print-sql


# Actualiza en caliente contenidos estaticos js/css/png/svg
[unix]
watch: static
    just termtitle Watch
    watchmedo shell-command  --patterns "*.css;*.js;*.png;*.jpg;*.webp;*.svg" --recursive --command "just static"

