import pandas as pd
import nltk
import string
import ast
import re
import unidecode

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter


def ingredient_parser(ingreds):
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill',
                'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml',
                'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre',
                'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#',
                'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme',
                'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre',
                'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']

    food_stops = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra',
                  'sprig',
                  'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried', 'sustainable',
                  'black',
                  'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea', 'quality', 'white', 'ripe',
                  'few',
                  'piece', 'source', 'to', 'organic', 'flat', 'smoked', 'ginger', 'sliced', 'green', 'picked', 'the',
                  'stick',
                  'plain', 'plus', 'mixed', 'mint', 'bay', 'basil', 'your', 'cumin', 'optional', 'fennel', 'serve',
                  'mustard',
                  'unsalted', 'baby', 'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut',
                  'good',
                  'brown', 'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on',
                  'deseeded',
                  'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest', 'pin',
                  'groundnut',
                  'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 'rocket',
                  'bone',
                  'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot',
                  'drained',
                  'sized', 'chestnut', 'watercress', 'fishmonger', 'english', 'dill', 'caper', 'raw', 'worcestershire',
                  'flake',
                  'cider', 'cayenne', 'tbsp', 'leg', 'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube',
                  'dressing',
                  'with', 'chunk', 'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled',
                  'saffron', 'other',
                  'chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian',
                  'shredded', 'divided',
                  'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice', 'more', 'coriander', 'bell', 'needed',
                  'thinly', 'boneless',
                  'half', 'thyme', 'cubed', 'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet',
                  'baking', 'beaten',
                  'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely',
                  'spring', 'chili',
                  'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root', 'quartered', 'head',
                  'softened', 'container',
                  'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'corn', 'pitted',
                  'sun', 'kosher',
                  'bite', 'toasted', 'lasagna', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod',
                  'anchovy', 'rom',
                  'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly',
                  'anise', 'thai',
                  'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati', 'marinara', 'dark', 'temperature',
                  'garnish', 'bouillon',
                  'loaf', 'shell', 'reggiano', 'canola', 'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long',
                  'broken', 'ketchup',
                  'bulk', 'cleaned', 'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind',
                  'pecorino',
                  'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link', 'firm',
                  'asafoetida',
                  'mild', 'dash', 'boiling']

    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = ast.literal_eval(ingreds)

    translator = str.maketrans('', '', string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []

    for i in ingredients:
        i.translate(translator)
        items = re.split(' |-', i)  # split hyphens and spaces
        items = [word for word in items if word.isalpha()]  # get rid of non alphabet letters
        items = [word.lower() for word in items]  # lowercase
        items = [unidecode.unidecode(word) for word in items]  # remove accents
        items = [lemmatizer.lemmatize(word) for word in items]  # lemmatize
        items = [word for word in items if word not in measures]  # remove measures
        items = [word for word in items if word not in food_stops]  # remove food stops

        if items:
            ingred_list.append(" ".join(items))

    ingred_list = " ".join(ingred_list)

    return ingred_list


if __name__ == "__main__":
    recipe_df = pd.read_csv(full_bonapp_df_clean.csv)
    recipe_df['ingredients_parsed'] = recipe_df['ingredients'].apply(lambda x: ingredient_parser(x))
    df = recipe_df[['dishtitle', 'ingredients_parsed', 'ingredients', 'urls']]
    df = recipe_df.dropna()

    df.to_csv('parsed_data.csv', index=False)