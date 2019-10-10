

Lab1105 team’s project description for the first stage of 2019 ICDM/ICBK Knowledge Graph Contest



********************
Introduction 
*************************

The aim of our project for this the first stage of contest.2019 ICDM/ICBK Knowledge Graph Contest is to extract triplet Entity-Relation-Entity (ERE)  from dataset consisting of 300 recent published articles from news media of 4 industries which are automotive engineering, cosmetics, public security and catering services.
To do that, we Firstly, use pandas to read the dataset. Then, we do some preprocessing operations on the texts from the dataset such as extend contraction’s forms and remove stopwords that we had defined. Then we use spaCy which is an industrial-strength nlp library to analyze the sentence and use neuralcoref to perform coreference resolution. We change the threshold in the code to make the result better. We use doc.ent(a method in spacy) to get named entities first. However, doc.ent has some drawbacks. It may miss some important entities that we need, and sometimes the entity is just a single word with incomplete meaning. So we use a deep learning model(BiLSTM-CRF) and noun_chunks to enhance the performance. Deep learning model can extract more entities and noun_chunks can get  complete noun phrases which have complete meaning. After that, we use dependency parsing to extract EREs that we want by adding some rules . At last, we store these EREs in dataframe and use pandas again to write them into the submission.csv.


******************
Project files organization
***************************

-DL directory :
We store here the deep learning model we trained and predict.py can extract some entities from a given text. We import that file when we extract entities.
-Data directory stores the original dataset (icdm_contest_data.csv) and the submission file will be generated in this directory.
-read_csv.py :
Run read_csv.py and the program will read and process the dataset and generate a new file submission.csv in data directory.
-relation_extraction.py :
In this file we do some preprocessing operation on the dataset and extract EREs we want. In the function dac_helper(), we remove some specific stopwords and change some specific formats. Then, in function get_ent_and_rel, we do coreference resolution and extract entities and relations. At last, the filter_ERE() function will remove some entities and relations which are not right.
-SPO.py:
 In this file we use spaCy to do the dependency parsing to get subject-predicate-object relations and we do lemmatization to combine some same words with different forms.
-ADV.py :
In this file we use dependency parsing again to get intermediary relations.



*************
Requirements:
***************
os:
Windows 10 64-bits

pandas==0.24.2
tensorflow==1.13.0-rc2
spacy==2.1.0
neuralcoref==4.0.0
nltk==3.4.4


******************
How  to run the project
************************

run Trian_Model.py first to train the model and then run read_csv.py and the program will read and process the dataset and generate a new file submission.csv in data directory.

