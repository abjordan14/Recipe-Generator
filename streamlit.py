import streamlit as st
import pymoji
import pandas as pd
import numpy as np
import SessionState
import os

import config, rec_sys
from ingredient_parser import ingredient_parser

import nltk

try:
    nltk.data.find('corpora/wordnet')
except:
    nltk.download('wordnet')

def make_clickable(name, link):
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'

def main():

    st.markdown(pymoji.replaceAliases('Bon Appetit Recipe Recommender :carrot:'))
    st.markdown("Enter the ingredients in your cupboard, and I'll find some recipes you might like")
    st.text("")

    session_state = SessionState.get(
        recipe_df = "",
        recipes = "",
        model_computed = False,
        execute_recsys = False,
        recipe_df_clean = ""
    )

    ingredients = st.text_input("So, what's in your pantry?")

    session_state.execute_recsys = st.button("Find Recipes")

    if session_state.execute_recsys:

        col1, col2, col3 = st.beta_columns([1, 6, 1])

        with col2:

            gif_runner = st.image("input/cooking_gif.gif")

        recipe = rec_sys.RecSys(ingredients)
        gif_runner.empty()
        session_state.recipe_df_clean = recipe.copy()

        recipe['url'] = recipe.apply (
            lambda row: make_clickable(row['recipe'], row['url']), axis=1
        )

        recipe_display = recipe[['recipe', 'url', 'ingredients']]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        session_state.model_computed = True
        session_state.execute_recsys = False

    if session_state.model_computed:

        recipe_all_box = st.selectbox (
            'Either see the top 5 recommendations or pick a particular recipe you like',
            ['Show me them all!', 'Select a single recipe'],
        )

        if recipe_all_box == "Show me them all!":
            st.write(session_state.recipe_display, unsafe_allow_html=True)

        else:
            selection = st.selectbox (
                'Select a delicious recipe', options = session_state.recipes
            )

            selection_details = session_state.recipe_df_clean.loc[
                session_state.recipe_df_clean.recipe == selection
            ]

            st.write(f"Recipe: {selection_details.recipe.values[0]}")
            st.write(f"Ingredients: {selection_details.ingredients.values[0]}")
            st.write(f"URL: {selection_details.url.values[0]}")
            st.write(f"Score: {selection_details.score.values[0]}")

    with st.sidebar.beta_expander('How it works', expanded=True):
        st.markdown(' How it works :thought_balloon:')
        st.write('I love Bon Appetit and I hope you do too.')


    if __name__ == '__main__':
        main()