from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    # 1. 👇 Add this line for signals
    #def ready(self):
    #    import website.signals

