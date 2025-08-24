-----

# 🚀 AI-Prompt-Compare

AI-Prompt-Compare es una potente aplicación web construida con Flask que te permite interactuar con múltiples modelos de lenguaje de IA de forma simultánea. Ha sido diseñada para desarrolladores, investigadores y entusiastas de la IA que deseen comparar el rendimiento de diferentes modelos o crear conversaciones complejas entre ellos.

La aplicación cuenta con una interfaz de usuario intuitiva y dos modos de operación principales para explorar las capacidades de los modelos de IA más avanzados.

## ✨ Características Principales

  - **Modo Comparar**: Envía un único prompt a todos los modelos de IA configurados y visualiza sus respuestas una al lado de la otra.
  - **Modo Conversación**: Inicia una cadena de diálogo donde la respuesta de un modelo se convierte en el prompt para el siguiente.
  - **Configuración Avanzada**: Ajusta parámetros como la `temperatura` y el `máximo de tokens`.
  - **Arquitectura Modular**: Añadir un nuevo modelo de IA es sencillo.
  - **Seguridad**: Acceso protegido por autenticación básica y con soporte para Fail2Ban.
  - **Soporte Multilenguaje (i18n)**: La interfaz está disponible en varios idiomas.
  - **Interfaz Moderna**: Construida con Tailwind CSS, es limpia, responsiva y fácil de usar.

-----

## 🛠️ Guía de Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu entorno local.

### 1\. Prerrequisitos

  - Python 3.10 o superior.
  - `pip` y `venv` instalados.
  - Claves de API para los modelos de IA que desees utilizar (Gemini, Mistral, DeepSeek, etc.).

### 2\. Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/ai-prompt-compare.git
cd ai-prompt-compare
```

### 3\. Crear y Activar un Entorno Virtual

Es una buena práctica utilizar un entorno virtual para aislar las dependencias del proyecto.

  - **En macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  - **En Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4\. Instalar Dependencias

Instala todas las librerías necesarias utilizando el fichero `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5\. Configurar las Claves de API (`.env`)

La aplicación carga las claves de API desde un fichero `.env`. Crea una copia del fichero de ejemplo `.env.EXAMPLE` y renómbrala a `.env`:

```bash
cp .env.EXAMPLE .env
```

Abre el fichero `.env` y añade tus claves de API. No es necesario rellenarlas todas, solo las de los modelos que vayas a activar en `models.json`.

```ini
GEMINI_API_KEY=TU_API_KEY_DE_GEMINI
MISTRAL_API_KEY=TU_API_KEY_DE_MISTRAL
GROK_API_KEY=TU_API_KEY_DE_GROQ
DEEPSEEK_API_KEY=TU_API_KEY_DE_DEEPSEEK
ANTHROPIC_API_KEY=TU_API_KEY_DE_ANTHROPIC
```

### 6\. Configurar Usuarios (`users.json`)

La autenticación se gestiona a través de un fichero `users.json`.

  - **Generar un Hash de Contraseña**: El proyecto incluye un script para generar hashes seguros para tus contraseñas. Ejecútalo con la contraseña que desees:
    ```bash
    python hash_generator.py 'tu_contraseña_segura'
    ```
  - **Crear `users.json`**:
    Crea una copia de `users.json.EXAMPLE` y renómbrala a `users.json`. Abre el fichero y edítalo. Reemplaza el nombre de usuario y el hash con los tuyos. Puedes añadir tantos usuarios como necesites.
    ```json
    {
      "tu_usuario": "scrypt:32768:8:1$...",
      "otro_usuario": "scrypt:32768:8:1$..."
    }
    ```

### 7\. Configurar los Modelos (`models.json`)

El fichero `models.json` te permite activar o desactivar los modelos de IA. Para activar un modelo, cambia su propiedad `"enabled"` a `true`. Para desactivarlo, ponla en `false`.

```json
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
```

-----

## ▶️ Ejecutar la Aplicación

Una vez completada la configuración, inicia el servidor de producción usando `waitress`:

```bash
python app.py
```

La aplicación estará disponible en `http://0.0.0.0:3556`. Cuando accedas desde tu navegador, se te pedirá un nombre de usuario y contraseña.

-----

## ⚙️ (Avanzado) Configurar como Servicio de `systemd`

Para que la aplicación se ejecute de forma continua en un servidor y se reinicie automáticamente, puedes configurarla como un servicio de `systemd` en Linux.

### 1\. Crear el Fichero de Servicio

```bash
sudo nano /etc/systemd/system/ia-prompt-compare.service
```

