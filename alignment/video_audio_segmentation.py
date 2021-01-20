import math
import ffmpeg  # install 'ffmpeg-python'
import os
import numpy as np
from util import get_path
import pysubs2
from pysubs2 import time
import time
from moviepy.editor import VideoFileClip


def video_audio_segmentation(path):
    for file in os.listdir('videos'):
        video_ns = [s for s in file if s.isdigit()]
        video_n = ''
        for value in video_ns:
            video_n += value
        try:
            timestamps = np.load(path + r'\coordinates_and_timestamps\video{c}_timestamp.npy'.format(c=video_n))
            do_segments(path, video_n, timestamps)
        except FileNotFoundError:
            print('No timestamps found for video {c}'.format(c=video_n))


def do_segments(path, video_n, timestamps):
    time_per_frame, keypoints = get_frame_rate(path, video_n)
    for counter_segments, timestamp in enumerate(timestamps):
        start = round(timestamp[0], 3)
        end = round(timestamp[1], 3)
        segment = 'segment{s}'.format(s=counter_segments)

        print('Segment n.', counter_segments, ' starts at second ', time.strftime('%H:%M:%S', time.gmtime(start)),
              ' ends at ', time.strftime('%H:%M:%S', time.gmtime(end + 0.5)))

        do_video_segments(path, video_n, segment,  time.strftime('%H:%M:%S', time.gmtime(start)),
                         time.strftime('%H:%M:%S', time.gmtime(end)))

        do_keypoints_segments(path, keypoints, video_n, segment, start, end, time_per_frame)

        do_subtitles_segments(path, video_n, segment, start, end)

    print('segments video {c} created.'.format(c=video_n))


def do_video_segments(path, video_n, segment, start, end):
    (
        ffmpeg
        .input('videos/video{}.ts'.format(video_n))
        .trim(start=start, end=end)
        .setpts('PTS-STARTPTS')
        .output(get_path(video_n, r'\{p}\video_segments'.format(p=path), 'video{}_' + segment + '.mp4'))
        .run()
    )


def get_frame_rate(path, video_n):
    video_name = 'video' + video_n
    clip = VideoFileClip(os.curdir + r'\videos\{v}.ts'.format(v=video_name))
    duration = clip.duration

    print(duration)

    for file1 in os.listdir(path + r'\coordinates_and_timestamps'):

        if (video_name in file1) and (file1.endswith('.npy')) and ("pose" in file1):
            print("In second loop")
            pose_tensor = np.load(path + r'\coordinates_and_timestamps\{f}'.format(f=file1))
            pose_frames = pose_tensor.shape[0]

        if (video_name in file1) and (file1.endswith('.npy')) and ("face" in file1):
            print("In third loop")
            face_tensor = np.load(path + r'\coordinates_and_timestamps\{f}'.format(f=file1))
            face_frames = face_tensor.shape[0]

        if (video_name in file1) and (file1.endswith('.npy')) and ("lefthand" in file1):
            lefthand_tensor = np.load(path + r'\coordinates_and_timestamps\{f}'.format(f=file1))
            lefthand_frames = lefthand_tensor.shape[0]

        if (video_name in file1) and (file1.endswith('.npy')) and ("righthand" in file1):
            righthand_tensor = np.load(path + r'\coordinates_and_timestamps\{f}'.format(f=file1))
            righthand_frames = righthand_tensor.shape[0]

    if (pose_frames == face_frames) and (face_frames == lefthand_frames) and (lefthand_frames == righthand_frames):
        pass
    else:
        print("ERROR IN THE SIZE OF TENSORS!!")

    keypoints_dict = {'pose': pose_tensor,
                      'face': face_tensor,
                      'left_hand': lefthand_tensor,
                      'right_hand': righthand_tensor}

    return (duration / pose_frames), keypoints_dict


def do_keypoints_segments(path, keypoints, video_n, segment, start, end, time_per_frame):
    start_frame = math.floor(start / time_per_frame)
    end_frame = math.floor(end / time_per_frame)

    print(start_frame, end_frame)

    for key, value in keypoints.items():
        out = segment + '_' + key + '.npy'
        with open(get_path(video_n, r'\{p}\coordinates_segments'.format(p=path), 'video{}_' + out), 'wb') as f:
            np.save(f, value[start_frame:end_frame, :, :])


