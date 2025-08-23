# ai_models/claude.py
import os
import anthropic
from .base_model import AIModel, logger

class ClaudeModel(AIModel):
    """
    Conector para la API de Anthropic (Claude).
    """

    def _validate_config(self):
        super()._validate_config()
        if 'api_key_env' not in self.config or 'model_name_api' not in self.config:
            raise ValueError("La configuración de Claude debe contener 'api_key_env' y 'model_name_api'.")

    def _initialize_model(self):
        api_key_env_var = self.config['api_key_env']
        api_key = os.getenv(api_key_env_var)
        if not api_key:
            raise ValueError(f"La variable de entorno '{api_key_env_var}' no está configurada.")
        self.client = anthropic.Anthropic(api_key=api_key)

class ClaudeModel(AIModel):
    # ... (_validate_config y _initialize_model no cambian) ...

    def query(self, prompt: str, options: dict = None) -> str:
        super().query(prompt, options)
        if self.initialization_error: return self.initialization_error

        try:
            # Parámetros para la API de Anthropic
            api_params = {
                'model': self.config['model_name_api'],
                'max_tokens': options.get('max_tokens', 2048), # Valor por defecto si no se proporciona
                'messages': [{"role": "user", "content": prompt}]
            }
            if options and 'temperature' in options:
                api_params['temperature'] = options['temperature']

            message = self.client.messages.create(**api_params)
            logger.info(f"Respuesta recibida de {self.name}.")
            return message.content[0].text
        except Exception as e:
            error_message = f"Error al consultar la API de Anthropic ({self.name}): {e}"
            logger.error(error_message)
            return error_message
