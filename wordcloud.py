import bleach
from flask import jsonify

from flask import Flask, render_template, request, Response
from engine import ElasticSearchEngine

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
    if autocomplete_type not in ['ngram', 'prefix', 'match', 'suggest']:
        raise ValueError("autocomplete_type must be `prefix`, `ngram`, `suggest` or `match`")
    message = bleach.clean(input_)
    if autocomplete_type == "suggest":
        return suggest(message)
    result = ElasticSearchEngine().autocomplete(message, autocomplete_type)
    response = [f"<li class='list-group-item'>{x}</li>" for x in result]
    result = f'<ul id="country-list-{autocomplete_type}" class="list-group list-group-flush w-25">'
    for x in response:
        result += x
    result += "</ul>"
    return jsonify({'data': result, 'has_data': len(response) > 0})

@app.route("/wordcloud")
def wordcloud():
    response = ElasticSearchEngine().wordcloud()
    return jsonify({'data': response})

@app.route("/cities/<city_id>/increase_weight", methods=["POST"])
def increase_city_weight(city_id: str):
    ElasticSearchEngine().updateWeight(city_id)
    return Response(status=200)


def suggest(message: str):
    result = ElasticSearchEngine().suggest(message)
    response = [f"<li class='suggest-item list-group-item' id='city-{x['id']}' onclick='increaseWeight(this.id)'>{x['name']}</li>" for x in result]
    result = '<ul id="suggest-country-list" class="list-group list-group-flush w-25">'
    for x in response:
        result += x
    result += "</ul>"
    return jsonify({'data': result, 'has_data': len(response) > 0})