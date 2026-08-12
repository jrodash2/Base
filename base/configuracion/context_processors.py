from django.db.utils import OperationalError, ProgrammingError

from .models import ConfiguracionSistema


def configuracion_sistema(request):
    try:
        configuracion = ConfiguracionSistema.obtener()
    except (OperationalError, ProgrammingError):
        configuracion = None
    return {"configuracion_sistema": configuracion}
