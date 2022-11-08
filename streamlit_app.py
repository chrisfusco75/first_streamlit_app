import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') 

streamlit.title('My Parents New Healthly Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free-Range Eggs') 
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return (fruityvice_normalized)

streamlit.header('Fruityvice Fruit Advice!')
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error("Please select a fruit to get information.")
  else: 
    back_from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_func)

except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
#sno func
def get_fruit_load_list():
        with my_cnx.cursor() as my_cur: 
                my_cur.execute("select * from fruit_load_list")
                return my_cur.fetchall()

#add button
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list_values ('from streamlit')")
            return "Thanks for adding " + new_fruit
    
fruit_add = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
if streamlit.button('Add a Fruit to the list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_func = insert_row_snowflake(fruit_add)
        streamlit.text(back_from_func)

#halt!
streamlit.stop()    
