# QuestionTopicAnalysis
Finding the question topic plays a major role in various use-cases starting from question answering system to answer evaluation. 

This repo shows a question topic identifier starting from building model, utilizing transfer learning to containerized deployment. 

The model training and saving using Google's universal sentence encoder is done in question_topic.ipynb

The dataset used is : http://cogcomp.org/Data/QA/QC/

Inside the docker_Question_Topic folder, the flask api is there along with the instructions and files toput it into a docker.
