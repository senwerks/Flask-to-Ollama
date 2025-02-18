from flask import Flask, render_template, request, Response, jsonify
import requests
import json

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434"

@app.route('/')
def index():
    models = get_available_models()
    ollama_status = check_ollama_status()
    return render_template('index.html', models=models, ollama_status=ollama_status)

@app.route('/api', methods=['GET'])
def api():
    model = request.args.get('model')
    prompt = request.args.get('prompt')
    
    if not model or not prompt:
        return jsonify({"error": "Model and prompt are required"}), 400
    
    def generate():
        payload = {"model": model, "prompt": prompt, "stream": True}
        try:
            r = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload, stream=True)
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        text = data.get("response", "")
                    except json.JSONDecodeError:
                        text = line
                    # Send the text chunk as an SSE message.
                    formatted_text = text.replace('\n', '\ndata: ')
                    yield f"data: {formatted_text}\n\n"

                    # If the JSON indicates the stream is complete, send an "end" event with total time.
                    if isinstance(data, dict) and data.get("done", False):
                        total_duration = data.get("total_duration")
                        if total_duration is not None:
                            # Convert nanoseconds to seconds.
                            total_time_s = float(total_duration) / 1e9
                            yield f"event: end\ndata: {total_time_s:.3f}\n\n"
                        else:
                            yield "event: end\ndata: \n\n"
                        break
        except requests.RequestException as e:
            yield f"data: Error communicating with Ollama API: {e}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")


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
            print_colour = '\033[94m'  # Blue by default.
    print_end = '\033[0m'
    print(print_colour + printing + print_end)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
