from lxml import html
import bs4, argparse, json
import asyncio, aiohttp
from tqdm.asyncio import tqdm

def read_command_line_input():
    """takes input from command line arguments"""
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

def extract_token(base_response_text):
    """extracts token from the html data"""
    base_soup = bs4.BeautifulSoup(base_response_text, 'html.parser')
    token = base_soup.find('input', {'name': '_token'}).get('value')
    return token

def extract_name_and_spga(post_response_text):
    """extracts name and sgpa from the resultant html"""
    post_html = html.fromstring(post_response_text)
    
    name_list = post_html.xpath("//td[contains(text(), 'Name')]/following-sibling::td[2]")
    if name_list:
        name_unfiltered = name_list[0].text_content().strip()
        name = ' '.join(name_unfiltered.split()[:3])
        if not name.replace(" ","").isalnum():
            name = ' '.join(name_unfiltered.split()[:2])
    else:
        name = 'error'
    
    sgpa_list = post_html.xpath("//td[contains(text(), 'SGPA')]/following-sibling::td")
    if sgpa_list:
        sgpa_unfiltered = sgpa_list[0].text_content().strip()
        sgpa = float(''.join(value if value.isdigit() or value == '.' else '' for value in sgpa_unfiltered))
    elif (name=='error'):
        sgpa = 'result does not exist'
    else:
        sgpa = 'FAIL'

    return name, sgpa

def prepare_headers_dict(token):
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
    return headers

def prepare_data_dict(token, roll):
    data = {
        '_token': token,
        'session': 'SE' + args.session,    # '20'
        'COURSETYPE': args.course,         # 'UG'
        'COURSECD': 'C0000' + args.code,   # '37'
        'RESULTTYPE': args.type,           # 'R'
        'p1': '',
        'ROLLNO': roll,                    # '23BG310401'
        'SEMCODE': 'SM0' + args.semester,  # '4'
        'all': '',
    }
    return data

def save_output_data():
    with open('result.json', 'w') as file:
        json.dump(sorted(output_data.items()), file, indent=4)
    print("\nData saved in the current directory as 'result.json'\n")

def prepare_roll_list():
    """generates a roll list from start roll to end roll"""
    roll_list = range(int(''.join(list(args.start)[-3:])), int(''.join(list(args.end)[-3:])) + 1)
    prefix = ''.join(list(args.start)[:7])
    
    return roll_list, prefix 

async def post_and_parse(session, token, roll):
    """makes post request and extracts name and sgpa"""
    data = prepare_data_dict(token, roll)
    async with session.post(POST_URL, data=data) as post_response:
        post_response_text = await post_response.text()
        name, sgpa = extract_name_and_spga(post_response_text)
        output_data[roll] = f"{name} : {sgpa}"

async def main():
    """creates the session, extracts token and awaits post_and_parse coroutine object"""
    async with aiohttp.ClientSession() as session:
        try:        
            async with session.get(BASE_URL, raise_for_status=True) as base_response:
                base_response_text = await base_response.text()

                token = extract_token(base_response_text)
                roll_list, prefix = prepare_roll_list()
                session.headers.update(prepare_headers_dict(token))

                coroutines = [(post_and_parse(session, token, prefix + str(f"{suffix:03d}"))) for suffix in roll_list]
                await tqdm.gather(*coroutines)
        
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message}")
        
        except aiohttp.ClientError as e:
            print(f"Request error occurred: {e}")

if __name__ == '__main__':
    BASE_URL = "https://sgbau.ucanapply.com/result-details"
    POST_URL = "https://sgbau.ucanapply.com/get-result-details"
    
    output_data = {}
    args = read_command_line_input()
    
    print("\nDownloading the requested data...\n")
    asyncio.run(main())
    
    save_output_data()
