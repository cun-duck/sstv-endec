import streamlit as st
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from pysstv.color import MartinM1
from PIL import Image
from pydub import AudioSegment
import io

st.title("SSTV Encoder & Decoder")

# Section 1: SSTV Decoder (Suara ke Gambar)
st.header("SSTV Decoder (Suara ke Gambar)")

# Pilihan input untuk decoder: upload file atau rekam dari mikrofon
input_option = st.radio("Pilih metode input suara:", ("Unggah File Audio", "Rekam dari Mikrofon"))

if input_option == "Unggah File Audio":
    # Upload file audio untuk didekode
    uploaded_file = st.file_uploader("Upload SSTV Audio File (WAV)", type=["wav"])
    if uploaded_file is not None:
        # Membaca file audio
        wav_data = io.BytesIO(uploaded_file.read())
        wav_file = wav.open(wav_data, 'rb')
        
        # Dekode sinyal audio ke gambar
        sstv = MartinM1(wav_file)
        sstv_image = sstv.decode()
        
        # Tampilkan gambar yang didekode
        st.image(sstv_image, caption="Decoded SSTV Image")

elif input_option == "Rekam dari Mikrofon":
    duration = st.slider("Durasi Rekaman (detik)", 1, 10, 5)  # Durasi rekaman
    fs = 44100  # Frekuensi sampling

    if st.button("Mulai Rekam"):
        # Rekam audio
        st.write("Merekam...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Tunggu hingga rekaman selesai

        # Simpan rekaman sebagai file WAV dalam memori
        wav_data = io.BytesIO()
        wav.write(wav_data, fs, audio_data)
        wav_data.seek(0)

        # Dekode sinyal audio ke gambar
        wav_file = wav.open(wav_data, 'rb')
        sstv = MartinM1(wav_file)
        sstv_image = sstv.decode()

        # Tampilkan gambar yang didekode
        st.image(sstv_image, caption="Decoded SSTV Image")

# Section 2: SSTV Encoder (Gambar ke Suara)
st.header("SSTV Encoder (Gambar ke Suara)")

# Upload gambar untuk di-encode menjadi suara SSTV
uploaded_image = st.file_uploader("Upload Gambar (JPG/PNG)", type=["jpg", "png"])

if uploaded_image is not None:
    # Baca dan tampilkan gambar
    img = Image.open(uploaded_image)
    st.image(img, caption="Gambar yang Diunggah", use_column_width=True)

    # Encode gambar menjadi audio SSTV dalam format WAV
    sstv = MartinM1(img, 44100)
    wav_data = io.BytesIO()
    sstv.write_wav(wav_data)
    wav_data.seek(0)

    # Konversi dari WAV ke MP3 menggunakan pydub
    audio_segment = AudioSegment.from_wav(wav_data)
    mp3_data = io.BytesIO()
    audio_segment.export(mp3_data, format="mp3")
    mp3_data.seek(0)

    # Tampilkan player audio dan tombol unduh
    st.audio(mp3_data, format="audio/mp3")
    st.download_button("Download Suara SSTV", data=mp3_data, file_name="sstv_audio.mp3", mime="audio/mpeg")
