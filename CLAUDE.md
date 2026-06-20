# CLAUDE.md — podman-gallery

Sitio web Django (blog + galería + eventos + proyectos + perfiles) llamado internamente
**"sigfrid"**, orquestado con **Podman Compose**. El nombre de carpeta es `podman-gallery`,
pero todos los nombres internos (compose `name:`, contenedores, volúmenes, imagen) son `sigfrid`.

## ⚠️ Qué copia corre — confirmá siempre el montaje

En `C:\Users\julia\Desktop\proyectos` hay **dos copias** del mismo proyecto Django (mismo
remoto GitHub `juliana-rar/podman-gallery`): `sigfrid` y `podman-gallery` (esta). Cuál de las
dos monta el contenedor `sigfrid-web` en `/app` **ha cambiado en el tiempo**, así que no lo
asumas: confirmalo antes de tocar nada.

```powershell
podman inspect sigfrid-web --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{end}}'
```

- **2026-06-20**: el montaje es `.../podman-gallery -> /app` (vía WSL:
  `/mnt/c/Users/julia/Desktop/proyectos/podman-gallery`). Es decir, **esta copia ES la viva**;
  editar acá **sí** cambia el sitio en ejecución (dev, host port 8091).
- Históricamente la copia viva era `sigfrid`; `podman-gallery` era un clon no montado. Si el
  `inspect` vuelve a apuntar a `sigfrid`, esta copia deja de reflejarse en el sitio.

Tras cambios de modelo, aplicá migraciones en el contenedor (corren solas al levantar, pero
si editás en caliente hay que correrlas a mano): `podman exec sigfrid-web python manage.py migrate`.

El usuario a veces pide cambios **solo en una copia** a propósito (p. ej. el hero con video de
fondo, cuyos assets `staticfiles/dessign/` solo están en `podman-gallery`) — preguntá si hay duda.

## Stack

- **Django 5.2** (Python 3.12), **PostgreSQL 16**, **Django REST Framework**.
- **CKEditor** (editor de texto enriquecido), **crispy-forms** (bootstrap4), **Pillow** (imágenes).
- **whitenoise** + **gunicorn** para producción; `ollama` está en requirements (integración IA).
- Usuario custom: `AUTH_USER_MODEL = 'user_profile.User'`, login por email
  (`user_profile.backends.EmailAuthenticationBackend`).

## Estructura

- `blog_website/` — proyecto Django: `settings.py`, `urls.py`, `wsgi.py`/`asgi.py`.
- Apps: `blog`, `miscellany`, `gallery`, `herophotos`, `projects`, `user_profile`. Casi todas
  cuelgan de la raíz `''` en `blog_website/urls.py`.
- `projects/api.py` — `ProyectoViewSet` (DRF), montado en `/api/proyectos/`.
- `templates/` — HTML del sitio (no en las apps). `assets/` — fuentes estáticas
  (`STATICFILES_DIRS`). `staticfiles/` — destino de `collectstatic` (`STATIC_ROOT`).
- `media/` — subidas de usuarios (`MEDIA_ROOT`), persistido en volumen.
- `context_processors` activos: `blog`, `gallery`, `herophotos`, `user_profile` (categorías,
  fotos de hero, settings del sitio → disponibles en todas las plantillas).

## Configuración

`settings.py` lee todo de un `.env` (vía `django-environ`). Variables requeridas:
`SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`,
`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`. En compose, `DB_HOST` se fuerza a `db`.

## Comandos

**Desarrollo** (`compose.yaml`, port host **8091** → 8000, código montado, runserver):
```powershell
podman compose up -d
podman compose down
podman logs -f sigfrid-web
```
Las migraciones corren solas al levantar (`migrate --noinput && runserver`).

Comandos de Django dentro del contenedor:
```powershell
podman exec -it sigfrid-web python manage.py makemigrations
podman exec -it sigfrid-web python manage.py migrate
podman exec -it sigfrid-web python manage.py createsuperuser
```

**Producción** (`compose.prod.yaml`, requiere `.env.prod`, nginx en host **8090**, gunicorn):
```powershell
podman compose -f compose.prod.yaml --env-file .env.prod up -d --build
```
Diferencias: `DEBUG=False`, código horneado en la imagen (sin montar host), nginx sirve
estáticos/media y hace reverse proxy, `collectstatic` corre al arrancar.

## Notas / gotchas

- Dev (8091) y prod (8090) conviven sin pisarse: nombres de proyecto y volúmenes distintos
  (`sigfrid_*` vs `sigfrid_*_prod`).
- El PostgreSQL local del host ocupa 5432; el `db` de dev expone **5433**.
- En `compose.prod.yaml` la línea de `gunicorn` debe ir en **una sola línea**: si el YAML
  folded la parte, arranca sin flags en 127.0.0.1 y nginx devuelve 502.
- En el Bash tool sobre Windows, rutas `/app/...` se manglean a `C:/Program Files/Git/app/...`;
  usá **PowerShell** para `podman exec ... ls /app/...`.
