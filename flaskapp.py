from flask import Flask
from flask import request
from flask import render_template
from textblob import TextBlob
from io import StringIO
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    text = str(text)
    data = pd.read_csv('database.csv')
    img = BytesIO()
    la = data[(data['State'] == text)]
    dis=la['Disaster Type'].value_counts()
    sns.barplot(dis.index, dis.values, alpha=0.8)
    plt.xlabel('Type of disaster', fontsize=14)
    plt.xticks(rotation='vertical')
    plt.ylabel('Number os disasters', fontsize=14)
    plt.title(text, fontsize=16)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}" align="middle">'.format(plot_url)

if __name__ == '__main__':
    app.run()