from lxml import html
import argparse, requests, bs4

# taking input from command line args 
add_args = {
    'session'  : {'required' : True, 'help' : '17:W22, 18:S23, ... , 21:W24'},
    'course'   : {'required' : True, 'help' : 'UG/PG/PHD'},
    'code'     : {'required' : True, 'help' : 'CSE:32/ENTC:37/IT:39/MECH:41/ELPO:43/firstYear:48'},
    'type'     : {'required' : True, 'help' : 'R/B/RV/EV'},
    'roll'     : {'required' : True, 'help' : 'roll number'},
    'semester' : {'required' : True, 'help' : '1, 2, 3 ...'},
}

parser = argparse.ArgumentParser()

# the simple way (without loop)
# parser.add_argument('--session', required=True, help='17:W22, 18:S23, ... , 21:W24')
# parser.add_argument('--course', required=True, help='UG/PG/PHD')
# ... 

for arg, values in add_args.items():
    parser.add_argument(f'--{arg}', **values)
    
args = parser.parse_args()

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
    'session': 'SE' + args.session,    # '20'
    'COURSETYPE': args.course,         # 'UG'
    'COURSECD': 'C0000' + args.code,   # '37'
    'RESULTTYPE': args.type,           # 'R'
    'p1': '',
    'ROLLNO': args.roll,               # '23BG310401'
    'SEMCODE': 'SM0' + args.semester,  # '4'
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
    sgpa = float(''.join(value if value.isdigit() or value == '.' else '' for value in sgpa_unfiltered))
else:
    sgpa = 'FAIL'

name_list = result_html.xpath("//td[contains(text(), 'Name')]/following-sibling::td[2]")
name_unfiltered = name_list[0].text_content().strip()
name = ' '.join(name_unfiltered.split()[:3])

# print the collected data
print(f'{name} : {sgpa}')
