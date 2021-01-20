# MRP-SignDB
Script to download, segment and align sign language videos
it is possible to run the modules separately through console input.

The scripts interacts with many files, we observed that some machines get an error because of the encoding during reading\writing files. Also be careful in istall the right packages.  

The URL could be different of the default one. The videos are stored in a new folder called MRP-SignDB\videos, the subtitles files in MRP-SignDB\audio_to_text\subtitles. It is also possible to manually add new files in the respective folders without running the entire module. Alternativally, to ensure the succesive modules to run correcly manually add MRP-SignDB\videos and MRP-SignDB\audio_to_text\subtitles containg the files.

The audio module is relevant when the subtitles are not provided.
In the folder Audio_to_text it is necessary to add the LIUM jar 'LIUM_SpkDiarization-8.4.1', it is possible to dowload it from https://projets-lium.univ-lemans.fr/spkdiarization/download/, in order to create the segments of the audio. Successively use DeepSpeech to translate the segments into text, you can find in the folder the file deepspeech.ipynb.

In the alignment module is necessary to store the results of OpenPose(openpose.ipynb) in a folder called coordinates_and_timestamps. SUccessively, the files regarding each video will be processed to create aligned segments.

The embedding part is still to be completed, the embeddings are created and stored in the alignment folder, then use them as a parameter to vecmap to cross-lingual alignment https://github.com/artetxem/vecmap.
 
