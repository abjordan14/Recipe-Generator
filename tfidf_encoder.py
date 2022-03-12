import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

df_recipes = pd.read_csv('parsed_data.csv')