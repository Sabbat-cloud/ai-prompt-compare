# ai_models/gemini.py
import os
import google.generativeai as genai
from .base_model import AIModel, logger

class GeminiModel(AIModel):
    """
    Conector para la API de Google Gemini, adaptado a la nueva clase base.
    """

    def _validate_config(self):
        """Valida la configuración específica de Gemini."""
        super()._validate_config()
        if 'api_key_env' not in self.config or 'model_name_api' not in self.config:
            raise ValueError("La configuración de Gemini debe contener 'api_key_env' y 'model_name_api'.")

    def _initialize_model(self):
        """Configura el modelo Gemini usando la API key del entorno."""
        api_key_env_var = self.config['api_key_env']
        api_key = os.getenv(api_key_env_var)

        if not api_key:
            raise ValueError(f"La variable de entorno '{api_key_env_var}' no está configurada.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.config['model_name_api'])
    
    def query(self, prompt: str, options: dict = None) -> str:
        super().query(prompt, options)
        if self.initialization_error: return self.initialization_error
            
        try:
            # Configuración de generación con los nuevos parámetros
            generation_config = {}
            if options:
                if 'temperature' in options:
                    generation_config['temperature'] = options['temperature']
                if 'max_tokens' in options:
                    generation_config['max_output_tokens'] = options['max_tokens']

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config if generation_config else None
            )
            logger.info(f"Respuesta recibida de {self.name}.")
            return response.text
        except Exception as e:
            error_message = f"Error al consultar la API de Gemini ({self.name}): {e}"
            logger.error(error_message)
            return error_message
