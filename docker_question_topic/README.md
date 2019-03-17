# sentiment_analysis_textblob
Sentiment Analysis using Textblob deployed through flask and docker.

To run the docker of sentiment analyzer app:
	
	#First change the docker file to take app.py as the application script
	1. Come to this directory.
	2. Build the docker image : docker build -t sentiment_analysis_textblob.
	3. Run the container :   docker run -p 8888:5000 --name sentiment_analysis sentiment_analysis_textblob

	Now the docker is running on the port 8888 in localhost.


To run the docker of sentiment analysis to use it as a micro service for your application:

	#First change the docker file to take api_app.py as the application script
	1. Come to this directory.
	2. Build the docker image : docker build -t sentiment_analysis_textblob.
	3. Run the container :   docker run -p 8888:5000 --name sentiment_analysis sentiment_analysis_textblob

	Now the docker is running on the port 8888 in localhost.

	To supply the input, 
	curl --request POST   
		 --url http://localhost:8888/analyse   
		 --header 'content-type: application/json'   
		 --data '{"rawtext":"Inoffensive and unremarkable."}'

    The output:
    	{
  			"blob_sentiment": "0.5",
			"blob_subjectivity": "0.75",
			"final_time": "0.011960983276367188",
			"number_of_tokens": "9",
			"received_text": "The mother of such children would become very happy.",
			"summary": "['mothers']"
		}




