# MRP-SignDB
Script to download, segment and align sign language videos
it is possible to run the modules separately through console input.

If the scraper module does not work, please check whether the URL is correct. The videos are stored in a new folder, the subtitles files in audio_to_text\subtitles. It is also possible to manually add new files in the respective folders without running the entire module as well as put the new folder of videos\subtitles.

The audio module is relevant when the subtitles are not provided.
In the folder Audio_to_text it is necessary to add the LIUM jar 'LIUM_SpkDiarization-8.4.1', please dowload it from https://projets-lium.univ-lemans.fr/spkdiarization/download/, in order to create the segments of the audio. Successively use DeepSpeech to translate the segments into text, you can find the file to run in Google Colab in the folder.

In the alignment module is necessary to store the results from OpenPose(see the file to run in Google Colab) in a folder called coordinates_and_timestamps. SUccessively, the files regarding each video will be processed to create aligned segments.

The embedding part is still to be completed, the embeddings are created and stored in the alignment folder, then use them as a parameter to vecmap to cross-lingual alignment https://github.com/artetxem/vecmap.
 
