# Utility functions for audio processing
import io 
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    from pydub import AudioSegment 
except ImportError:
    AudioSegment = None 

def transcribe_audio_file(audio_file):
    """
    Transcribe audio file to text using Google Speech Recognition
    
    Args:
        audio_file: Flask file object containing audio data
        
    Returns:
        dict: {"transcript": str} on success, {"error": str} on failure
    """
    if not sr or not AudioSegment:
        return {"error": "Speech Recognition module is not installed"}

    try:
        # Convert audio to WAV format
        content_type = getattr(audio_file, 'content_type', 'audio/webm') or 'audio/webm'
        fmt = content_type.split(';')[0].split('/')[-1].strip()
        if not fmt or fmt not in ['webm', 'wav', 'mp3', 'ogg', 'm4a', 'flac']:
            fmt = 'webm'
        audio = AudioSegment.from_file(audio_file, format=fmt)
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # Recognize speech
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)
        
        # Transcribe with Hindi language support
        text = r.recognize_google(audio_data, language="hi-IN")
        
        print(f"🎤 Transcribed Text: {text}")
        return {"transcript": text}

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return {"error": "Could not understand audio"}
    except sr.RequestError as e:
        print(f"Could not request results from Google service; {e}")
        return {"error": "API unavailable"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An internal error occurred"}