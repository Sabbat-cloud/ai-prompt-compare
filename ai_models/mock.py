# ai_models/mock.py
import time
from .base_model import AIModel, logger

class MockModel(AIModel):
    """
    Un modelo de IA falso para fines de desarrollo y pruebas.
    """

    def _validate_config(self):
        """
        No se necesita una validación especial para el modelo mock.
        """
        super()._validate_config()

    def _initialize_model(self):
        """
        No se requiere inicialización para el modelo mock.
        """
        pass

    # CORRECCIÓN AQUÍ: Añadimos `options: dict = None` para que acepte los nuevos parámetros
    def query(self, prompt: str, options: dict = None) -> str:
        """
        Simula una llamada a una API de IA.
        """
        # La llamada a super() ahora necesita los `options`
        super().query(prompt, options) 
        if self.initialization_error:
            return self.initialization_error

        logger.info(f"Mock AI recibiendo prompt: '{prompt[:30]}...' con opciones: {options}")

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
