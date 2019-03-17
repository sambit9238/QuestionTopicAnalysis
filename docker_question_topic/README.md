# question_topic_trec
Question topic identification using Google's universal sentence encoder

To run the docker of question topic identification to use it as a micro service for your application:
	
	#First change the docker file to take app.py as the application script
	1. Come to this directory.
	2. Build the docker image : docker build -t question_topic .
	3. Run the container :   docker run -p 8888:5000 --name question_topic question_topic

	Now the docker is running on the port 8888 in localhost.


To supply the input, 
	curl 	--request POST   
		--url http://0.0.0.0:8888/predict_topic   
		--header 'content-type:	application/json'   
		--data '{"rawtext_list":["Where do you work now?", "What is your salary?"]}'
		
		
The output,
	{
  	"input": "['Where do you work now?', 'What is your salary?']",
  	"output": "[	{'ABBR': 0.0033528977, 
				'DESC': 0.0013749895,
				'ENTY': 0.0068545835,
				'HUM': 0.7283039,
				'LOC': 0.25804028,
				'NUM': 0.0020733867}, 
			{'ABBR': 0.0012655753, 
				'DESC': 0.0079659065, 
				'ENTY': 0.011016952, 
				'HUM': 0.028764706, 
				'LOC': 0.013653239, 
				'NUM': 0.93733364}
			]"



