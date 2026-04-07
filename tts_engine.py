import edge_tts
import asyncio

async def get_voices():
    """Fetch available voices from edge-tts."""
    voices = await edge_tts.VoicesManager.create()
    return voices.find(Locale="en-US") # Default to en-US for now, can be extended

def format_rate(rate_val: int) -> str:
    """
    Format rate integer to edge-tts string format.
    0 -> +0%
    10 -> +10%
    -10 -> -10%
    """
    if rate_val >= 0:
        return f"+{rate_val}%"
    return f"{rate_val}%"

def format_pitch(pitch_val: int) -> str:
    """
    Format pitch integer to edge-tts string format.
    0 -> +0Hz
    10 -> +10Hz
    -10 -> -10Hz
    """
    if pitch_val >= 0:
        return f"+{pitch_val}Hz"
    return f"{pitch_val}Hz"

async def generate_tts(text: str, voice: str, rate: int, pitch: int, output_file: str):
    """Generate TTS audio and save to file."""
    rate_str = format_rate(rate)
    pitch_str = format_pitch(pitch)
    
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    await communicate.save(output_file)

if __name__ == "__main__":
    # Small test
    async def main():
        v = await get_voices()
        print(f"Found {len(v)} English voices.")
        # await generate_tts("Hello world", v[0]['Name'], 0, 0, "test.mp3")
    
    asyncio.run(main())
