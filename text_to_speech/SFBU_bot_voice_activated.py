# Content of utils.py
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.pdf import PyPDFLoader
import datetime
import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import whisper
import queue
import threading
import torch
import numpy as np
import re
import click
import urllib3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from openai import OpenAI



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
loader = PyPDFLoader('./2023Catalog.pdf')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs1 = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = DocArrayInMemorySearch.from_documents(docs1, embeddings)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo" if datetime.datetime.now().date() >= datetime.date(2023, 9, 2) else "gpt-3.5-turbo-0301", temperature=0),
        chain_type="stuff",
        retriever=retriever,
        # return_source_documents=True,
        # return_generated_question=True,
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    )





@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Whether to use the English model", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for the mic to detect", type=int)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--wake_word", default="hey computer", help="Wake word to listen for", type=str)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)
def main(model, english, energy, pause, dynamic_energy, wake_word, verbose):
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()

    threading.Thread(target=record_audio, args=(audio_queue, energy, pause, dynamic_energy,)).start()
    threading.Thread(target=transcribe_forever, args=(audio_queue, result_queue, audio_model, english, wake_word, verbose,)).start()
    threading.Thread(target=reply, args=(result_queue,verbose)).start()

    time.sleep(500)

    while True:
        print(result_queue.get())
        

def record_audio(audio_queue, energy, pause, dynamic_energy):
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Listening...")
        i = 0
        while True:
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1

def transcribe_forever(audio_queue, result_queue, audio_model, english, wake_word, verbose):
    stop_word = "stop"  # Define the stop word
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        predicted_text = result["text"]

        if predicted_text.strip().lower().startswith(wake_word.strip().lower()):
            pattern = re.compile(re.escape(wake_word), re.IGNORECASE)
            predicted_text = pattern.sub("", predicted_text).strip()
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            predicted_text = predicted_text.translate({ord(i): None for i in punc})
            if verbose:
                print("You said the wake word.. Processing {}...".format(predicted_text))

            if stop_word in predicted_text.lower():
                print("Interrupted by stop word.")
                continue

            result_queue.put_nowait(predicted_text)
        else:
            if verbose:
                print("You did not say the wake word.. Ignoring")


def reply(result_queue, verbose):
    cache = {}  # Cache for storing previously generated responses
    while True:
        question = result_queue.get()
        if question in cache:
            response1 = cache[question]
        else:
            prompt = "Q: {}?\nA:".format(question)
            data = qa.invoke({"question": prompt})
            response1 = data['answer']
            cache[question] = response1
        # We catch the exception in case there is no answer
        try:
            answer = data['answer']
            print(answer)
            response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=answer
            )

            file_name = "reply2.mp3"
            client.with_streaming_response.audio.speech.create
            response.stream_to_file(file_name)
        except Exception as e:
            choices = [
                "I'm sorry, I don't know the answer to that",
                "I'm not sure I understand",
                "I'm not sure I can answer that",
                "Please repeat the question in a different way"
            ]
            response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",input=choices[np.random.randint(0, len(choices))], lang="en", slow=False)
            if verbose:
                print(e)

        # In both cases, we play the audio
        # response.save("reply2.mp3")
        reply_audio = AudioSegment.from_mp3("reply2.mp3")
        play(reply_audio)
        time.sleep(500)
        os.remove("reply2.mp3")
        result_queue.queue.clear()

main()
