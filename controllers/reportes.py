from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.analitica_service import AnaliticaService

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/analitica')
@login_required
def analitica():
    # 1. El controlador solo revisa permisos (Su única responsabilidad web)
    if current_user.rol != 'admin':
        return "No autorizado", 403

    # 2. Pide los datos ya procesados al Servicio de Analítica
    datos_ingresos = AnaliticaService.obtener_datos_ingresos()
    nombres_prod, cantidades_prod = AnaliticaService.obtener_top_productos()
    tabla_meses = AnaliticaService.obtener_temporadas_demanda()

    # 3. Entrega los datos a la plantilla
    return render_template('reportes.html', 
                           datos_ingresos=datos_ingresos,
                           nombres_prod=nombres_prod,
                           cantidades_prod=cantidades_prod,
                           tabla_meses=tabla_meses)