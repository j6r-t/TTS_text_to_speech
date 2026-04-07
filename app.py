import streamlit as st
import asyncio
import os
import tempfile
from tts_engine import get_voices, generate_tts

# Page configuration
st.set_page_config(
    page_title="Edge-TTS Synthesizer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    @import url('https://unpkg.com/@phosphor-icons/web@2.1.1/src/duotone/style.css');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        font-size: 1.1rem !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    .sidebar .sidebar-content {
        background-color: #0f172a;
    }

    h1, h2, h3 {
        color: #3b82f6 !important;
        font-weight: 600 !important;
    }

    .status-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #1e293b;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    
    /* Center the title */
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
    }

    .ph-duotone {
        vertical-align: middle;
        margin-right: 8px;
        font-size: 1.4em;
    }
    </style>
    """, unsafe_allow_html=True)

def get_voices_sync():
    """Wrapper to run get_voices synchronously."""
    return asyncio.run(get_voices())

def generate_tts_sync(text: str, voice: str, rate: int, pitch: int, output_file: str):
    """Wrapper to run generate_tts synchronously."""
    return asyncio.run(generate_tts(text, voice, rate, pitch, output_file))

def main():
    st.markdown('<div class="title-container"><h1><i class="ph-duotone ph-microphone-stage"></i> Edge-TTS Synthesizer</h1><p style="color: #94a3b8;">Convert text to lifelike speech using Microsoft Edge Neural Voices</p></div>', unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown('<h3><i class="ph-duotone ph-sliders-horizontal"></i> Settings</h3>', unsafe_allow_html=True)
        
        # Voice selection
        try:
            # Cache the voices to avoid repeated API calls
            @st.cache_resource
            def cached_voices():
                return get_voices_sync()
            
            voices = cached_voices()
            voice_options = {f"{v['FriendlyName']} ({v['Gender']})": v['Name'] for v in voices}
            selected_voice_label = st.selectbox("Select Voice", options=list(voice_options.keys()))
            selected_voice = voice_options[selected_voice_label]
        except Exception as e:
            st.error(f"Error fetching voices: {e}")
            selected_voice = "en-US-AriaNeural"

        st.divider()
        
        st.markdown('<h4><i class="ph-duotone ph-equalizer"></i> Audio Controls</h4>', unsafe_allow_html=True)
        rate = st.slider("Speech Rate", min_value=-50, max_value=100, value=0, help="Positive increases, negative decreases.")
        pitch = st.slider("Pitch", min_value=-50, max_value=50, value=0, help="Positive increases, negative decreases.")
        
        st.info("💡 0 is the baseline setting.")

    # Main UI
    col1, col2 = st.columns([2, 1])

    with col1:
        text_input = st.text_area("Enter text here...", height=300, placeholder="Type or paste the text you want to synthesize...")
    
    with col2:
        st.markdown('<h3><i class="ph-duotone ph-export"></i> Export Options</h3>', unsafe_allow_html=True)
        filename = st.text_input("Filename", value="synthesized_audio.mp3")
        
        generate_btn = st.button("Generate & Play") # Removing emoji from button text for consistency or using icon class if possible
        
        if generate_btn:
            if not text_input.strip():
                st.warning("Please enter some text first!")
            else:
                with st.spinner("Synthesizing audio..."):
                    try:
                        # Use a temporary file for the synthesis
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                            tmp_path = tmp_file.name
                        
                        generate_tts_sync(text_input, selected_voice, rate, pitch, tmp_path)
                        
                        st.success("✅ Synthesis complete!")
                        
                        # Play audio
                        with open(tmp_path, "rb") as f:
                            audio_bytes = f.read()
                        
                        st.audio(audio_bytes, format="audio/mp3")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download MP3",
                            data=audio_bytes,
                            file_name=filename if filename.endswith(".mp3") else f"{filename}.mp3",
                            mime="audio/mp3",
                        )
                        
                        # Cleanup the temporary file
                        os.unlink(tmp_path)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")

    st.divider()
    st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.8rem;">Powered by Edge-TTS & Streamlit</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
