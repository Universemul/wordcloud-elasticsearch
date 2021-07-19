import bleach
from flask import jsonify

from flask import Flask, render_template, request, Response
from engine import ElasticSearchEngine
from es_helpers import WORDCLOUD_INDEX, MEETING_POINTS_INDEX

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():
    return render_template('wordcloud.html')

@app.route("/autocomplete")
def home_autocomplete():
    return render_template('autocomplete.html')

@app.route("/autocomplete/<autocomplete_type>/<input_>", methods=["GET"])
def autocomplete(autocomplete_type: str, input_: str):
    if autocomplete_type not in ['ngram', 'prefix']:
        raise ValueError("autocomplete_type must be `prefix` or `ngram`")
    message = bleach.clean(input_)
    response = [f"<li class='list-group-item'>{x}</li>" for x in ElasticSearchEngine().autocomplete(message, autocomplete_type)]
    result = '<ul id="country-list" class="list-group list-group-flush w-25">'
    for x in response:
        result += x
    result += "</ul>"
    return jsonify({'data': result, 'has_data': len(response) > 0})

@app.route("/wordcloud")
def wordcloud():
    response = ElasticSearchEngine().wordcloud()
    return jsonify({'data': response})
