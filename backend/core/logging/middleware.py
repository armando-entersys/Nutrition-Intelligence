"""
Middleware de Logging Automático para FastAPI
Captura automáticamente todas las requests y responses
"""
import time
import uuid
from typing import Callable, Dict, Any, Optional
import json
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import traceback

from .nutrition_logger import nutrition_logger, LogLevel

class LoggingMiddleware:
    """Middleware para captura automática de logs de requests"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Generar ID único para la request
            request_id = f"req_{uuid.uuid4().hex[:8]}"
            request.state.request_id = request_id
            
            # Capturar información de la request
            start_time = time.time()
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "")
            
            # Extraer user_id del token si está disponible
            user_id = await self._extract_user_id(request)
            
            try:
                # Procesar request
                async def send_wrapper(message):
                    if message["type"] == "http.response.start":
                        # Calcular tiempo de respuesta
                        response_time_ms = int((time.time() - start_time) * 1000)
                        status_code = message["status"]
                        
                        # Determinar si es success o error
                        is_success = 200 <= status_code < 400
                        status = LogLevel.SUCCESS if is_success else LogLevel.ERROR
                        
                        # Construir mensaje
                        endpoint = request.url.path
                        method = request.method
                        
                        if is_success:
                            message_text = f"{method} {endpoint} - {status_code}"
                        else:
                            message_text = f"Error en {method} {endpoint} - Status {status_code}"
                        
                        # Metadatos técnicos
                        metadata = {
                            "ip": client_ip,
                            "user_agent": user_agent,
                            "content_type": request.headers.get("content-type", ""),
                            "query_params": dict(request.query_params) if request.query_params else None
                        }
                        
                        # Contexto de negocio basado en endpoint
                        business_context = await self._extract_business_context(request, status_code)
                        
                        # Log automático
                        nutrition_logger.log_request(
                            status=status,
                            message=message_text,
                            request_id=request_id,
                            endpoint=endpoint,
                            method=method,
                            user_id=user_id,
                            response_time_ms=response_time_ms,
                            status_code=status_code,
                            metadata=metadata,
                            business_context=business_context
                        )
                    
                    await send(message)
                
                await self.app(scope, receive, send_wrapper)
                
            except Exception as e:
                # Log de error de la aplicación
                response_time_ms = int((time.time() - start_time) * 1000)
                error_type = type(e).__name__
                
                nutrition_logger.log_error(
                    message=f"Excepción no manejada en {request.method} {request.url.path}: {str(e)}",
                    request_id=request_id,
                    endpoint=request.url.path,
                    method=request.method,
                    user_id=user_id,
                    response_time_ms=response_time_ms,
                    status_code=500,
                    metadata={
                        "ip": client_ip,
                        "user_agent": user_agent,
                        "error_type": error_type,
                        "traceback": traceback.format_exc()
                    }
                )
                
                # Re-raise la excepción para que FastAPI la maneje
                raise
        else:
            # Para websockets u otros tipos, pasar sin procesamiento
            await self.app(scope, receive, send)
    
    async def _extract_user_id(self, request: Request) -> Optional[str]:
        """Extraer user ID del token de autorización"""
        try:
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                # Aquí podrías decodificar el JWT para extraer el user_id
                # Por simplicidad, usamos el request state si está disponible
                return getattr(request.state, 'current_user_id', None)
            return None
        except Exception:
            return None
    
    async def _extract_business_context(self, request: Request, status_code: int) -> Dict[str, Any]:
        """Extraer contexto de negocio basado en el endpoint"""
        context = {}
        path = request.url.path
        
        try:
            # Extraer IDs de la URL
            path_parts = path.split('/')
            
            # Detectar patrones comunes
            if '/patients/' in path:
                for i, part in enumerate(path_parts):
                    if part == 'patients' and i + 1 < len(path_parts):
                        if path_parts[i + 1].isdigit():
                            context['patient_id'] = int(path_parts[i + 1])
                        break
            
            if '/recipes/' in path:
                for i, part in enumerate(path_parts):
                    if part == 'recipes' and i + 1 < len(path_parts):
                        if path_parts[i + 1].isdigit():
                            context['recipe_id'] = int(path_parts[i + 1])
                        break
            
            if '/nutritionists/' in path:
                for i, part in enumerate(path_parts):
                    if part == 'nutritionists' and i + 1 < len(path_parts):
                        if path_parts[i + 1].isdigit():
                            context['nutritionist_id'] = int(path_parts[i + 1])
                        break
            
            # Detectar tipo de acción basado en endpoint
            if path.endswith('/nutritional-profile'):
                context['action'] = 'nutritional_profile_management'
            elif '/equivalences/' in path:
                context['action'] = 'equivalences_management'
            elif '/weekly-plans' in path:
                context['action'] = 'meal_planning'
            elif '/auth/' in path:
                context['action'] = 'authentication'
            
            # Agregar información del método HTTP
            context['http_method'] = request.method
            context['endpoint_category'] = self._categorize_endpoint(path)
            
            # Si es error, marcar como tal
            if status_code >= 400:
                context['has_error'] = True
                context['error_category'] = self._categorize_error(status_code)
            
        except Exception as e:
            # No fallar si hay error extrayendo contexto
            context['context_extraction_error'] = str(e)
        
        return context
    
    def _categorize_endpoint(self, path: str) -> str:
        """Categorizar endpoint para métricas"""
        if '/auth/' in path:
            return 'authentication'
        elif '/equivalences/' in path:
            return 'nutrition_equivalences'
        elif '/patients/' in path:
            return 'patient_management'
        elif '/nutritionists/' in path:
            return 'nutritionist_management'
        elif '/recipes/' in path:
            return 'recipe_management'
        elif '/meal-plans/' in path or '/weekly-plans' in path:
            return 'meal_planning'
        elif '/foods/' in path:
            return 'food_management'
        elif '/users/' in path:
            return 'user_management'
        elif '/health' in path or '/docs' in path:
            return 'system'
        else:
            return 'other'
    
    def _categorize_error(self, status_code: int) -> str:
        """Categorizar tipo de error"""
        if status_code == 400:
            return 'bad_request'
        elif status_code == 401:
            return 'authentication_error'
        elif status_code == 403:
            return 'authorization_error'
        elif status_code == 404:
            return 'not_found'
        elif status_code == 422:
            return 'validation_error'
        elif 500 <= status_code < 600:
            return 'server_error'
        else:
            return 'client_error'

def create_request_logging_middleware():
    """Factory function para crear el middleware"""
    def logging_middleware(request: Request, call_next: Callable) -> Callable:
        return LoggingMiddleware.process_request(request, call_next)
    
    return logging_middleware

# Context manager para logging de operaciones específicas
class LoggingContext:
    """Context manager para operaciones que requieren logging detallado"""
    
    def __init__(self, operation_name: str, business_context: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.business_context = business_context or {}
        self.start_time = None
        self.request_id = f"op_{uuid.uuid4().hex[:8]}"
    
    def __enter__(self):
        self.start_time = time.time()
        nutrition_logger.log_info(
            f"Iniciando operación: {self.operation_name}",
            request_id=self.request_id,
            business_context=self.business_context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self.start_time) * 1000)
        
        if exc_type is None:
            # Operación exitosa
            nutrition_logger.log_success(
                f"Operación completada: {self.operation_name}",
                request_id=self.request_id,
                response_time_ms=duration_ms,
                business_context=self.business_context
            )
        else:
            # Operación falló
            nutrition_logger.log_error(
                f"Operación falló: {self.operation_name} - {exc_val}",
                request_id=self.request_id,
                response_time_ms=duration_ms,
                business_context={
                    **self.business_context,
                    'error_type': exc_type.__name__,
                    'error_message': str(exc_val)
                }
            )
    
    def add_context(self, **kwargs):
        """Agregar contexto adicional durante la operación"""
        self.business_context.update(kwargs)
    
    def log_checkpoint(self, checkpoint_name: str, **additional_context):
        """Log de checkpoint durante la operación"""
        nutrition_logger.log_info(
            f"Checkpoint: {checkpoint_name} en operación {self.operation_name}",
            request_id=self.request_id,
            business_context={
                **self.business_context,
                'checkpoint': checkpoint_name,
                **additional_context
            }
        )

# Decorador para funciones que requieren logging automático
def log_operation(operation_name: str, log_params: bool = False):
    """
    Decorador para logging automático de funciones
    
    Args:
        operation_name: Nombre de la operación para el log
        log_params: Si debe registrar los parámetros de la función
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            business_context = {'operation': operation_name}
            
            if log_params:
                business_context['params'] = {
                    'args_count': len(args),
                    'kwargs': {k: str(v)[:100] for k, v in kwargs.items()}  # Truncar valores largos
                }
            
            with LoggingContext(operation_name, business_context) as ctx:
                try:
                    result = await func(*args, **kwargs)
                    ctx.add_context(success=True, result_type=type(result).__name__)
                    return result
                except Exception as e:
                    ctx.add_context(error=str(e))
                    raise
        
        def sync_wrapper(*args, **kwargs):
            business_context = {'operation': operation_name}
            
            if log_params:
                business_context['params'] = {
                    'args_count': len(args),
                    'kwargs': {k: str(v)[:100] for k, v in kwargs.items()}
                }
            
            with LoggingContext(operation_name, business_context) as ctx:
                try:
                    result = func(*args, **kwargs)
                    ctx.add_context(success=True, result_type=type(result).__name__)
                    return result
                except Exception as e:
                    ctx.add_context(error=str(e))
                    raise
        
        # Retornar wrapper apropiado según si la función es async o no
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator