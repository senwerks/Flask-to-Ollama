from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434"

@app.route('/')
def index():
    # Get available models from Ollama
    models = get_available_models()
    ollama_status = check_ollama_status()
    return render_template('index.html', models=models, ollama_status=ollama_status)

@app.route('/api', methods=['POST'])
def api():
    model = request.form.get('model')
    prompt = request.form.get('prompt')
    
    if not model or not prompt:
        return jsonify({"error": "Model and prompt are required"}), 400
    
    # Format and send request to Ollama
    response = send_prompt_to_ollama(model, prompt)
    return jsonify(response)

def get_available_models():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        models = [model['name'] for model in response.json().get('models', [])]
        return models
    except requests.RequestException as e:
        print("Error fetching models:", e)
        return []

def send_prompt_to_ollama(model, prompt):
    try:
        payload = {"model": model, "prompt": prompt, "stream": False}
        response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error communicating with Ollama API:", e)
        return {"error": "Failed to communicate with Ollama API"}

def check_ollama_status():
    try:
        response = requests.get(OLLAMA_API_URL)
        if response.status_code == 200 and "Ollama is running" in response.text:
            return "Ollama is currently online"
    except requests.RequestException:
        pass
    return "Offline"

if __name__ == '__main__':
    app.run(debug=True)