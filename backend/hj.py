from moviepy.editor import *

mp4_file = '1.mp4'
mp3_file = r'E:\converted-mp-file.mp3'


videoclip = VideoFileClip(mp4_file)

audioclip = videoclip.audio
audioclip.write_audiofile(mp3_file)

audioclip.close()
videoclip.close()