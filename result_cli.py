import requests, bs4

# Getting the html data from the website
url = 'https://sgbau.ucanapply.com/result-details'
session = requests.Session()
page = session.get(url)

# Extracting token from the page
soup = bs4.BeautifulSoup(page.content, 'html.parser')
token = soup.find('input', {'name': '_token'}).get('value')

# Implementing headers and data dictionary

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-CSRF-TOKEN': token,
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://sgbau.ucanapply.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://sgbau.ucanapply.com/result-details',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

data = {
    '_token': token,
    'session': 'SE20',
    'COURSETYPE': 'UG',
    'COURSECD': 'C000037',
    'RESULTTYPE': 'R',
    'p1': '',
    'ROLLNO': '23BG310401',
    'SEMCODE': 'SM04',
    'all': '',
}

print(token)
