"""
Sistema de Logging Avanzado para Nutrition Intelligence
Genera logs en formato JSON estructurado + formato legacy con pipes
Enhanced with RotatingFileHandler for production use
"""
import json
import os
import gzip
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, date
from pathlib import Path
import threading
from typing import Dict, Any, Optional, Union
from enum import Enum
import uuid

class LogLevel(str, Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"
    DEBUG = "Debug"

class NutritionLogger:
    """Logger principal con formato dual (JSON + Legacy pipes)"""
    
    def __init__(self, app_name: str = "nutrition-intelligence-api", logs_base_dir: str = "logs"):
        self.app_name = app_name
        self.logs_base_dir = Path(logs_base_dir)
        self.app_logs_dir = self.logs_base_dir / app_name
        self.archive_dir = self.app_logs_dir / "archives"
        
        # Crear directorios si no existen
        self.app_logs_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.lock = threading.Lock()
        
        # Configuración
        self.max_file_size_mb = 100  # Rotar archivo si supera 100MB
        self.keep_days = 30  # Mantener logs por 30 días
        
    def _get_current_date(self) -> str:
        """Obtener fecha actual en formato YYYY-MM-DD"""
        return date.today().strftime("%Y-%m-%d")
    
    def _get_timestamp(self) -> str:
        """Obtener timestamp ISO con zona UTC"""
        return datetime.utcnow().isoformat() + "Z"
    
    def _ensure_log_rotation(self, file_path: Path):
        """Verificar si necesita rotación por tamaño"""
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > self.max_file_size_mb:
                # Comprimir y mover a archive
                timestamp = datetime.now().strftime("%H%M%S")
                archive_name = f"{file_path.stem}_{timestamp}.gz"
                archive_path = self.archive_dir / archive_name
                
                with open(file_path, 'rb') as f_in:
                    with gzip.open(archive_path, 'wb') as f_out:
                        f_out.writelines(f_in)
                
                # Limpiar archivo original
                file_path.unlink()
    
    def _clean_old_logs(self):
        """Limpiar logs antiguos según configuración"""
        try:
            current_date = date.today()
            
            # Buscar archivos de log antiguos
            for log_file in self.app_logs_dir.glob("*.json"):
                try:
                    file_date_str = log_file.stem  # YYYY-MM-DD
                    file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
                    
                    days_old = (current_date - file_date).days
                    if days_old > self.keep_days:
                        # Comprimir antes de eliminar
                        archive_name = f"{log_file.stem}.gz"
                        archive_path = self.archive_dir / archive_name
                        
                        if not archive_path.exists():
                            with open(log_file, 'rb') as f_in:
                                with gzip.open(archive_path, 'wb') as f_out:
                                    f_out.writelines(f_in)
                        
                        log_file.unlink()
                        
                        # También eliminar archivo legacy correspondiente
                        legacy_file = log_file.with_suffix('.legacy')
                        if legacy_file.exists():
                            legacy_file.unlink()
                            
                except ValueError:
                    # Skip files that don't match date format
                    continue
                    
        except Exception as e:
            # Error en limpieza no debe afectar logging principal
            print(f"Warning: Error during log cleanup: {e}")
    
    def log_request(self,
                   status: Union[LogLevel, str],
                   message: str,
                   request_id: Optional[str] = None,
                   endpoint: Optional[str] = None,
                   method: Optional[str] = None,
                   user_id: Optional[str] = None,
                   response_time_ms: Optional[int] = None,
                   status_code: Optional[int] = None,
                   metadata: Optional[Dict[str, Any]] = None,
                   business_context: Optional[Dict[str, Any]] = None):
        """
        Registrar un evento del sistema
        
        Args:
            status: Success/Error/Warning/Info/Debug
            message: Mensaje descriptivo del evento
            request_id: ID único del request (se genera automáticamente si no se proporciona)
            endpoint: Endpoint de la API (ej: /api/v1/users/me)
            method: Método HTTP (GET, POST, etc)
            user_id: ID del usuario que ejecuta la acción
            response_time_ms: Tiempo de respuesta en millisegundos
            status_code: Código de status HTTP
            metadata: Metadatos técnicos (IP, user agent, etc)
            business_context: Contexto de negocio (paciente_id, receta_id, etc)
        """
        
        timestamp = self._get_timestamp()
        today = self._get_current_date()
        
        # Generar request_id si no se proporciona
        if not request_id:
            request_id = f"req_{uuid.uuid4().hex[:8]}"
        
        # Asegurar que status es string
        status_str = status.value if isinstance(status, LogLevel) else str(status)
        
        # Construir log entry estructurado (JSON)
        log_entry = {
            "status": status_str,
            "application": self.app_name,
            "timestamp": timestamp,
            "request_id": request_id,
            "message": message,
            
            # Request details
            "endpoint": endpoint,
            "method": method,
            "user_id": user_id,
            "response_time_ms": response_time_ms,
            "status_code": status_code,
            
            # Technical metadata
            "metadata": metadata or {},
            
            # Business context
            "business_context": business_context or {}
        }
        
        # Formato legacy con pipes (tu estándar)
        legacy_entry = f"{status_str}|{self.app_name}|{timestamp}|Mensaje: {message}"
        
        # Agregar contexto adicional al formato legacy si es relevante
        if business_context:
            context_parts = []
            for key, value in business_context.items():
                context_parts.append(f"{key}:{value}")
            if context_parts:
                legacy_entry += f" - Contexto: {', '.join(context_parts)}"
        
        log_entry["legacy_format"] = legacy_entry
        
        # Escribir logs de forma thread-safe
        with self.lock:
            try:
                # Definir archivos del día
                json_file = self.app_logs_dir / f"{today}.json"
                legacy_file = self.app_logs_dir / f"{today}.legacy"
                
                # Verificar rotación antes de escribir
                self._ensure_log_rotation(json_file)
                self._ensure_log_rotation(legacy_file)
                
                # Escribir JSON estructurado
                with open(json_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False, separators=(',', ':')) + "\n")
                
                # Escribir formato legacy
                with open(legacy_file, "a", encoding="utf-8") as f:
                    f.write(legacy_entry + "\n")
                
                # Limpiar logs antiguos (una vez por día)
                if datetime.now().hour == 0 and datetime.now().minute < 5:
                    self._clean_old_logs()
                    
            except Exception as e:
                # Fallback: imprimir en consola si falla escritura a archivo
                print(f"LOGGING ERROR: {e}")
                print(f"FAILED LOG: {legacy_entry}")
    
    # Métodos de conveniencia para diferentes niveles
    def log_success(self, message: str, **kwargs):
        """Log de operación exitosa"""
        self.log_request(LogLevel.SUCCESS, message, **kwargs)
    
    def log_error(self, message: str, **kwargs):
        """Log de error"""
        self.log_request(LogLevel.ERROR, message, **kwargs)
    
    def log_warning(self, message: str, **kwargs):
        """Log de advertencia"""
        self.log_request(LogLevel.WARNING, message, **kwargs)
    
    def log_info(self, message: str, **kwargs):
        """Log informativo"""
        self.log_request(LogLevel.INFO, message, **kwargs)
    
    def log_debug(self, message: str, **kwargs):
        """Log de debug"""
        self.log_request(LogLevel.DEBUG, message, **kwargs)
    
    # Métodos específicos para contextos de negocio
    def log_nutritional_calculation(self, patient_id: int, calories: float, equivalents: Dict[str, float], success: bool = True):
        """Log específico para cálculos nutricionales"""
        status = LogLevel.SUCCESS if success else LogLevel.ERROR
        equivalents_str = ", ".join([f"{k}:{v}" for k, v in equivalents.items()])
        
        message = f"Cálculo nutricional {'completado' if success else 'fallido'} - {calories} kcal, {len(equivalents)} grupos"
        
        self.log_request(
            status=status,
            message=message,
            business_context={
                "action": "nutritional_calculation",
                "patient_id": patient_id,
                "target_calories": calories,
                "equivalents_count": len(equivalents),
                "equivalents_detail": equivalents_str
            }
        )
    
    def log_recipe_interaction(self, user_id: str, recipe_id: int, action: str, rating: Optional[int] = None):
        """Log específico para interacciones con recetas"""
        message = f"Receta {action} - Usuario: {user_id}, Receta: {recipe_id}"
        
        business_context = {
            "action": "recipe_interaction",
            "user_id": user_id,
            "recipe_id": recipe_id,
            "interaction_type": action
        }
        
        if rating:
            message += f", Calificación: {rating}"
            business_context["rating"] = rating
        
        self.log_success(message, business_context=business_context)
    
    def log_meal_plan_assignment(self, nutritionist_id: str, patient_id: int, plan_id: int, recipes_count: int):
        """Log específico para asignación de planes alimenticios"""
        message = f"Plan alimenticio asignado - {recipes_count} recetas para paciente {patient_id}"
        
        self.log_success(
            message,
            business_context={
                "action": "meal_plan_assignment",
                "nutritionist_id": nutritionist_id,
                "patient_id": patient_id,
                "plan_id": plan_id,
                "recipes_count": recipes_count
            }
        )
    
    def log_equivalences_tracking(self, patient_id: int, equivalents_consumed: Dict[str, float], adherence_pct: float):
        """Log específico para seguimiento de equivalentes"""
        total_equivalents = sum(equivalents_consumed.values())
        message = f"Equivalentes registrados - {total_equivalents:.1f} total, {adherence_pct:.1f}% adherencia"
        
        self.log_success(
            message,
            business_context={
                "action": "equivalences_tracking",
                "patient_id": patient_id,
                "total_equivalents": total_equivalents,
                "adherence_percentage": adherence_pct,
                "equivalents_detail": equivalents_consumed
            }
        )

