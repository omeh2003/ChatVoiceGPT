import pyaudio
import wave
import datetime
import keyboard

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

t_temperature = 0.7
t_frequency_penalty = 0
t_presence_penalty = 0
t_top_p = 0.5


def record_audio(file_name):
    frames = []
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Press space to start recording...")
    keyboard.wait('space')  # ждем нажатия клавиши
    print("Recording started...")
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if not keyboard.is_pressed('space'):  # запись закончится при повторном нажатии клавиши
            break
    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Saved to", file_name)


def generate_response(prompt):
    temperature = t_temperature
    frequency_penalty = t_frequency_penalty
    presence_penalty = t_presence_penalty
    top_p = t_top_p
    if prompt is None:
        return None
    if prompt == "":
        return None
    if prompt.__len__() >= 2000:
        prompt = f"{prompt}"[:1999]
    try:
        completions = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=3500,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
    except openai.error.ServiceUnavailableError as e:
        return str(e.error["message"])
    except openai.error.RateLimitError as e:
        return str(e.error["message"])
    except openai.error.InvalidRequestError as e:
        return str(e.error["message"])
    except openai.error.ServerError as e:
        return str(e.error["message"])
    except Exception as e:
        return str(e.error["message"])

    return completions.choices[0].text


if __name__ == "__main__":
    while True:
        file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + ".wav"
        record_audio(file_name)
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        import openai

        token = open("data\\token.txt", "r").read()
        openai.api_key = token
        audio_file = open(file_name, "rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        print(transcript["text"])

        answer = generate_response(transcript["text"] + " Для лучшего понимания отвечай на русском языке.\n")
        print(answer)