### 2\. Añadir la Configuración del Servicio

Pega el siguiente contenido en el fichero. **Asegúrate de reemplazar `TU_USUARIO` y las rutas** con los valores correctos de tu sistema.

```ini
[Unit]
Description=AI-Prompt-Compare Application
After=network.target

[Service]
User=TU_USUARIO
Group=www-data
WorkingDirectory=/ruta/absoluta/a/ai-prompt-compare
ExecStart=/ruta/absoluta/a/ai-prompt-compare/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

  - **`User`**: El usuario con el que se ejecutará el servicio (no se recomienda `root`).
  - **`WorkingDirectory`**: La ruta completa al directorio raíz del proyecto.
  - **`ExecStart`**: La ruta completa al ejecutable de Python dentro del entorno virtual.

### 3\. Habilitar e Iniciar el Servicio

```bash
# Recargar systemd para que lea el nuevo fichero
sudo systemctl daemon-reload

# Habilitar el servicio para que se inicie en el arranque
sudo systemctl enable ai-prompt-compare.service

# Iniciar el servicio ahora mismo
sudo systemctl start ai-prompt-compare.service
```

### 4\. Verificar el Estado del Servicio

```bash
sudo systemctl status ai-prompt-compare.service
```

Si todo ha ido bien, deberías ver un estado `active (running)`.

-----

## 🌍 Traducción (i18n)

El proyecto utiliza `Flask-Babel` para la internacionalización. Añadir un nuevo idioma es un proceso sencillo.

### 1\. Inicializar el nuevo idioma

Usa el código de idioma de 2 letras (ej: `fr` para francés, `de` para alemán).

```bash
pybabel init -i messages.pot -d translations -l fr
```

Esto creará un nuevo fichero en `translations/fr/LC_MESSAGES/messages.po`.

### 2\. Traducir los textos

Abre el nuevo fichero `.po`. Verás pares de `msgid` (texto original) y `msgstr` (traducción vacía). Rellena las cadenas `msgstr` con la traducción.

```po
#: templates/index.html:50
msgid "Modo Comparar"
msgstr "Compare Mode"  # <-- Ejemplo para inglés (en)
```

### 3\. Compilar las traducciones

Una vez guardado el fichero `.po`, compila las traducciones a un formato optimizado (`.mo`).

```bash
pybabel compile -d translations
```

### 4\. Actualizar las traducciones

Si añades más textos a la aplicación en el futuro, sigue estos pasos:

```bash
# Extrae los nuevos textos al fichero principal .pot
pybabel extract -F babel.cfg -k _ -o messages.pot .

# Actualiza el fichero .po de tu idioma con los nuevos textos
pybabel update -i messages.pot -d translations

# Traduce los nuevos msgid en el fichero .po y compila de nuevo
pybabel compile -d translations
```

-----

## 🛡️ (Avanzado) Seguridad con Fail2Ban

Para proteger la aplicación contra ataques de fuerza bruta, puedes configurar una jaula de Fail2Ban.

**Requisito previo**: Asegúrate de haber añadido la línea de logging de intentos fallidos en `app.py`.

### 1\. Crear un filtro para Fail2Ban

```bash
sudo nano /etc/fail2ban/filter.d/ia-prompt-compare.conf
```

Pega el siguiente contenido:

```ini
[Definition]
failregex = Failed login attempt for user '.*' from IP: <HOST>
ignoreregex =
```

### 2\. Crear la jaula (Jail)

```bash
sudo nano /etc/fail2ban/jail.d/ia-prompt-compare.local
```

Pega la siguiente configuración. **¡Asegúrate de cambiar `logpath` por la ruta real al log de tu aplicación\!**

```ini
[ia-prompt-compare]
enabled  = true
port     = 3556
filter   = ia-prompt-compare
logpath  = /var/log/syslog
maxretry = 5
findtime = 600
bantime  = 3600
```

  - `logpath`: Si usas `systemd`, los logs podrían ir a `/var/log/syslog` o al journal. Usa `journalctl -u ia-prompt-compare.service` para localizarlos.
  - `maxretry`: Número de intentos fallidos antes de banear.
  - `bantime`: Duración del baneo en segundos (3600 = 1 hora).

### 3\. Reiniciar Fail2Ban

Aplica los cambios reiniciando el servicio.

```bash
sudo systemctl restart fail2ban
```

Para verificar que la jaula está activa, usa `sudo fail2ban-client status ia-prompt-compare`.

-----

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](https://www.google.com/search?q=LICENSE).
