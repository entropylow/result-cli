from lxml import html
import requests, bs4

# getting the html data from the website
url = 'https://sgbau.ucanapply.com/result-details'
session = requests.Session()
input_response = session.get(url)

# extracting token from the page
input_soup = bs4.BeautifulSoup(input_response.content, 'html.parser')
token = input_soup.find('input', {'name': '_token'}).get('value')

# implementing headers and data dictionary
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

# submitting the data
post_url = 'https://sgbau.ucanapply.com/get-result-details'
result_response = session.post(post_url, headers=headers, data=data)

result_soup = bs4.BeautifulSoup(result_response.content, 'html.parser')

# save the file on hard drive
# file = open('result_page.html', 'wb')
# for chunk in result_page.iter_content(10000000):
#     file.write(chunk)
# file.close()


# extracting name and sgpa
result_html = html.fromstring(result_response.content)

sgpa_list = result_html.xpath("//td[contains(text(), 'SGPA')]/following-sibling::td")

if sgpa_list:
    sgpa_unfilterd = sgpa_list[0].text_content().strip()
else:
    sgpa = 'FAIL'

sgpa = float(''.join(value if value.isdigit() or value == '.' else '' for value in sgpa_unfilterd))


name_list = result_html.xpath("//td[contains(text(), 'Name')]/following-sibling::td[2]")
name_unfilterd = name_list[0].text_content().strip()
name = ' '.join(name_unfilterd.split()[:3])

# print the collected data
print(f'{name} : {sgpa}')
