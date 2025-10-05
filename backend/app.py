from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import google.generativeai as genai
import check
import tempfile
import base64
from elevenlabs.client import ElevenLabs
import math

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyBZIQRj8ZPbIDapJ3VbG3rYUTq7uXkI2tk")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Tour Guide API is running"})

@app.route('/api/describe-location', methods=['POST'])
def describe_location():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        
        if not lat or not lng:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        # Get description from check.py
        description = check.describe_places(lat, lng)
        
        return jsonify({
            "description": description,
            "location": {"lat": lat, "lng": lng}
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Generate audio using ElevenLabs
        api_key = os.getenv("ELEVEN_API_KEY", "sk_f97508bc90abc6598e9eab4339e1d1ba212a05e71c030533")
        client = ElevenLabs(api_key=api_key)
        
        # Convert text → audio stream
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # Convert audio stream to base64
        audio_data = b""
        for chunk in audio_stream:
            audio_data += chunk
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            "audio": audio_base64,
            "format": "mp3"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tour-guide', methods=['POST'])
def tour_guide():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        
        if not lat or not lng:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        # Generate description
        description = check.describe_places(lat, lng)
        
        # Generate audio
        api_key = os.getenv("ELEVEN_API_KEY", "sk_f97508bc90abc6598e9eab4339e1d1ba212a05e71c030533")
        client = ElevenLabs(api_key=api_key)
        
        audio_stream = client.text_to_speech.convert(
            text=description,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        audio_data = b""
        for chunk in audio_stream:
            audio_data += chunk
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            "description": description,
            "audio": audio_base64,
            "location": {"lat": lat, "lng": lng}
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
