from bs4 import BeautifulSoup
import requests

def gschol_search(query):
    newq = query.replace(" ", "+")
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C15&q=" + newq + "&btnG="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 elements with class "gs_rt"
    h3_elements = soup.find_all('h3', class_='gs_rt')

    # Extract href attributes within <a> elements under each h3
    for h3_element in h3_elements:
        a_element = h3_element.find('a')
        if a_element:
            href_value = a_element.get('href')
            print(href_value)

def snopes_search(query):
    newq = query.replace(" ", "%20")
    url = "https://www.snopes.com/search/" + newq + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 elements with class "gs_rt"
    div_elements = soup.find_all('div', class_='article_wrapper')

    # Extract href attributes within <a> elements under each h3
    for div in div_elements:
        input_element = div.find('input')
        if input_element:
            href_value = input_element.get('value')
            print(href_value)