# Instancia global del logger
nutrition_logger = NutritionLogger()

# Funciones de conveniencia para uso directo
def log_success(message: str, **kwargs):
    nutrition_logger.log_success(message, **kwargs)

def log_error(message: str, **kwargs):
    nutrition_logger.log_error(message, **kwargs)

def log_warning(message: str, **kwargs):
    nutrition_logger.log_warning(message, **kwargs)

def log_info(message: str, **kwargs):
    nutrition_logger.log_info(message, **kwargs)

def log_nutritional_calculation(patient_id: int, calories: float, equivalents: Dict[str, float], success: bool = True):
    nutrition_logger.log_nutritional_calculation(patient_id, calories, equivalents, success)

def log_recipe_interaction(user_id: str, recipe_id: int, action: str, rating: Optional[int] = None):
    nutrition_logger.log_recipe_interaction(user_id, recipe_id, action, rating)

def log_meal_plan_assignment(nutritionist_id: str, patient_id: int, plan_id: int, recipes_count: int):
    nutrition_logger.log_meal_plan_assignment(nutritionist_id, patient_id, plan_id, recipes_count)

def log_equivalences_tracking(patient_id: int, equivalents_consumed: Dict[str, float], adherence_pct: float):
    nutrition_logger.log_equivalences_tracking(patient_id, equivalents_consumed, adherence_pct)