import os
import subprocess
import moviepy.editor
from pydub import AudioSegment as am
from util import get_path, input_checking


def audio_module():
    path = r'audio_to_text'
    submodules = {'extract' : {'question': 'Audio folder already exists, do you want to extract the audio and overwrite it?',
                               'folder': path + r'\audio',
                               'process': processing},
                  'lium': {'question': 'Segments folder already exists, do you want to overwrite it using LIUM?',
                            'folder': path + r'\segments',
                            'process': process_segments},
                  'deepspeech': {'question': 'Subtitles folder already exists, do you want to overwrite it using DeepSpeech?',
                                  'folder': path + r'\ds_subtitles',
                                  'process': translate_segments}
                  }
    print('\n Audio module is running...')
    is_done = False
    if os.path.isdir(path + r'\subtitles'):
        is_done = True
        print('Subtitles folder already exists, it contains the following files:')
        [print(file) for file in os.listdir(path + r'\subtitles')]
        print('do you want to continue with the audio module?')
        if input_checking():
            is_done = False
    if not is_done:
        for submodule in submodules.values():
            check_if_processed(submodule, path)


def processing(path): # (video_path, audio_exp):
    directory = os.path.abspath(os.curdir) + r'\videos'
    for counter, file in enumerate(os.listdir('videos')):
        audio_path = get_path(counter, r'\{p}\audio'.format(p=path), 'audio_video{}.wav')

        # To extract the audio from the videos
        video = moviepy.editor.VideoFileClip(os.path.join(directory, file))
        audio = video.audio
        audio.write_audiofile(audio_path)

        # Process the audio
        sound = am.from_file(audio_path, format='wav', frame_rate=22050)
        sound = sound.set_frame_rate(16000)
        sound = sound.set_channels(1)
        sound.export(audio_path, format='wav', bitrate="256k")


def process_segments(path):
    try:
        os.mkdir(path + '/segments')
    except OSError:
        pass
    param = r'java -jar {p}\LIUM_SpkDiarization-8.4.1.jar '.format(p=path)
    input = r'--fInputMask={p}\audio\audio_video{c}.wav '.format(p=path, c=0)
    output = r'--sOutputMask={p}\segments\segments_video{c}.seg '.format(p=path, c=0)
    param += input + output + r'test'
    subprocess.run(param, shell=True)

    start = []  # Creating two empty lists
    dur = []

    with open(path + r'\segments\segments_video{c}.seg'.format(c=0)) as f:
        for line in f:
            x = line.split()

            if x[0] == ';;':  # To exclude the irrelevant lines, separation of the clusters
                start = start
                dur = dur
            else:
                start.append(int(x[2]))
                dur.append(int(x[3]))

    end = [a + b for a, b in zip(start, dur)]  # Creating a list to store the end of the segments

    # The list 'seg' now will include all the segments in a format: (start,end)
    seg = []
    for i in range(len(start)):
        seg.append([start[i], end[i]])

    # With the extracted audio as an input, the segmented .wav files are created and stored in a folder.
    try:
        os.mkdir(path + '/audio_segments')
    except OSError:
        pass
    print('Audio module is creating the segments..')
    for i in range(len(seg)):
        t1 = (seg[i][0]) * 10
        t2 = (seg[i][1]) * 10

        newAudio = am.from_wav(path + r'\audio\audio_video{c}.wav'.format(c=0))
        newAudio = newAudio[t1:t2]
        newAudio.export(path + r'\audio_segments\segment{cs}video{cv}.wav'.format(cs=i, cv=0), format='wav')


def translate_segments(path):
    print('To use DeepSpeech please follow the instruction on README')


def check_if_processed(submodules, path):
    flag = True
    if os.path.isdir(submodules['folder']):
        print(submodules['question'])
        if not input_checking():
            flag = False
    if flag:
        submodules['process'](path)
