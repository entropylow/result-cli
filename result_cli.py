from lxml import html
import sys, requests, bs4

# variables
variables = {
    'session_code'  : '',
    'course_type'   : '',
    'course_number' : '',
    'result_type'   : '',
    'roll_number'   : '',
    'semester_code' : '',
}

# fill the variables dictionary using command line arguments
n = 1
for key in variables.keys():
    if n < len(sys.argv):
        variables[key] = sys.argv[n].strip()
        n += 1
    else:
        break

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
    'session': variables['session_code'],    # 'SE20'
    'COURSETYPE': variables['course_type'],  # 'UG'
    'COURSECD': variables['course_number'],  # 'C000037'
    'RESULTTYPE': variables['result_type'],  # 'R'
    'p1': '',
    'ROLLNO': variables['roll_number'],      # '23BG310401'
    'SEMCODE': variables['semester_code'],   # 'SM04'
    'all': '',
}

# submitting the data
post_url = 'https://sgbau.ucanapply.com/get-result-details'
result_response = session.post(post_url, headers=headers, data=data)

# save the file on hard drive
# file = open('result_page.html', 'wb')
# for chunk in result_response.iter_content(10000000):
#     file.write(chunk)
# file.close()

# extracting name and sgpa
result_html = html.fromstring(result_response.content)

sgpa_list = result_html.xpath("//td[contains(text(), 'SGPA')]/following-sibling::td")
if sgpa_list:
    sgpa_unfiltered = sgpa_list[0].text_content().strip()
else:
    sgpa = 'FAIL'
sgpa = float(''.join(value if value.isdigit() or value == '.' else '' for value in sgpa_unfiltered))

name_list = result_html.xpath("//td[contains(text(), 'Name')]/following-sibling::td[2]")
name_unfiltered = name_list[0].text_content().strip()
name = ' '.join(name_unfiltered.split()[:3])

# print the collected data
print(f'{name} : {sgpa}')
