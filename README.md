# sigfrid

Sitio web Django (galería de obra, productos, exhibiciones, miscelánea y perfiles de
artista), contenerizado con **Podman Compose** y **PostgreSQL**.

## Stack

- Django 5.2 (Python 3.12) · PostgreSQL 16
- CKEditor (texto enriquecido) · Pillow (imágenes)
- WhiteNoise + gunicorn para producción · nginx como reverse proxy

## Desarrollo

```bash
podman compose up -d        # app en http://localhost:8091
podman logs -f sigfrid-web
```

Comandos de Django dentro del contenedor:

```bash
podman exec -it sigfrid-web python manage.py migrate
podman exec -it sigfrid-web python manage.py createsuperuser
```

## Producción

Ver **[DEPLOY.md](DEPLOY.md)** para la guía completa de despliegue (gunicorn + nginx,
variables de entorno, HTTPS y backups).

## Estructura

- `blog_website/` — proyecto Django (settings, urls, wsgi).
- Apps: `core`, `gallery`, `products`, `miscellany`, `herophotos`, `user_profile`.
- `templates/` — HTML · `assets/` — fuentes estáticas · `media/` — subidas de usuarios.
</content>
