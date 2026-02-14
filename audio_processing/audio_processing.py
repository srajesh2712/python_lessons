import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

FORMAT = pyaudio.paInt16  # 16-bit resolution (2 bytes per sample)
CHANNELS = 1              # Mono audio
RATE = 100000#44100              # 44.1kHz sampling rate
CHUNK = 1024              # Number of frames per buffer
WAVE_OUTPUT_FILENAME = "recorded_in_python.wav"
audio = pyaudio.PyAudio()
RECORD_SECONDS = 5
# Start the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

def dispaly_output(raw_data):
    # np.frombuffer is a super-fast way to turn bytes into numbers
    audio_as_integers = np.frombuffer(raw_data, dtype=np.int16)

    # Create a time axis (so the bottom of the graph shows seconds)
    time_axis = np.linspace(0, RECORD_SECONDS, num=len(audio_as_integers))

    # --- PLOTTING ---
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio_as_integers, color='blue', linewidth=0.5)

    plt.title("The 'Shape' of Your Voice (PCM Data)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (Microphone Diaphragm Position)")
    plt.ylim(-32768, 32767)  # The limits of 16-bit audio
    plt.grid(True)
    plt.show()
print("Listening... Press Ctrl+C to stop.")
frames = []
try:


    # Collect the raw bytes in a list
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)


    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
except KeyboardInterrupt:
    print("Shutting down.")
stream.stop_stream()
stream.close()

raw_pcm_data = b''.join(frames)
dispaly_output(raw_pcm_data)
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT)) # This will be 2 bytes (16-bit)
    wf.setframerate(RATE)
    wf.writeframes(raw_pcm_data)

print(f"File saved as {WAVE_OUTPUT_FILENAME}")