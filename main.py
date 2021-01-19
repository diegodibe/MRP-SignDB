from scraper import website_handler
from audio_to_text import audio_module
from alignment import alignment_module
from util import input_checking

if __name__ == '__main__':
    print('Do you want to download new videos using the scraper?')
    if input_checking():
        website_handler.scraper()
    print('Do you want to process the audio stream?')
    if input_checking():
        audio_module.audio_module()
    print('Do you want to run the alignment module?')
    if input_checking():
        alignment_module.alignment_module()
