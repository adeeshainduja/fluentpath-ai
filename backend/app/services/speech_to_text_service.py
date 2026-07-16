from pathlib import Path


def transcribe_audio(
    audio_path: str,
) -> str:
    """Validate an audio file before external transcription."""

    if not Path(audio_path).exists():
        raise FileNotFoundError("Audio file not found.")

    raise NotImplementedError(
        "Server-side transcription is not configured. "
        "Use the browser speech recognition flow."
    )
