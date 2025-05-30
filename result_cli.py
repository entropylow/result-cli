from lxml import html
import argparse, requests, bs4

def get_input():
    """take the input from command line arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--session', required=True, help='17:W22, 18:S23, ... , 21:W24')
    parser.add_argument('--course', required=True, help='UG/PG/PHD')
    parser.add_argument('--code', required=True, help='CSE:32/ENTC:37/IT:39/MECH:41/ELPO:43/firstYear:48') 
    parser.add_argument('--type', required=True, help='R/B/RV/EV') 
    parser.add_argument('--start', required=True, help='start roll number') 
    parser.add_argument('--end', required=True, help='end roll number') 
    parser.add_argument('--semester', required=True, help='1, 2, 3, ...') 

    args = parser.parse_args()
    return args

def create_session():
    """create a session object that will preserve the cookies and the TCP connection"""
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

def fill_missing_fields(args, token):
    """completes the dictionaries"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3',
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
        'ROLLNO': '',               # '23BG310401'
        'SEMCODE': 'SM0' + args.semester,  # '4'
        'all': '',
    }
    return headers, data

def post_response(post_url, session, data):
    """get the result by submiting the data"""
    result_response = session.post(post_url, data=data)
    return result_response

def extract_data(result_response):
    """extract name and sgpa from the resultant html"""
    result_html = html.fromstring(result_response.content)
    
    name_list = result_html.xpath("//td[contains(text(), 'Name')]/following-sibling::td[2]")
    if name_list:
        name_unfiltered = name_list[0].text_content().strip()
        name = ' '.join(name_unfiltered.split()[:3])
    else:
        name = 'error'
    
    sgpa_list = result_html.xpath("//td[contains(text(), 'SGPA')]/following-sibling::td")
    if sgpa_list:
        sgpa_unfiltered = sgpa_list[0].text_content().strip()
        sgpa = float(''.join(value if value.isdigit() or value == '.' else '' for value in sgpa_unfiltered))
    elif (name=='error'):
        sgpa = 'result does not exist'
    else:
        sgpa = 'FAIL'

    return name, sgpa

def prepare_post():
    """prepare the data for the post requests"""
    url = 'https://sgbau.ucanapply.com/result-details'
            
    args = get_input()
    session = create_session()
    input_response = get_response(url, session)
    token = extract_token(input_response)
    headers, data = fill_missing_fields(args, token)
    session.headers.update(headers)

    return session, args, data

def fetch_result(session, args, data):
    """prints name and sgpa for a given range"""
    post_url = 'https://sgbau.ucanapply.com/get-result-details'

    start = int(''.join(list(args.start)[-3:]))
    end = int(''.join(list(args.end)[-3:]))
    prefix = ''.join(list(args.start)[:7])

    for roll in range(start, end + 1):
        data['ROLLNO'] = prefix + str(roll)
        result_response = post_response(post_url, session, data)
        name, sgpa = extract_data(result_response)
        print(f'{name} : {sgpa}')
    
    return None

if __name__ == '__main__':
    session, args, data = prepare_post()
    fetch_result(session, args, data)
