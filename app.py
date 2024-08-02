import logging
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, Response
import os
from agent.utils import create_tool_node_with_fallback, _print_event


load_dotenv()

from agent.main import *

app = Flask(__name__, static_folder="./static", static_url_path="/static")

# def synthesize_audio(text, model):
#     try:
#         deepgram = DeepgramClient(os.environ.get("DEEPGRAM_API_KEY"))
#         options = SpeakOptions(model=model)
#         audio_folder = os.path.join(app.static_folder, 'audio')
#         if not os.path.exists(audio_folder):
#             os.makedirs(audio_folder)
#         filename = os.path.join(app.static_folder, audio_folder, "output.mp3")
#         deepgram.speak.v("1").save(filename, {"text":text}, options)
#         return filename
#     except Exception as e:
#         raise ValueError(f"Speech synthesis failed: {str(e)}")

_printed = set()


def synthesize_audio(text, model):
    try:
        deepgram = DeepgramClient(os.environ.get("DEEPGRAM_API_KEY"))
        options = SpeakOptions(model=model)
        dg_stream = deepgram.speak.v("1").stream({"text":text}, options)        
        return dg_stream

    except Exception as e:
        raise ValueError(f"Speech synthesis failed: {str(e)}")
    

@app.route('/')
def index():
    return render_template('index.html')

# @app.route("/api", methods=["POST"])
# def synthesize_speech():
#     try:
#         data = request.get_json()
#         text = data.get('text')
#         model = data.get('model')

#         if not text:
#             raise ValueError("Text is required in the request")

#         audio_file = synthesize_audio(text, model)
#         audio_url = f"{request.url_root}static/audio/{os.path.basename(audio_file)}"

#         return jsonify({"success": True, "audioUrl": audio_url})

#     except ValueError as ve:
#         return jsonify({"success": False, "error": str(ve)})

#     except Exception as e:
#         return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route("/api", methods=["POST"])
def synthesize_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        model = data.get('model')

        if not text:
            raise ValueError("Text is required in the request")

        response = synthesize_audio(text, model)

        def generate_audio():
            # Yield the audio data incrementally
            chunk_size = 1024
            while True:
                chunk = response.stream.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        # Return a Response object with the generator function
        return Response(generate_audio(), mimetype='audio/wav')

    except Exception as e:
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route("/talk", methods=["POST"])
def respond_to_speech():
    try:
        data = request.get_json()
        text = data.get('user_speech')

        print(text)

        print("response from ai")

        question = text

        events = part_1_graph.invoke(
            {"messages": ("user", question)}, config, stream_mode="values"
        )

        # print(events.get("messages")[-1].content)

        output_text = events.get("messages")[-1].content

        # for event in events:
        #     # output_text = _print_event(event, _printed)
        #     print(event)
        #     output_text = event

        print("the output text is", output_text)

        return jsonify({"success": True, "response": output_text})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    # print(lookup_policy("what is the policy on cancelling a booking"))
    app.run(debug=True, port=8080)
