from flask import Flask, request, jsonify
import numpy as np
import sounddevice as sd
from TTS.api import TTS
import werkzeug.exceptions
import logging
from threading import Thread
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Singleton for TTS Model
class TTSManager:
    _instance = None
    _tts_model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize_tts(self) -> TTS:
        if self._tts_model is None:
            logger.info("Initializing TTS...")
            self._tts_model = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=False, gpu=False)
            logger.info("TTS model initialized and cached.")
        else:
            logger.info("Using cached TTS model.")
        return self._tts_model

tts_manager = TTSManager.get_instance()

def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/synthesize', methods=['POST'])
    def synthesize():
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                raise werkzeug.exceptions.BadRequest("No text provided for synthesis")

            text = data['text']
            speed = data.get('speed', 4.0)

            if not isinstance(text, str) or len(text.strip()) == 0:
                raise werkzeug.exceptions.BadRequest("Invalid text provided for synthesis")

            logger.info(f"Received text: {text} with speed: {speed}")

            tts = tts_manager.initialize_tts()
            logger.info("Starting TTS synthesis...")

            try:
                wav = tts.tts(text, speed=speed)
                logger.info("TTS synthesis complete.")
            except Exception as e:
                logger.error(f"TTS synthesis failed: {str(e)}")
                return jsonify({"error": f"TTS synthesis failed: {str(e)}"}), 500

            wav_np = np.array(wav, dtype=np.float32)
            logger.info("Converted to NumPy array.")

            # Play audio asynchronously
            thread = Thread(target=play_audio_async, args=(wav_np,))
            thread.start()

            return jsonify({"status": "success"})

        except werkzeug.exceptions.BadRequest as e:
            logger.error(f"BadRequest: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"TTS synthesis failed: {str(e)}")
            return jsonify({"error": f"TTS synthesis failed: {str(e)}"}), 500

    @app.route('/stop', methods=['POST'])
    def stop():
        logger.info("Stopping audio...")
        try:
            sd.stop()
        except Exception as e:
            logger.error(f"Failed to stop audio: {str(e)}")
            return jsonify({"error": f"Failed to stop audio: {str(e)}"}), 500
        return jsonify({"status": "stopped"})

    @app.route('/status', methods=['GET'])
    def status():
        try:
            is_playing = sd.get_stream().active if sd.get_stream() else False
            logger.info(f"Audio status: {'playing' if is_playing else 'stopped'}")
            return jsonify({"status": "playing" if is_playing else "stopped"}), 200
        except RuntimeError:
            return jsonify({"status": "stopped"}), 200
        except Exception as e:
            logger.error(f"Failed to get audio status: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy"}), 200

    return app

def play_audio_async(wav_np):
    try:
        sd.play(wav_np, samplerate=22050)
        sd.wait()
    except Exception as e:
        logger.error(f"Audio playback failed: {str(e)}")

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
