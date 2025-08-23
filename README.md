README.md (English)
🚀 AI-Prompt-Compare
AI-Prompt-Compare is a powerful web application built with Flask that allows you to interact with multiple AI language models simultaneously. It is designed for developers, researchers, and AI enthusiasts who want to compare the performance of different models or create complex conversations between them.

The application features an intuitive user interface and two main operating modes to explore the capabilities of the most advanced AI models.

✨ Key Features
Compare Mode: Send a single prompt to all configured AI models and view their responses side-by-side. This is ideal for evaluating the quality, style, and accuracy of each model.

Conversation Mode: Start a dialogue chain where one model's response becomes the prompt for the next. This allows for creating debates, brainstorming sessions, or seeing how AIs collaborate or diverge on a topic.

Advanced Settings: Adjust parameters like temperature (to control creativity) and max tokens (to limit response length) to fine-tune the results.

Modular Architecture: Adding a new AI model is straightforward. You just need to create a new connector class in the ai_models directory and add its configuration to models.json.

Security: Access to the application is protected by basic authentication, ensuring that only authorized users can use it.

Modern UI: The interface is built with Tailwind CSS, providing a clean, responsive, and user-friendly experience.

🛠️ Installation and Configuration Guide
Follow these steps to get the project up and running in your local environment.

1. Prerequisites
Python 3.10 or higher.

pip and venv installed.

API keys for the AI models you wish to use (Gemini, Mistral, DeepSeek, etc.).

2. Clone the Repository
Bash

git clone https://github.com/your_username/ai-prompt-compare.git
cd ai-prompt-compare
3. Create and Activate a Virtual Environment
It is a best practice to use a virtual environment to isolate project dependencies.

On macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
On Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
4. Install Dependencies
Install all the required libraries using the requirements.txt file.

Bash

pip install -r requirements.txt
5. Configure API Keys (.env)
The application loads API keys from a .env file.

Create a copy of the example file .env.EXAMPLE and rename it to .env:

Bash

cp .env.EXAMPLE .env
Open the .env file and add your API keys. You don't need to fill them all, only for the models you plan to enable in models.json.

Ini, TOML

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
GROK_API_KEY=YOUR_GROQ_API_KEY
DEEPSEEK_API_KEY=YOUR_DEEPSEEK_API_KEY
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
6. Configure Users (users.json)
Authentication is managed through a users.json file.

Generate a Password Hash: The project includes a script to generate secure hashes for your passwords. Run it with your desired password:

Bash

python hash_generator.py 'your_secure_password'
Create users.json:

Create a copy of users.json.EXAMPLE and rename it to users.json.

Open the file and edit it. Replace the username and hash with your own. You can add as many users as you need.

JSON

{
  "your_user": "scrypt:32768:8:1$...",
  "another_user": "scrypt:32768:8:1$..."
}
7. Configure Models (models.json)
The models.json file allows you to enable or disable the AI models that will be displayed in the interface.

To enable a model, set its "enabled" property to true.

To disable a model, set it to false.

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
    // ... other models
  ]
}
▶️ Run the Application
Once the configuration is complete, start the production server using waitress:

Bash

python app.py
The application will be available at http://0.0.0.0:3556. When you access it from your browser, you will be prompted for a username and password.

⚙️ (Advanced) Set Up as a System Service (Linux with systemd)
To run the application continuously on a server and have it restart automatically, you can configure it as a systemd service.

1. Create the Service File
Create a new service file for the application:

Bash

sudo nano /etc/systemd/system/ai-prompt-compare.service
2. Add the Service Configuration
Paste the following content into the file. Make sure to replace YOUR_USER and the paths in WorkingDirectory and ExecStart with the correct values for your system.

Ini, TOML

[Unit]
Description=AI Prompt Compare Application
After=network.target

[Service]
User=YOUR_USER
Group=www-data # Or your user's group
WorkingDirectory=/absolute/path/to/ai-prompt-compare
ExecStart=/absolute/path/to/ai-prompt-compare/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
User: The user that will run the service (running as root is not recommended).

WorkingDirectory: The full path to the project's root directory.

ExecStart: The full path to the Python executable inside the virtual environment, followed by app.py.

3. Enable and Start the Service
Once you have saved the file, reload the systemd daemon, enable the service to start on boot, and then start it.

Bash

# Reload systemd to read the new file
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable ai-prompt-compare.service

# Start the service immediately
sudo systemctl start ai-prompt-compare.service
4. Check the Service Status
You can check if the service is running correctly with the following command:

Bash

sudo systemctl status ia-prompt-compare.service
If everything went well, you should see an active (running) status.

📄 License
This project is licensed under the MIT License.
