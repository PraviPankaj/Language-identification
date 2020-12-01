# Language Identification

The repository contains the code that allows you to obtain a dataset for desired languages and train a neural network that's able to identify the language spoken in a recording as short as 3 seconds.
Reference: https://github.com/HPI-DeepLearning/crnn-lid 


## Repository Structure
The repository is separated into four categories, with each containing its own ReadMe. 

| Folder | Description |
|--|--|
| [*data/*]| Contains the scripts for downloading and preprocessing the dataset. |
| [*tensorflow/*] | Neural-network-related scripts. Creation, training, evaluation etc.|


## Requirements
To install all the required packages, run

    pip install -r requirements.txt

Please note that the `requirements.txt` specifies the CPU-based `tensorflow`. 

Furthermore, you should have the following utilities installed in your system:

- FFmpeg
- SoX
- youtube-dl



