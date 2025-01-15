# apps/users/apps.py

from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Users and Phones'

    def ready(self):
        """
        This method is called when the application is fully loaded.
        - You can import signals here if you need them later.
        - For now, we'll leave it empty since we don't want signals or extra logic.
        """
        pass
