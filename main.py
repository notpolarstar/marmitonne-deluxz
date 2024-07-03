from flask import Flask, render_template, request
import urllib.request, json
import nltk.data
from deep_translator import GoogleTranslator

nltk.download('punkt')
app = Flask(__name__)


@app.route('/')
def home():
  return render_template("Page.html")

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
  plat = request.args.get('plat')
  plat = GoogleTranslator(source='auto', target='en').translate(plat)
  url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + plat
  response = urllib.request.urlopen(url)
  response = response.read()
  dict = json.loads(response)
  if dict["meals"] == None:
    return render_template("Page.html")
  for i in range(len(dict["meals"])):
    dict["meals"][i]["strMeal"] = GoogleTranslator(
      source='auto', target='fr').translate(dict["meals"][i]["strMeal"])
  #print(dict["meals"])
  return render_template("Search.html", recette=dict["meals"])


@app.route('/api/<plat_id>', methods=['GET', 'POST'])
def api(plat_id):
  #print("debut")
  #print(plat_id)
  url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + plat_id
  #print(url)
  response = urllib.request.urlopen(url)
  response = response.read()
  dict = json.loads(response)
  #print(dict["meals"])
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  inst = dict["meals"][0]["strInstructions"]
  inst = GoogleTranslator(source='auto', target='fr').translate(inst)
  inst = tokenizer.tokenize(inst)
  #print(inst)
  dict["meals"][0]["strMeal"] = GoogleTranslator(
    source='auto', target='fr').translate(dict["meals"][0]["strMeal"])

  ingredients = []
  mesures = []
  for ing in range(1, 21):
    ingredients.append(dict["meals"][0]["strIngredient" + str(ing)])
    mesures.append(dict["meals"][0]["strMeasure" + str(ing)])
  ingredients = list(filter(None and not " ", ingredients))
  #print(ingredients)
  dict["meals"][0]["strMeal"] = dict["meals"][0]["strMeal"].title()
  return render_template("Api.html",
                         plat=dict["meals"][0],
                         inst=inst,
                         ingredients=ingredients,
                         mesures=mesures)


app.run(host='0.0.0.0', port=80000)