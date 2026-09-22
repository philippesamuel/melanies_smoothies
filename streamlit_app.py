import requests

import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

name_on_order = st.text_input(label='Name on Smoothie:', value="")
st.write(f"The name on your Smoothie will be: {name_on_order}")

cnx = st.connection("snowflake")
session = cnx.session()
tbl_fruits = session.table("smoothies.public.fruit_options")
df_fruits = tbl_fruits.select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=df_fruits, use_container_width=True)

ingredients = st.multiselect(
    label='Choose up to 5 ingredients: ', 
    options=df_fruits,
    max_selections=5,
)


if ingredients:
    ingredients_string = ', '.join(ingredients)
        
    for fruit in ingredients:
        search_on = (
            df_fruits
                .filter(col('FRUIT_NAME') == fruit)
                .select(col('SEARCH_ON'))
                .first()[0]
            )
        url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        st.subheader(f"{fruit} Nutrition Information")
        smoothiefroot_response = requests.get(url)
        df_smoothie = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # st.write(ingredienst_string)

    insert_orders_stmt = f"""
    insert into smoothies.public.orders(ingredients, name_on_order)
    values (?, ?)
    """

    # st.write(insert_orders_stmt)
    # st.stop()
    
    submit_btn = st.button('Submit Order')

    if submit_btn:
        session.sql(
            insert_orders_stmt, 
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        
