import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import soundfile as sf

# 🔁 Session state to store audio
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = []

st.title("🎤 Record Audio Without audio_frame_callback")

# 🟢 Start WebRTC (no audio_frame_callback)
webrtc_ctx = webrtc_streamer(
    key="audio-recorder",
    mode=WebRtcMode.SENDONLY,
    media_stream_constraints={"audio": True, "video": False},
    audio_receiver_size=32  # increase buffer to prevent overflow
)

# 🔄 Continuously pull frames if connection is active
if webrtc_ctx.state.playing:
    audio_receiver = webrtc_ctx.audio_receiver
    if audio_receiver:
        try:
            frames = audio_receiver.get_frames(timeout=5)
            for frame in frames:
                audio = frame.to_ndarray()
                st.session_state.audio_frames.append(audio.copy())
                st.write(f"📥 Frame received: shape = {audio.shape}")
        except Exception as e:
            st.warning(f"⚠️ Error while receiving audio frames: {e}")

# 🛑 Save & Download
if st.button("Stop & Save Audio"):
    if st.session_state.audio_frames:
        audio_data = np.concatenate(st.session_state.audio_frames, axis=1).T  # (samples, 1)
        audio_data = audio_data.astype(np.float32)
        sf.write("output.wav", audio_data, samplerate=48000)
        st.success("✅ Audio saved as output.wav")
        st.audio("output.wav")
    else:
        st.warning("⚠️ No audio was recorded.")
