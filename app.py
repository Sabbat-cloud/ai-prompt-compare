# app.py
import os
import json
import logging
import threading
import time
from datetime import datetime
from collections import defaultdict
from importlib import import_module
from functools import lru_cache, wraps

from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import concurrent.futures
from werkzeug.security import check_password_hash
from waitress import serve

# --- Configuración Inicial ---
load_dotenv()
app = Flask(__name__)

# Configurar Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# --- LÓGICA DE AUTENTICACIÓN ---

def load_users():
    """Carga los usuarios desde users.json."""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Error: 'users.json' no encontrado o con formato incorrecto. La autenticación no funcionará.")
        return {}

USERS = load_users()

def check_auth(username, password):
    """Verifica si un usuario y contraseña son válidos."""
    if username in USERS and check_password_hash(USERS.get(username), password):
        return True
    return False

def authenticate():
    """Respuesta para cuando se requiere autenticación."""
    return Response(
        'Acceso no autorizado.\n'
        'Debes proporcionar credenciales válidas.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def login_required(f):
    """Decorador para proteger rutas."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- Sistema de Métricas ---
class Metrics:
    def __init__(self):
        self.response_times = defaultdict(list)
        self.error_count = defaultdict(int)
        self.total_requests = 0
    
    def record_request(self):
        self.total_requests += 1

    def record_response_time(self, model_name, response_time):
        self.response_times[model_name].append(response_time)
    
    def record_error(self, model_name):
        self.error_count[model_name] += 1

metrics = Metrics()

# --- Funciones de Ayuda ---

def save_results(prompt, results, mode):
    """Guarda el prompt y los resultados en un fichero JSON."""
    try:
        base_dir = 'results'
        os.makedirs(base_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(base_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_prompt = "".join([c if c.isalnum() else "_" for c in prompt[:30]])
        filename = f"{timestamp}_{mode}_{safe_prompt}.json"
        filepath = os.path.join(date_dir, filename)
        data_to_save = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'initial_prompt': prompt,
            'results': results
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        logger.info(f"Resultados guardados en: {filepath}")
    except Exception as e:
        logger.error(f"Error al guardar los resultados: {e}")

def load_ai_models_config():
    """Carga la configuración de los modelos desde models.json."""
    try:
        with open('models.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error al cargar 'models.json': {e}")
        return {}

@lru_cache(maxsize=32)
def get_ai_instance(module_path, class_name, model_config_tuple):
    """Crea y devuelve una instancia de un modelo de IA cacheada."""
    model_config = dict(model_config_tuple)
    try:
        ai_module = import_module(module_path)
        AIClass = getattr(ai_module, class_name)
        return AIClass(model_config)
    except (ImportError, AttributeError) as e:
        logger.error(f"No se pudo cargar la clase {class_name} desde {module_path}: {e}")
        return None

def call_ai_model_with_timeout(model_config, prompt, options, timeout=60):
    """Llama a un modelo de IA con timeout y registra métricas."""
    start_time = time.time()
    model_name = model_config['name']
    try:
        config_tuple = tuple(sorted(model_config.items()))
        ai_instance = get_ai_instance(model_config['module_path'], model_config['class_name'], config_tuple)
        
        if ai_instance is None:
            raise ValueError(f"No se pudo crear la instancia del modelo {model_name}.")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ai_instance.query, prompt, options)
            response = future.result(timeout=timeout)
            
        metrics.record_response_time(model_name, time.time() - start_time)
        return response

    except Exception as e:
        metrics.record_error(model_name)
        error_message = f"Error en {model_name}: {e}"
        if isinstance(e, concurrent.futures.TimeoutError):
            error_message = f"Timeout al consultar {model_name} después de {timeout} segundos."
        
        logger.warning(error_message)
        return error_message

# --- Rutas de la Aplicación ---

@app.route('/')
@login_required
def index():
    """Renderiza la página principal."""
    models_config = load_ai_models_config()
    model_names = [model['name'] for model in models_config.get('models', []) if model.get('enabled', False)]
    return render_template('index.html', model_names=model_names)

@app.route('/status')
def status():
    """Endpoint para ver el estado del sistema y métricas (público)."""
    active_models = [model['name'] for model in load_ai_models_config().get('models', []) if model.get('enabled', False)]
    
    avg_response_times = {
        model: sum(times) / len(times) if times else 0
        for model, times in metrics.response_times.items()
    }

    status_info = {
        'total_requests': metrics.total_requests,
        'active_models': active_models,
        'average_response_times_sec': {k: round(v, 2) for k, v in avg_response_times.items()},
        'error_counts': dict(metrics.error_count),
    }
    return jsonify(status_info)


@app.route('/compare', methods=['POST'])
@limiter.limit("10 per minute")
@login_required
def compare():
    """Endpoint API para el modo Comparar."""
    metrics.record_request()
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    options = data.get('options', {})
    if not prompt:
        return jsonify({'error': 'El prompt es inválido.'}), 400
    
    models_config = [model for model in load_ai_models_config().get('models', []) if model.get('enabled', False)]
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models_config)) as executor:
        future_to_model = {executor.submit(call_ai_model_with_timeout, config, prompt, options): config for config in models_config}
        
        for future in concurrent.futures.as_completed(future_to_model):
            model_config = future_to_model[future]
            try:
                results[model_config['name']] = future.result()
            except Exception as e:
                error_message = f"Error al obtener resultado de {model_config['name']}: {e}"
                logger.error(error_message)
                results[model_config['name']] = error_message
    
    save_results(prompt, results, 'compare')
            
    return jsonify(results)

@app.route('/conversation', methods=['POST'])
@limiter.limit("5 per minute")
@login_required
def conversation():
    """Endpoint API para el modo Conversación."""
    metrics.record_request()
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    options = data.get('options', {})
    if not prompt:
        return jsonify({'error': 'El prompt es inválido.'}), 400

    models_config = [model for model in load_ai_models_config().get('models', []) if model.get('enabled', False)]
    
    if len(models_config) > 1:
        models_config = [m for m in models_config if m.get('name') != 'Mock AI (Pruebas)']
        
    conversation_chain = []
    current_prompt = prompt

    for model_config in models_config:
        response_text = call_ai_model_with_timeout(model_config, current_prompt, options)
        
        step = {
            'model_name': model_config['name'],
            'prompt': current_prompt,
            'response': response_text
        }
        conversation_chain.append(step)
        
        if "Error" in response_text or "Timeout" in response_text:
            logger.warning(f"Deteniendo la conversación debido a un error en {model_config['name']}.")
            break
            
        current_prompt = response_text
    
    save_results(prompt, conversation_chain, 'conversation')
            
    return jsonify(conversation_chain)

# --- Punto de Entrada ---
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 3556
    logger.info(f"Iniciando servidor de producción con Waitress en http://{host}:{port}")
    serve(app, host=host, port=port)
