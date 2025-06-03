import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import soundfile as sf
import tempfile
import os

st.title("🎤 Record and Save Audio")

# Temporary buffer for storing audio frames
if "audio_frames" not in st.session_state:
    st.session_state["audio_frames"] = []

# Audio callback to collect frames
def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    audio = frame.to_ndarray()
    st.session_state["audio_frames"].append(audio.copy())
    return frame

# Start WebRTC audio stream
webrtc_ctx = webrtc_streamer(
    key="audio-recorder",
    mode=WebRtcMode.SENDONLY,
    in_audio=True,
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False}
    ),
    audio_frame_callback=audio_frame_callback,
)

# Button to save audio
if st.button("📝 Save Recording"):
    if st.session_state["audio_frames"]:
        audio_data = np.concatenate(st.session_state["audio_frames"])
        sample_rate = 48000  # Default WebRTC sample rate
        # Save to WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, audio_data, samplerate=sample_rate)
            st.success("✅ Audio saved successfully!")
            st.audio(tmpfile.name)
            st.session_state["saved_audio_path"] = tmpfile.name
    else:
        st.warning("⚠️ No audio recorded yet!")

# Optional: Transcription (Whisper)
if "saved_audio_path" in st.session_state:
    if st.button("🧠 Transcribe with Whisper"):
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(st.session_state["saved_audio_path"])
        st.markdown("### 📄 Transcription:")
        st.write(result["text"])
