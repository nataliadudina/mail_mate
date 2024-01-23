from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    #
    # def ready(self):
    #     super().ready()
    #     from .run_scheduler import start_scheduler
    #     print('ready')
    #     start_scheduler()
