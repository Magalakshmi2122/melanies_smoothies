# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order= st.text_input("Name On Smoothie")
st.write("The name on your smoothie will be",name_on_order)
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose upto 5 ingredients.:'
    , my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
      dora_insert = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled, hash_ing)
    VALUES 
      ('combo_for_Kevin', 'Kevin', FALSE, 7976616299844859825),
      ('combo_for_Divya', 'Divya', TRUE, -6112358379204300652),
      ('combo_for_Xi', 'Xi', TRUE, 1016924841131818535);
    """
    if st.button("Insert DORA Test Orders"):
        session.sql(dora_insert).collect()
        st.success("DORA test orders inserted!")

#         st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")
# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
