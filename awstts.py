import boto3
import json
import csv

def tts(text):
# Initialize the Boto3 Polly client
    polly_client = boto3.client('polly')

    # Request speech synthesis for audio output
    audio_response = polly_client.synthesize_speech(
        Engine='neural',
        Text=text,
        OutputFormat='mp3',
        VoiceId='Matthew'
    )

    # Request speech marks
    marks_response = polly_client.synthesize_speech(
        Engine='neural',
        Text=text,
        OutputFormat='json',
        VoiceId='Matthew' ,
        SpeechMarkTypes=['word']
    )

    # Extract and save the audio stream
    audio_stream = audio_response['AudioStream'].read()
    with open('speech.mp3', 'wb') as audio_file:
        audio_file.write(audio_stream)

    # Process and save the word timings as JSON
    word_timings = marks_response['AudioStream'].read()

    # print(word_timings)
    with open('subtitles.json', 'w') as doc:
        doc.write(word_timings.decode())

    # Remember to close the streams
    audio_response['AudioStream'].close()
    marks_response['AudioStream'].close()

    
    
    
