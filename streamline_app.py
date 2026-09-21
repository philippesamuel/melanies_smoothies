# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

name_on_order = st.text_input(label='Name on Smoothie:', value="")
st.write(f"The name on your Smoothie will be: {name_on_order}")

session = get_active_session()
tbl_fruits = session.table("smoothies.public.fruit_options")
df_fruits = tbl_fruits.select(col('FRUIT_NAME'))
# st.dataframe(data=df_fruits, use_container_width=True)

ingredients = st.multiselect(
    label='Choose up to 5 ingredients: ', 
    options=df_fruits,
    max_selections=5,
)

if ingredients:
    ingredients_string = ', '.join(ingredients)
    
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
        