def do_subtitles_segments(path, video_n, segment, start, end):
    alignedsub = ''

    startms = start * 1000
    endms = (end + 0.5) * 1000

    # code for subtitles segments
    subs = pysubs2.load(r'audio_to_text\subtitles\subtitles{c}.txt'.format(c=video_n), encoding='latin-1')  # "utf-8"
    i = 0
    for l in subs:
        # print(l)
        # print(l.start)  # shows the start timestamp in miliseconds
        # print(l.end)
        if i > 1 and l.start < endms:  # first 2 subs are the same in every file (date etc)
            if l.start < startms < l.end:
                # if subtitle starts before the video segment starts and ends while the video segment still
                # plays

                if subs[i].text[0].isupper():
                    alignedsub += ' ' + subs[i].text

                elif ('.' in subs[i - 1].text) or ('?' in subs[i - 1].text) or (subs[i - 1].text[0].isupper()):
                    if '.' in subs[i - 1].text:
                        if subs[i - 1].text[-1] != '.':
                            alignedsub += ' ' + subs[i - 1].text.split('.')[-1] + ' ' + subs[i].text
                        # else:
                        #     alignedsub += ' ' + subs[i].text
                    elif '?' in subs[i - 1].text:
                        if subs[i - 1].text[-1] != '?':
                            alignedsub += ' ' + subs[i - 1].text.split('?')[-1] + ' ' + subs[i].text
                        # else:
                        #     alignedsub += ' ' + subs[i].text
                    elif subs[i - 1].text[0].isupper():
                        alignedsub += ' ' + subs[i - 1].text + ' ' + subs[i].text

                elif ('.' in l.text) or ('?' in l.text):
                    if '.' in l.text:
                        if subs[i].text[-1] != '.':
                            alignedsub += ' ' + subs[i].text.split('.')[-1]
                    elif '?' in l.text:
                        if subs[i].text[-1] != '?' and subs[i].text[0].isupper():
                            alignedsub += ' ' + subs[i].text.split('?')[-1]

            elif l.start > startms and l.end < endms:
                # if subtitle starts and ends while the video segment is playing
                if alignedsub == '' and subs[i].text[0].isupper() is False:
                    if ('.' in subs[i - 1].text) or ('?' in subs[i - 1].text) or (subs[i - 1].text[0].isupper()):
                        if '.' in subs[i - 1].text:
                            if subs[i - 1].text[-1] != '.':
                                alignedsub += ' ' + subs[i - 1].text.split('.')[-1] + ' ' + subs[i].text
                            # else:
                            #     alignedsub += ' ' + subs[i].text
                        elif '?' in subs[i - 1].text:
                            if subs[i - 1].text[-1] != '?':
                                alignedsub += ' ' + subs[i - 1].text.split('?')[-1] + ' ' + subs[i].text
                            # else:
                            #     alignedsub += ' ' + subs[i].text
                        elif subs[i - 1].text[0].isupper():
                            alignedsub += ' ' + subs[i - 1].text + ' ' + subs[i].text

                else:
                    alignedsub += ' ' + subs[i].text

            elif l.start < endms < l.end:
                # if subtitle starts before the video segment ends and continues after that
                if ('.' in subs[i - 1].text) or ('?' in subs[i - 1].text):
                    if '.' in subs[i - 1].text:
                        alignedsub = alignedsub.replace(alignedsub.split('.')[-1], '')
                    elif '?' in subs[i - 1].text:
                        alignedsub = alignedsub.replace(alignedsub.split('?')[-1], '')

                elif ('.' in l.text) or ('?' in l.text):
                    if '.' in l.text:
                        alignedsub += ' ' + subs[i].text.split('.')[0] + '.'
                    elif '?' in l.text:
                        alignedsub += ' ' + subs[i].text.split('?')[0] + '?'

                elif subs[i].text[0].isupper():
                    pass
        i += 1
    alignedsub = alignedsub.replace("\\N", " ")
    alignedsub = alignedsub[1:]
    print(alignedsub)
    with open(get_path(video_n, r'\{p}\subtitle_segments'.format(p=path), 'video{}subtitle' + segment + '.txt'),
              'w') as f:
        f.write(alignedsub)

