README.es.md (Español)
🚀 IA-Prompt-Compare
IA-Prompt-Compare es una potente aplicación web construida con Flask que te permite interactuar con múltiples modelos de lenguaje de IA de forma simultánea. Ha sido diseñada para desarrolladores, investigadores y entusiastas de la IA que deseen comparar el rendimiento de diferentes modelos o crear conversaciones complejas entre ellos.

La aplicación cuenta con una interfaz de usuario intuitiva y dos modos de operación principales para explorar las capacidades de los modelos de IA más avanzados.

✨ Características Principales
Modo Comparar: Envía un único prompt a todos los modelos de IA configurados y visualiza sus respuestas una al lado de la otra. Es ideal para evaluar la calidad, el estilo y la precisión de cada modelo.

Modo Conversación: Inicia una cadena de diálogo donde la respuesta de un modelo se convierte en el prompt para el siguiente. Esto permite crear debates, tormentas de ideas o ver cómo las IAs colaboran o divergen en un tema.

Configuración Avanzada: Ajusta parámetros como la temperatura (para controlar la creatividad) y el máximo de tokens (para limitar la longitud de la respuesta) para afinar los resultados.

Arquitectura Modular: Añadir un nuevo modelo de IA es sencillo. Solo necesitas crear una nueva clase conector en el directorio ai_models y añadir su configuración en models.json.

Seguridad: El acceso a la aplicación está protegido por autenticación básica, asegurando que solo los usuarios autorizados puedan utilizarla.

Interfaz Moderna: La interfaz está construida con Tailwind CSS, es limpia, responsiva y fácil de usar.

🛠️ Guía de Instalación y Configuración
Sigue estos pasos para poner en marcha el proyecto en tu entorno local.

1. Prerrequisitos
Python 3.10 o superior.

pip y venv instalados.

Claves de API para los modelos de IA que desees utilizar (Gemini, Mistral, DeepSeek, etc.).

2. Clonar el Repositorio
Bash

git clone https://github.com/tu_usuario/ia-prompt-compare.git
cd ia-prompt-compare
3. Crear y Activar un Entorno Virtual
Es una buena práctica utilizar un entorno virtual para aislar las dependencias del proyecto.

En macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
En Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
4. Instalar Dependencias
Instala todas las librerías necesarias utilizando el fichero requirements.txt.

Bash

pip install -r requirements.txt
5. Configurar las Claves de API (.env)
La aplicación carga las claves de API desde un fichero .env.

Crea una copia del fichero de ejemplo .env.EXAMPLE y renómbrala a .env:

Bash

cp .env.EXAMPLE .env
Abre el fichero .env y añade tus claves de API. No es necesario rellenarlas todas, solo las de los modelos que vayas a activar en models.json.

Ini, TOML

GEMINI_API_KEY=TU_API_KEY_DE_GEMINI
MISTRAL_API_KEY=TU_API_KEY_DE_MISTRAL
GROK_API_KEY=TU_API_KEY_DE_GROQ
DEEPSEEK_API_KEY=TU_API_KEY_DE_DEEPSEEK
ANTHROPIC_API_KEY=TU_API_KEY_DE_ANTHROPIC
6. Configurar Usuarios (users.json)
La autenticación se gestiona a través de un fichero users.json.

Generar un Hash de Contraseña: El proyecto incluye un script para generar hashes seguros para tus contraseñas. Ejecútalo con la contraseña que desees:

Bash

python hash_generator.py 'tu_contraseña_segura'
Crear users.json:

Crea una copia de users.json.EXAMPLE y renómbrala a users.json.

Abre el fichero y edítalo. Reemplaza el nombre de usuario y el hash con los tuyos. Puedes añadir tantos usuarios como necesites.

JSON

{
  "tu_usuario": "scrypt:32768:8:1$...",
  "otro_usuario": "scrypt:32768:8:1$..."
}
7. Configurar los Modelos (models.json)
El fichero models.json te permite activar o desactivar los modelos de IA que se mostrarán en la interfaz.

Para activar un modelo, cambia su propiedad "enabled" a true.

Para desactivar un modelo, ponla en false.

JSON

{
  "models": [
    {
      "name": "Gemini 1.5 Flash",
      "enabled": true,
      "module_path": "ai_models.gemini",
      "class_name": "GeminiModel",
      "model_name_api": "gemini-1.5-flash-latest",
      "api_key_env": "GEMINI_API_KEY"
    },
    {
      "name": "Codestral (Mistral)",
      "enabled": false,
      "module_path": "ai_models.mistral",
      "class_name": "MistralModel",
      "model_name_api": "codestral-latest",
      "api_key_env": "MISTRAL_API_KEY"
    }
    // ... otros modelos
  ]
}
▶️ Ejecutar la Aplicación
Una vez completada la configuración, inicia el servidor de producción usando waitress:

Bash

python app.py
La aplicación estará disponible en http://0.0.0.0:3556. Cuando accedas desde tu navegador, se te pedirá un nombre de usuario y contraseña.

📄 Licencia
Este proyecto está bajo la Licencia MIT.
