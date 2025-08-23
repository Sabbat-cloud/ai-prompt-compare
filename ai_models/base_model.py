# ai_models/base_model.py
from abc import ABC, abstractmethod
import logging

# Configura un logger específico para los modelos de IA
logger = logging.getLogger(__name__)

class AIModel(ABC):
    """
    Clase base abstracta mejorada para todos los modelos de IA.
    Define una estructura robusta que incluye inicialización, validación y consulta.
    """

    def __init__(self, config):
        """
        Constructor que recibe la configuración y la valida.
        """
        self.config = config
        self.name = config.get('name', 'Modelo Desconocido')
        self.initialization_error = None
        
        try:
            self._validate_config()
            self._initialize_model()
            logger.info(f"Modelo '{self.name}' inicializado correctamente.")
        except Exception as e:
            self.initialization_error = f"Error al inicializar {self.name}: {e}"
            logger.error(self.initialization_error)
            self.model = None

    @abstractmethod
    def _validate_config(self):
        """
        Valida que la configuración esencial para el modelo está presente.
        Debe lanzar un `ValueError` si falta algo.
        """
        if 'name' not in self.config or 'module_path' not in self.config:
            raise ValueError("La configuración debe contener 'name' y 'module_path'.")

    @abstractmethod
    def _initialize_model(self):
        """
        Prepara el cliente o la conexión con la API del modelo.
        Este es el lugar para configurar API keys y URLs base.
        """
        pass
    @abstractmethod
    def query(self, prompt: str, options: dict = None) -> str:
        """
        Método abstracto para realizar una consulta, ahora con parámetros opcionales.

        Args:
            prompt (str): La pregunta o prompt.
            options (dict, optional): Un diccionario con parámetros como 'temperature' o 'max_tokens'.
        """
        if self.initialization_error:
            return self.initialization_error
        
        if not prompt:
            return "Error: El prompt no puede estar vacío."
            
        logger.info(f"Enviando prompt a {self.name} con opciones: {options}")

