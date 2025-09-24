"""
Funciones de utilidad para respuestas de la API
"""

from flask import jsonify


def success_response(data=None, message=None, status_code=200):
    """
    Crear respuesta exitosa estándar
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje opcional
        status_code: Código de estado HTTP
    
    Returns:
        Respuesta JSON con formato estándar
    """
    response = {
        'success': True
    }
    
    if data is not None:
        response['data'] = data
        
    if message:
        response['message'] = message
        
    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    """
    Crear respuesta de error estándar
    
    Args:
        message: Mensaje de error
        status_code: Código de estado HTTP
        errors: Errores adicionales (ej. errores de validación)
    
    Returns:
        Respuesta JSON con formato de error estándar
    """
    response = {
        'success': False,
        'message': message
    }
    
    if errors:
        response['errors'] = errors
        
    return jsonify(response), status_code


def paginated_response(items, page, per_page, total, endpoint, **kwargs):
    """
    Crear respuesta paginada estándar
    
    Args:
        items: Lista de elementos
        page: Página actual
        per_page: Elementos por página
        total: Total de elementos
        endpoint: Endpoint para links de paginación
        **kwargs: Parámetros adicionales para URLs
    
    Returns:
        Respuesta JSON con datos paginados
    """
    from flask import url_for, request
    
    # Calcular información de paginación
    has_prev = page > 1
    has_next = page * per_page < total
    total_pages = (total + per_page - 1) // per_page
    
    # Generar URLs de paginación
    def get_page_url(page_num):
        args = request.args.copy()
        args['page'] = page_num
        args.update(kwargs)
        return url_for(endpoint, **args)
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next
    }
    
    # URLs de navegación
    if has_prev:
        pagination_info['prev_url'] = get_page_url(page - 1)
    if has_next:
        pagination_info['next_url'] = get_page_url(page + 1)
        
    # Primera y última página
    if total_pages > 0:
        pagination_info['first_url'] = get_page_url(1)
        pagination_info['last_url'] = get_page_url(total_pages)
    
    response_data = {
        'items': items,
        'pagination': pagination_info
    }
    
    return success_response(response_data)


def validation_error_response(validation_errors):
    """
    Crear respuesta de error de validación
    
    Args:
        validation_errors: Errores de validación de Marshmallow
    
    Returns:
        Respuesta JSON con errores de validación
    """
    return error_response(
        message='Errores de validación en los datos enviados',
        status_code=422,
        errors=validation_errors
    )