FROM python:3.6.3

# install Python modules needed by the Python app
COPY . /question_topic_app
WORKDIR /question_topic_app

RUN mkdir sentence_encoder_T
RUN pip install --no-cache-dir -r requirements.txt
RUN curl -L "https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed" | tar -zxvC sentence_encoder_T

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "app.py"]
