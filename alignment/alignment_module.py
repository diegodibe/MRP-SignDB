from alignment.video_audio_segmentation import video_audio_segmentation
from alignment.graph_processing import graph_processing
from alignment.embeddings import embeddings
import os
from util import input_checking


def alignment_module():
    print('\n Alignment module is running...')
    path = r'alignment'
    is_done = False
    if os.path.isdir(path + r'\coordinates_segments'):
        is_done = True
        print('Segment folders already exist, do you want to overwrite them?')
        if input_checking():
            is_done = False
    if not is_done:
        video_audio_segmentation(path)

    is_done = False
    if os.path.isdir(path + r'\graphs'):
        is_done = True
        print('Graph folder already exists, do you want to overwrite it?')
        if input_checking():
            is_done = False
    if not is_done:
        graph_processing(path)
    print('Do you want to create the embeddings?')
    if input_checking():
        embeddings(path)