# ai_models/mistral.py
import os
# Usamos MistralClient porque es la clase correcta para la versión 0.4.2 de la librería
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .base_model import AIModel, logger

class MistralModel(AIModel):
    """
    Conector para la API de Mistral AI (compatible con la versión 0.4.2 de la librería).
    """

    def _validate_config(self):
        """Valida la configuración específica de Mistral."""
        super()._validate_config()
        if 'api_key_env' not in self.config or 'model_name_api' not in self.config:
            raise ValueError("La configuración de Mistral debe contener 'api_key_env' y 'model_name_api'.")

    def _initialize_model(self):
        """Configura el cliente de Mistral usando la API key del entorno."""
        api_key_env_var = self.config['api_key_env']
        api_key = os.getenv(api_key_env_var)

        if not api_key:
            raise ValueError(f"La variable de entorno '{api_key_env_var}' no está configurada.")
        
        # Usamos la clase MistralClient
        self.client = MistralClient(api_key=api_key)

    def query(self, prompt: str, options: dict = None) -> str:
        """
        Envía un prompt a la API de Mistral y devuelve la respuesta.
        """
        super().query(prompt, options)
        if self.initialization_error:
            return self.initialization_error
            
        try:
            # En esta versión, sí es necesario usar ChatMessage
            messages = [ChatMessage(role="user", content=prompt)]

            api_params = {
                'model': self.config['model_name_api'],
                'messages': messages
            }
            if options:
                if 'temperature' in options:
                    api_params['temperature'] = min(max(options['temperature'], 0.0), 1.0)
                if 'max_tokens' in options:
                    api_params['max_tokens'] = options['max_tokens']
            
            chat_response = self.client.chat(**api_params)
            
            logger.info(f"Respuesta recibida de {self.name}.")
            return chat_response.choices[0].message.content

        except Exception as e:
            error_message = f"Error al consultar la API de Mistral ({self.name}): {str(e)}"
            logger.error(error_message)
            return error_message
