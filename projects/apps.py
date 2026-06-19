from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'          # ← Esto es obligatorio
    verbose_name = 'Proyectos'