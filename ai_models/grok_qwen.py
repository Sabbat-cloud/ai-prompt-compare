# ai_models/groq_qwen.py
import os
from groq import Groq
from .base_model import AIModel, logger

class GroqQwenModel(AIModel):
    """
    Conector para la API de Groq, adaptado a la nueva clase base.
    """

    def _validate_config(self):
        super()._validate_config()
        if 'api_key_env' not in self.config or 'model_name_api' not in self.config:
            raise ValueError("La configuración de Groq debe contener 'api_key_env' y 'model_name_api'.")

    def _initialize_model(self):
        api_key_env_var = self.config['api_key_env']
        api_key = os.getenv(api_key_env_var)
        if not api_key:
            raise ValueError(f"La variable de entorno '{api_key_env_var}' no está configurada.")
        self.client = Groq(api_key=api_key)
class DeepSeekModel(AIModel):
    # ... (_validate_config y _initialize_model no cambian) ...

    def query(self, prompt: str, options: dict = None) -> str:
        super().query(prompt, options)
        if self.initialization_error: return self.initialization_error

        try:
            # Parámetros para la API compatible con OpenAI
            api_params = {
                'model': self.config['model_name_api'],
                'messages': [{"role": "user", "content": prompt}]
            }
            if options:
                if 'temperature' in options:
                    api_params['temperature'] = options['temperature']
                if 'max_tokens' in options:
                    api_params['max_tokens'] = options['max_tokens']

            chat_completion = self.client.chat.completions.create(**api_params)
            logger.info(f"Respuesta recibida de {self.name}.")
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_message = f"Error al consultar la API de Grok ({self.name}): {e}"
            logger.error(error_message)
            return error_message
