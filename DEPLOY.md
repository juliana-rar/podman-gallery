# Despliegue en producción — sigfrid / podman-gallery

App Django servida con **gunicorn** detrás de **nginx**, con **PostgreSQL**, orquestada
por **Podman Compose**. Todo corre en contenedores; no se instala nada de Python en el host.

## 1. Requisitos en el servidor

- `podman` y `podman-compose` (o `podman compose`).
- Puertos: el stack expone solo **8090** (nginx). Mapealo a 80/443 con tu reverse
  proxy/firewall, o cambiá el puerto en `compose.prod.yaml`.

## 2. Configurar variables de entorno

```bash
cp .env.prod.example .env.prod
# editá .env.prod con valores reales
```

Generá una `SECRET_KEY` nueva:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Completá como mínimo: `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
`DB_NAME`, `DB_USER`, `DB_PASSWORD`. Dejá `DB_HOST=db`.

> `.env.prod` contiene secretos y está en `.gitignore`. Nunca lo subas al repo.

## 3. Levantar el stack

```bash
podman compose -f compose.prod.yaml --env-file .env.prod up -d --build
```

Al arrancar, el contenedor `web` ejecuta automáticamente:

1. `python manage.py migrate --noinput`
2. `python manage.py collectstatic --noinput`
3. `gunicorn blog_website.wsgi:application --bind 0.0.0.0:8000 --workers 3`

nginx sirve `/static/` y `/media/` desde volúmenes compartidos y hace de reverse proxy.

## 4. Primer arranque: superusuario

```bash
podman exec -it sigfrid-web-prod python manage.py createsuperuser
```

## 5. Operación

```bash
# Logs
podman logs -f sigfrid-web-prod
podman logs -f sigfrid-nginx-prod

# Migraciones tras desplegar cambios de modelos
podman exec -it sigfrid-web-prod python manage.py migrate

# Re-desplegar una versión nueva (rebuild de la imagen)
git pull
podman compose -f compose.prod.yaml --env-file .env.prod up -d --build

# Parar
podman compose -f compose.prod.yaml --env-file .env.prod down
```

## 6. HTTPS (recomendado)

El `compose.prod.yaml` sirve HTTP en 8090. Para TLS, poné delante un reverse proxy con
certificado (Caddy, Traefik o nginx + certbot en el host) que termine HTTPS y reenvíe a
`127.0.0.1:8090`. Una vez con HTTPS real, activá en `.env.prod`:

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

Django ya confía en `X-Forwarded-Proto` (`SECURE_PROXY_SSL_HEADER`), así que detecta
HTTPS correctamente detrás del proxy.

## 7. Backups de datos

- **Base de datos** (volumen `sigfrid_dbdata_prod`):
  ```bash
  podman exec -t sigfrid-db-prod pg_dump -U $DB_USER $DB_NAME > backup_$(date +%F).sql
  ```
- **Media subida por usuarios**: volumen `sigfrid_media_prod`.

## Notas

- Si nginx devuelve **502**, casi siempre es la línea de `gunicorn` en `compose.prod.yaml`
  partida en varias líneas (debe ir en una sola); revisá que arranque con sus flags.
- Producción (`sigfrid-*-prod`, puerto 8090) y desarrollo (`sigfrid-*`, puerto 8091)
  usan nombres y volúmenes distintos, así que conviven sin pisarse.
</content>
