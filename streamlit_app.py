# Import python packages.
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import streamlit as st

# Write directly to the app.
st.title(f"Smoothie chooser :balloon: {st.__version__}")
st.write(
  """Choose the fruits you want!
  """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input("Smooothie name")
st.write("The name on your smoothie will be", name)

ingredient_list = st.multiselect(
    'Choose five ingredients',
    my_dataframe,
    max_selections=5
)
if ingredient_list:
    ingredient_string = ''
    for f in ingredient_list:
        ingredient_string += f + ' '

   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('""" + ingredient_string + """','"""+name+"""')"""
    st.write(my_insert_stmt)
    confirm = st.button('Submit Order')
    if confirm:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



