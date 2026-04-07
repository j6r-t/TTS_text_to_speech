# Edge-TTS Synthesizer

A premium Text-to-Speech application powered by Microsoft Edge's Neural Voices.

## Features
- **Neural Voices:** Access high-quality, lifelike voices from Microsoft Edge.
- **Custom Controls:** Fine-tune the speech rate and pitch using a normalized scale.
- **Real-time Preview:** Listen to the generated audio directly in the browser.
- **MP3 Export:** Save your synthesized audio to disk.

## Installation
1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using Streamlit:
```bash
streamlit run app.py
```

## Parameter Logic
- **Rate:** 0 is default. Positive values increase speed (+%), negative values decrease speed (-%).
- **Pitch:** 0 is default. Positive values increase pitch (+Hz), negative values decrease pitch (-Hz).