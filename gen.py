import numpy as np
import cv2
import pandas as pd
import json
from moviepy.editor import VideoFileClip, AudioFileClip
from awstts import tts

def main():
    def pipeline(frame):
        nonlocal ms, i, text
        if ms > end or i == len(words): return frame
        writable_frame = np.copy(frame)
        
        if ms > float(timestamps[i]): 
            text = words[i] 
            if len(text) < 3 and i+1 < len(words) and len(words[i+1]) < 10:
                text += ' ' + words[i+1]
                i += 1
            i+=1
        ms += inc
        height, width, _ = writable_frame.shape
        
        text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 8, thickness=3)[0]
        text_x = (width - text_width) // 2
        text_y = (height + text_height) // 2
        
        # Put the text on the writable frame with white color and black outline
        cv2.putText(writable_frame,text,(text_x, text_y),cv2.FONT_HERSHEY_SIMPLEX,8,(0,0,0),80,cv2.LINE_AA)
        cv2.putText(writable_frame,text,(text_x, text_y),cv2.FONT_HERSHEY_SIMPLEX,8,(255,255,255),40,cv2.LINE_AA)
        return writable_frame
    
    with open("script.txt", "r") as file:
        txt = file.read().replace("\n", ". ")
        # print(txt)
        tts(txt)
    
    df = pd.read_json("subtitles.json", lines=True)
    # f = open('debug.txt', 'w')
    # for i in range(len(df)):
    #     print(df.iloc[i:i+1], file=f)
    # print(df, file = f)
    timestamps = df['time'].tolist()
    words = df['value'].tolist()
    ends = df['end'].tolist()
    end = ends[-1] + timestamps[-1]
    # print(words)
    
    video = VideoFileClip("vid.mp4")
    video = video.set_duration(end/1000+0.2) 
    fps = 20.0
    video.fps = fps
    
    text = ''
    ms, i, inc= 1000.0/fps/2, 0, 1000.0/fps
    # Process and write the output video
    out_video = video.fl_image(pipeline)
    out_video.audio = AudioFileClip("speech.mp3")
    out_video.write_videofile("vidout.mp4", audio=True, fps=fps)

main()