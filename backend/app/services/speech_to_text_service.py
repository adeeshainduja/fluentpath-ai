from pathlib import Path


def transcribe_audio(
    audio_path: str,
) -> str:
    """
    Convert speech into text.

    TODO:
    Integrate Whisper API or Gemini Audio.
    """

    if not Path(audio_path).exists():
        raise FileNotFoundError("Audio file not found.")

    # Placeholder transcription
    return "This is a sample transcription."