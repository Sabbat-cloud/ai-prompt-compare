# ai_models/mock.py
import time
from .base_model import AIModel, logger

class MockModel(AIModel):
    """
    Un modelo de IA falso para fines de desarrollo y pruebas.
    Hereda de la clase base AIModel y ahora implementa los métodos abstractos requeridos.
    """

    def _validate_config(self):
        """
        No se necesita una validación especial para el modelo mock.
        Llamamos a super() por si en el futuro la base tiene validaciones.
        """
        super()._validate_config()

    def _initialize_model(self):
        """
        No se requiere inicialización para el modelo mock, ya que no se conecta a ninguna API.
        """
        # No es necesario hacer nada aquí.
        pass

    def query(self, prompt: str) -> str:
        """
        Simula una llamada a una API de IA.
        Espera un par de segundos y devuelve una respuesta predefinida.

        Args:
            prompt (str): El prompt del usuario (no se utiliza en esta simulación).

        Returns:
            str: Una respuesta de prueba.
        """
        super().query(prompt) # Llama al método base para validaciones y logging
        if self.initialization_error:
            return self.initialization_error

        logger.info(f"Mock AI recibiendo prompt: '{prompt[:30]}...'")

        # Simulamos un retraso como si fuera una llamada de red real
        time.sleep(2)

        response = (
            f"Soy {self.name}, un modelo de prueba. "
            "He recibido tu prompt que empezaba con:\n\n"
            f"'{prompt[:100]}...'\n\n"
            "Mi única función es devolver este texto para verificar que la aplicación funciona correctamente."
        )

        logger.info("Mock AI devolviendo respuesta.")
        return response
