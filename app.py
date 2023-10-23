from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import requests
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app= Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
lemma = WordNetLemmatizer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/real')
def real():
    return render_template('real.html')

@app.route('/fake')
def fake():
    return render_template('fake.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        text = str(request.form['news'])
        # Text Preprocessing
        words = re.findall("[a-zA-Z]*", text)
        text = " ".join(words)
        # Lowering the text
        text = text.lower()
        # Spliting all the words
        text = text.split()
        # Removing Stop Words
        text = [word for word in text if word not in set(stopwords.words('english'))]
        # Lemmatization
        text = [lemma.lemmatize(word) for word in text]
        # Joining all remaining words
        text = " ".join(text)
        
        vectorized = vectorizer.transform(text).reshape(1, -1)

        prediction = model.predict(vectorized)[0]
        output = ""
        if prediction == 0:
            output="fake"
        else:
            output="real"
    return redirect(url_for(output))

if __name__=='__main__':
    app.run(debug=True)
