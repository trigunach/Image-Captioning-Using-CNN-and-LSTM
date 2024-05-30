## Basic phases for caption generation

### Data Collection from Dataset
* For the image caption generator, Flickr30K dataset is used. There are also other datasets like Flickr8k and MSCOCO dataset. The Flickr30k dataset contains about 30000 images each with 5 captions.

### Reading the data
* I created a dictionary which contains the name of the image without its extension type as a key and a list of the 5 captions for the corresponding images as values. In our datasets, there consists of large number of words.
### Data Cleaning
* Lowercasting all the characters and converting all the non-alphabetic characters (such as ‘#’, ‘%’, ‘$’, ‘&’, ‘@’ etc.), removing them and saving to a new file named ‘‘tokens_clean.txt’’. 

### Loading the training and testing set
* When we load the data, we will add two tokens in every caption as:
i. ‘startseq’: This is a start sequence token which will be added at the start of every
caption.
ii. ‘endseq’: This is an end sequence token which will be added at the end of every
caption.

### Image Pre-processing
* The images from the Flickr_30k dataset were first transformed into an array before feeding it into the ResNet 50 model. The features of the images are extracted just before the last layer of classification. The output is an array vector of length 2048 which represents the features extracted from the images. A dictionary with each image tagged to its features is formed and saved. 

### Text Pre-processing
* We need to encode each word into a fixed sized vector. We created two python dictionaries namely “word_to_index” and “index_to_word”.
*These two python dictionaries can be used as follows:
- word_to_index[‘w’]: - returns index of the word ‘w’
- index_to_word[‘yhat’]: - returns the word whose index is ‘yhat’

### Data Preparation using Generator Function
* For the generation of the description of the input images, it undergoes the process of Long Short Term Memory (LSTM)

### Inference
* The output of the model is softmax function that generates probability distribution across all the words.
* Greedy Search Algorithm was used to select the words with maximum probability.
* BLEU Score was used as evaluation metrics.

## RESULTS
#### UI was created using Flask.
#### Summary
1. Image sent to CNN(Resnet50).
2. Last layer of CNN is removed.
3. CNN produces image vector of length 2048.
4. Image vector and Caption sent to model.
5. Model generates probability distribution.
6. Select word with maximum probability.

## Implementation
- run ```text_data_processing.ipynb``` to create dictionary.
- run ```imagecaptioning_model.ipynb``` to create, train the model and evaluate the model.
- run ```main2.py``` to test the model on custom image.

* Place your dataset images into ```data/Images/```
* Place your dataset captions into ```data/textFiles/```
* After training your model, place them into ```model_checkpoints/```

## Requirements
1. Tensorflow
2. Visual Studio
3. Python 3.10
4. Flask
5. Numpy

#### Training time: ~30 hrs on i5 
