from lxml import html
import argparse, requests, bs4

def get_input():
    """take the input from command line arguments"""
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
    return args

def create_session():
    """create a session for the current request"""
    session = requests.Session()
    return session

def get_response(url, session):
    """get the html data for the current session"""
    input_response = session.get(url)
    return input_response
    
def extract_token(input_response):
    """extract the token from the html data"""
    input_soup = bs4.BeautifulSoup(input_response.content, 'html.parser')
    token = input_soup.find('input', {'name': '_token'}).get('value')
    return token

def post_response(post_url, args, token):
    """get the result by submiting the data"""
    # the headers and data dictionaries 
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
    
    # submit the data
    result_response = session.post(post_url, headers=headers, data=data)
    return result_response

def extract_data(result_response):
    """extract name and sgpa from the resultant html"""
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
    
    return name, sgpa

if __name__ == '__main__':
    url = 'https://sgbau.ucanapply.com/result-details'
    post_url = 'https://sgbau.ucanapply.com/get-result-details'
            
    args = get_input()
    session = create_session()
    input_response = get_response(url, session)
    token = extract_token(input_response)
    result_response = post_response(post_url, args, token)
    name, sgpa = extract_data(result_response)

    # print the collected data
    print(f'{name} : {sgpa}')
