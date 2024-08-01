##### THIS IS THE MODIFIED VERSION OF PYTHON CODE WHERE SLIGHT CHANGES IN RETURN VALUES HAVE BEEN MADE AFTER USER TESTING #####
##### RUNS WITH modified.html, NO CHANGE NEEDED #####

# import statements

from flask import Flask, render_template, request, redirect, url_for, jsonify
import spacy
import requests
from string import punctuation
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
import assemblyai as aai
import moviepy.editor as mp
from gtts import gTTS
import os

app = Flask(__name__)

# wav audio extraction from the mp4 video

def extract_audio(video_path, audio_path):
    try:
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
    except AttributeError as e:
        print(f"An AttributeError occurred: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# summary paragraph to mp3 playback audio transformation  with gTTS

def read_out_loud(text, speed=0.5):
    if not text.strip():
        print("No text to speak.")
        return None
    try:
        tts = gTTS(text=text, lang='en', slow=(speed < 1.0))
        audio_path = "static/speech.mp3"
        tts.save(audio_path)
        print("Successfully converted text to speech.")
        return audio_path
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return None

# fetches word definition from WordsAPI

def get_easy_meaning(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
    headers = {
        "X-RapidAPI-Key": "ff451617a7msha599f3e42079e9cp1c5e4ajsnfe64a9f99b30",
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'definitions' in data and len(data['definitions']) > 0:
                easy_meaning = data['definitions'][0]['definition']
                return easy_meaning
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# fetching image URL and image description from UnsplashAPI, returns URL, description and meaning from get_easy_meaning()

def get_image_url(word):
    access_key = "crCCWXqqa2NkFi05lQHzkXAjMXYqXrqzzfRHKuFEGPg"
    url = f"https://api.unsplash.com/search/photos?query={word}&per_page=1"
    headers = {"Authorization": f"Client-ID {access_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['total'] > 0 and len(data['results']) > 0:
            image_url = data['results'][0]['urls']['regular']
            description = data['results'][0]['alt_description'] or 'No description available.'
            meaning = get_easy_meaning(word)
            return {'url': image_url, 'description': description, 'meaning': meaning}
        else:
            return search_synonym_image(word, headers)
    except Exception as e:
        print(f"An error occurred while fetching image: {e}")
        return {'url': '', 'description': 'No description available.', 'meaning': 'No meaning available.'}
    
# synonyms of words used to fetch images, used in get_image_url if image is not found for original word
# returns URL, description and meaning from get_easy_meaning()     

def search_synonym_image(word, headers):
    synonyms_url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    synonyms_headers = {
        "X-RapidAPI-Key": "ff451617a7msha599f3e42079e9cp1c5e4ajsnfe64a9f99b30",
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(synonyms_url, headers=synonyms_headers)
        if response.status_code == 200 :
            data = response.json()
            if 'synonyms' in data and len(data['synonyms']) > 0:
                for synonym in data['synonyms']:
                    url = f"https://api.unsplash.com/search/photos?query={synonym}&per_page=1"
                    image_response = requests.get(url, headers=headers)
                    image_data = image_response.json()
                    if image_data['total'] > 0 and len(image_data['results']) > 0:
                        return {
                            'url': image_data['results'][0]['urls']['regular'],
                            'description': image_data['results'][0]['alt_description'] or 'No description available.',
                            'meaning' : get_easy_meaning(word)
                        }
        return {'url': '', 'description': 'No description available.'}
    except Exception as e:
        print(f"An error occurred while fetching synonym image: {e}")
        return {'url': '', 'description': 'No description available.', 'meaning': 'No meaning available.'}

@app.route('/')
def index():
    return render_template('modified.html')

# video uploading path

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video_file' in request.files:
        video_file = request.files['video_file']
        if video_file.filename != '':
            video_folder = 'static/uploads/Documentaries'
            os.makedirs(video_folder, exist_ok=True)
            video_path = os.path.join(video_folder, video_file.filename)
            video_file.save(video_path)
            return redirect(url_for('process_video', video_filename=video_file.filename))
    return redirect(url_for('index'))

# video processing path, videoplayer and transcript rendered

@app.route('/process_video/<video_filename>')
def process_video(video_filename):
    video_path = os.path.join('static', 'uploads', 'Documentaries', video_filename)
    audio_path = "static/audio.wav"
    extract_audio(video_path, audio_path)
    
    aai.settings.api_key = "4b7c1827b9a343b192dbb93771a5d7b9"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    text = transcript.text
    
    # print transcript text to terminal

    print("Transcript:", text)

    return render_template('modified.html', transcript=text, video_url=url_for('static', filename=f'uploads/Documentaries/{video_filename}'))

# summarisation path, renders summary and highlighted words to HTML template

@app.route('/summarise', methods=['POST'])
def summarise():
    transcript = request.form['transcript']
    
    def summarize(text, per):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
                if word.text not in word_frequencies:
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
        
        max_frequency = max(word_frequencies.values())
        word_frequencies = {word: (freq / max_frequency) for word, freq in word_frequencies.items()}
        
        sentence_scores = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_frequencies:
                    if sent not in sentence_scores:
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]
        
        select_length = int(len(doc) * per)
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
        
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        
        summary = edit_summary(summary)
        
        return summary
    
    def edit_summary(text):
    
        nlp = spacy.load('en_core_web_sm')

        # fix improper sentence ending and beginning issue involving 'and'
        
        text = text.replace('. And', ' and')
        doc = nlp(text)
    
        sentences = list(doc.sents)
        corrected_sentences = []

        for sentence in sentences:
            tokens = list(sentence)
            have_found = False
            tense = None
            to_found = False

            # find 'have' and determine the tense of the first verb after 'have'

            for i, token in enumerate(tokens):
                if token.text.lower() == 'have':
                    have_found = True
                elif have_found and token.pos_ == 'VERB':
                    if token.tag_ in ['VBD', 'VBN']:  
                        tense = 'past'
                    else:
                        tense = 'present'
                    break

            # if 'have' is found and past tense is determined, correct subsequent verbs before "to"

            if have_found and tense:
                corrected_tokens = []
                for token in tokens:
                    if token.text.lower() == 'to':
                        to_found = True

                    if token.pos_ == 'VERB' and not to_found:
                        if tense == 'past' and token.tag_ not in ['VBD', 'VBN']:
                            corrected_tokens.append(token.lemma_ + 'ed') 
                        else:
                            corrected_tokens.append(token.text)
                    else:
                        corrected_tokens.append(token.text)
                corrected_sentence = ' '.join(corrected_tokens)
            else:
                corrected_sentence = sentence.text
        
            corrected_sentences.append(corrected_sentence)
    
        # format punctuations properly

        corrected_paragraph = ' '.join(corrected_sentences)
        corrected_paragraph = corrected_paragraph.replace(' ,', ',').replace(' .', '.')

        return corrected_paragraph
    

    summary = summarize(transcript, 0.03)
    words_with_meanings = {}
    for word in summary.split():
        if len(word) > 6:
            easy_meaning = get_easy_meaning(word)
            if easy_meaning:
                words_with_meanings[word] = easy_meaning
    
    return jsonify({'summary': summary, 'words_with_meanings': words_with_meanings})

# read out loud path, renders error log and audio mp3 URL for playback to HTML template

@app.route('/read_out_loud', methods=['POST'])
def read_out_loud_route():
    data = request.json
    summary = data['summary']
    speed = float(data.get('speed', 0.3))
    if not summary.strip():
        return jsonify({'success': False, 'error': 'No text to speak'})
    try:
        audio_path = read_out_loud(summary, speed)
        if audio_path:
            return jsonify({'success': True, 'audio_url': url_for('static', filename='speech.mp3')})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate speech'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# image URL and description fetching path, renders word meaning, image URL and description to HTML template

@app.route('/get_image_url', methods=['POST'])
def get_image_url_route():
    word = request.json['word']
    try:
        image_info = get_image_url(word)
        return jsonify(image_info)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
