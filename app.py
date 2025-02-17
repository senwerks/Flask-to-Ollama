from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434"
# Abundance of colourful (and redundant) print statements while I'm testing it all.

def prettyprint(colour, printing):
    match colour:
        case "magenta":
            print_colour = '\033[95m'
        case "blue":
            print_colour = '\033[94m'
        case "cyan":
            print_colour = '\033[96m'
        case "green":
            print_colour = '\033[92m'
        case "yellow":
            print_colour = '\033[93m'
        case "red":
            print_colour = '\033[91m'
        case "bold":
            print_colour = '\033[1m'
        case "underline":
            print_colour = '\033[4m'
        case _:
            print_colour = '\033[94m' # Blue by default.
    print_end = '\033[0m'
    print(print_colour + printing + print_end)

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
    prettyprint("blue", "Sending prompt to Ollama API and waiting for a response...")
    response = send_prompt_to_ollama(model, prompt)
    prettyprint("green", "Got response from Ollama:")
    print(response)
    return jsonify(response)

def get_available_models():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        models = [model['name'] for model in response.json().get('models', [])]
        return models
    except requests.RequestException as e:
        prettyprint("red", "Error fetching models:")
        print(e)
        return []

def send_prompt_to_ollama(model, prompt):
    try:
        payload = {"model": model, "prompt": prompt, "stream": False}
        response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        prettyprint("red", "Error communicating with Ollama API:")
        print(e)
        return {"error": "Failed to communicate with Ollama API"}

def check_ollama_status():
    try:
        response = requests.get(OLLAMA_API_URL)
        if response.status_code == 200 and "Ollama is running" in response.text:
            prettyprint("green", "Ollama server is Online.")
            return "Online"
    except requests.RequestException:
        pass

    prettyprint("red", "Ollama server is Offline!")
    return "Offline!"

if __name__ == '__main__':
    app.run(debug=True)