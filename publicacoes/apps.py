from django.apps import AppConfig


class PublicacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publicacoes'
    verbose_name = 'Publicações PDF'
    
    def ready(self):
        """Configurações executadas quando a aplicação está pronta"""
        # Importar signals se houver
        # import publicacoes.signals
        pass

