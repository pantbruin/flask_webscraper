from flask import Flask
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/<string:search_term>')
def hello(search_term):

    path_as_list = search_term.split("_")

    for index in range(len(path_as_list)):
        path_as_list[index] = path_as_list[index].lower().capitalize()

    corrected_path = "_".join(path_as_list)

    full_url = 'https://en.wikipedia.org/wiki/' + corrected_path

    # Make get request
    wiki_response = requests.get(full_url)

    # Parse response content
    soup = BeautifulSoup(wiki_response.content, 'html.parser')

    infobox_table = soup.find("table", class_="infobox")

    # Look in infobox table first
    if infobox_table:
        image_element = infobox_table.find("img")
        if image_element:
            attributes_as_dict = image_element.attrs
            final_url = 'https:' + attributes_as_dict['src']
            return {'image_url': final_url}

    first_thumbnail_image = soup.find("img", class_="thumbimage")
    if first_thumbnail_image:
        attributes_as_dict = first_thumbnail_image.attrs
        final_url = 'https:' + attributes_as_dict['src']
        return {'image_url': final_url}
    else:
        return {'image_url': False}
