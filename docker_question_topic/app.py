from flask import Flask, render_template,request,url_for, jsonify

# NLP Packages
import tensorflow_hub as hub
import tensorflow as tf
import re
import random 
import time
import numpy as np
from tensorflow.keras.layers import Input, Lambda, Dense
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K
import pickle

app = Flask(__name__)

le =  None
model_que_topic = None

#Data cleaning operations
def replace_contraction(text):
    contraction_patterns = [ (r'won\'t', 'will not'), (r'can\'t', 'can not'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                         (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]
    patterns = [(re.compile(regex), repl) for (regex, repl) in contraction_patterns]
    for (pattern, repl) in patterns:
        (text, count) = re.subn(pattern, repl, text)
    return text
def replace_links(text, filler=' '):
        text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                      filler, text).strip()
        return text
def remove_numbers(text):
    text = ''.join([i for i in text if not i.isdigit()])
    return text
def cleanText(text):
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = replace_contraction(text)
    text = replace_links(text, "link")
    text = remove_numbers(text)
    text = re.sub(r'[,!@#$%^&*)(|/><";:.?\'\\}{]',"",text)
    text = text.lower()
    return text

#Universal Sentence Encoder module load
def UseTEmbedding(x):
	embed = hub.Module("sentence_encoder_T/")
	return embed(tf.squeeze(tf.cast(x, tf.string)), signature="default", as_dict=True)["default"]

#Model architecture
def build_model(): 
	input_text = Input(shape=(1,), dtype="string")
	embedding = Lambda(UseTEmbedding, output_shape=(512, ))(input_text)
	dense1 = Dense(256, kernel_regularizer=tf.keras.regularizers.l2(0.001), \
                   activation=tf.nn.relu)(embedding)
	dense2 = Dense(256, kernel_regularizer=tf.keras.regularizers.l2(0.001), \
                   activation=tf.nn.relu)(dense1)
	pred = Dense(6, activation='sigmoid')(dense2)
	model = Model(inputs=[input_text], outputs=[pred])	
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	return model

#Question topic enoder
with open("le_quetopic.pickle","rb") as f:
    le = pickle.load(f)

@app.route('/predict_topic',methods=['POST'])
def analyse():
	global le
	global model_que_topic
	pred = None
	start = time.time()
	if not request.json or not 'rawtext_list' in request.json:
		abort(400)
	rawtext_list = request.json['rawtext_list']

	prtext_list = [cleanText(i) for i in rawtext_list]
	prtext_list.append('')
    
	model_que_topic = build_model()
	with tf.Session() as session:
		K.set_session(session)
		session.run(tf.global_variables_initializer())  
		session.run(tf.tables_initializer())
		model_que_topic.load_weights('quetopic_model_useT.h5')
		pred = model_que_topic.predict(np.array(prtext_list))
    
	'''
	This -1 indexing shouldn't be there but presently helpless as GUSE is not running on single input :) 
	'''
	pred= pred[:-1]
	result = []
	for i in pred:
		result.append(dict(zip(le.classes_, i/sum(i))))

	response = {
		"output" : str(result), 
		"input" : str(rawtext_list),
        "time" : time.time() - start
	}

	return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)