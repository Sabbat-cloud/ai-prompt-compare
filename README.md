-----

# 🚀 AI-Prompt-Compare

AI-Prompt-Compare is a powerful web application built with Flask that allows you to interact with multiple AI language models simultaneously. It is designed for developers, researchers, and AI enthusiasts who want to compare the performance of different models or create complex conversations between them.

The application features an intuitive user interface and two main operating modes to explore the capabilities of the most advanced AI models.

## ✨ Key Features

  - **Compare Mode**: Send a single prompt to all configured AI models and view their responses side-by-side.
  - **Conversation Mode**: Start a dialogue chain where one model's response becomes the prompt for the next.
  - **Advanced Settings**: Adjust parameters like `temperature` and `max tokens`.
  - **Modular Architecture**: Adding a new AI model is straightforward.
  - **Security**: Access is protected by basic authentication with Fail2Ban support.
  - **Multi-language Support (i18n)**: The interface is available in multiple languages.
  - **Modern UI**: Built with Tailwind CSS, it's clean, responsive, and user-friendly.

-----

## 🛠️ Installation and Configuration Guide

Follow these steps to get the project up and running in your local environment.

### 1\. Prerequisites

  - Python 3.10 or higher.
  - `pip` and `venv` installed.
  - API keys for the AI models you wish to use (Gemini, Mistral, DeepSeek, etc.).

### 2\. Clone the Repository

```bash
git clone https://github.com/your_username/ai-prompt-compare.git
cd ai-prompt-compare
```

### 3\. Create and Activate a Virtual Environment

It is a best practice to use a virtual environment to isolate project dependencies.

  - **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  - **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4\. Install Dependencies

Install all the required libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Configure API Keys (`.env`)

The application loads API keys from a `.env` file. Create a copy of the example file `.env.EXAMPLE` and rename it to `.env`:

```bash
cp .env.EXAMPLE .env
```

Open the `.env` file and add your API keys. You don't need to fill them all, only for the models you plan to enable in `models.json`.

```ini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
GROK_API_KEY=YOUR_GROQ_API_KEY
DEEPSEEK_API_KEY=YOUR_DEEPSEEK_API_KEY
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
```

### 6\. Configure Users (`users.json`)

Authentication is managed through a `users.json` file.

  - **Generate a Password Hash**: The project includes a script to generate secure hashes for your passwords. Run it with your desired password:
    ```bash
    python hash_generator.py 'your_secure_password'
    ```
  - **Create `users.json`**:
    Create a copy of `users.json.EXAMPLE` and rename it to `users.json`. Open the file and edit it. Replace the username and hash with your own.
    ```json
    {
      "your_user": "scrypt:32768:8:1$...",
      "another_user": "scrypt:32768:8:1$..."
    }
    ```

### 7\. Configure Models (`models.json`)

The `models.json` file allows you to enable or disable the AI models. To enable a model, set its `"enabled"` property to `true`. To disable it, set it to `false`.

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
    // ... other models
  ]
}
```

-----

## ▶️ Run the Application

Once the configuration is complete, start the production server using `waitress`:

```bash
python app.py
```

The application will be available at `http://0.0.0.0:3556`. When you access it from your browser, you will be prompted for a username and password.

-----

## ⚙️ (Advanced) Set Up as a `systemd` Service

To run the application continuously on a server and have it restart automatically, you can configure it as a `systemd` service on Linux.

### 1\. Create the Service File

```bash
sudo nano /etc/systemd/system/ai-prompt-compare.service
```

### 2\. Add the Service Configuration

Paste the following content into the file. **Make sure to replace `YOUR_USER` and the paths** with the correct values for your system.

```ini
[Unit]
Description=AI-Prompt-Compare Application
After=network.target

[Service]
User=YOUR_USER
Group=www-data
WorkingDirectory=/absolute/path/to/ai-prompt-compare
ExecStart=/absolute/path/to/ai-prompt-compare/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

  - **`User`**: The user that will run the service (running as `root` is not recommended).
  - **`WorkingDirectory`**: The full path to the project's root directory.
  - **`ExecStart`**: The full path to the Python executable inside the virtual environment.

### 3\. Enable and Start the Service

```bash
# Reload systemd to read the new file
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable ai-prompt-compare.service

# Start the service immediately
sudo systemctl start ai-prompt-compare.service
```

### 4\. Check the Service Status

```bash
sudo systemctl status ai-prompt-compare.service
```

If everything went well, you should see an `active (running)` status.

-----

## 🌍 Translation (i18n)

The project uses `Flask-Babel` for internationalization. Adding a new language is a simple process.

### 1\. Initialize the New Language

Use the 2-letter language code (e.g., `fr` for French, `de` for German).

```bash
pybabel init -i messages.pot -d translations -l fr
```

This will create a new file at `translations/fr/LC_MESSAGES/messages.po`.

### 2\. Translate the Strings

Open the new `.po` file. You will see pairs of `msgid` (original text) and `msgstr` (empty translation). Fill in the `msgstr` strings.

```po
#: templates/index.html:50
msgid "Modo Comparar"
msgstr "Compare Mode" # <-- Example for English (en)
```

### 3\. Compile the Translations

After saving the `.po` file, compile the translations into an optimized `.mo` format.

```bash
pybabel compile -d translations
```

### 4\. Update Translations

If you add more text to the application in the future, follow these steps:

```bash
# Extract new strings into the main .pot file
pybabel extract -F babel.cfg -k _ -o messages.pot .

# Update your language's .po file with the new strings
pybabel update -i messages.pot -d translations

# Translate the new msgids in the .po file and compile again
pybabel compile -d translations
```

-----

## 🛡️ (Advanced) Security with Fail2Ban

To protect the application against brute-force attacks, you can set up a Fail2Ban jail.

**Prerequisite**: Ensure you have added the failed attempt logging line in `app.py`.

### 1\. Create a Fail2Ban Filter

```bash
sudo nano /etc/fail2ban/filter.d/ia-prompt-compare.conf
```

Paste the following content:

```ini
[Definition]
failregex = Failed login attempt for user '.*' from IP: <HOST>
ignoreregex =
```

### 2\. Create the Jail

```bash
sudo nano /etc/fail2ban/jail.d/ia-prompt-compare.local
```

Paste the following configuration. **Make sure to change `logpath` to the actual path of your application's log file\!**

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

  - `logpath`: If you use `systemd`, logs might go to `/var/log/syslog` or the journal. Use `journalctl -u ia-prompt-compare.service` to check where they are stored.
  - `maxretry`: Number of failed attempts before banning.
  - `bantime`: Ban duration in seconds (3600 = 1 hour).

### 3\. Restart Fail2Ban

Apply the changes by restarting the service.

```bash
sudo systemctl restart fail2ban
```

To verify that the jail is active, you can use `sudo fail2ban-client status ia-prompt-compare`.

-----

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).
