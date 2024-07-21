import json
from flask import Flask, request, render_template,jsonify
import requests
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET
from flask_cors import CORS
from urllib.parse import urlparse

ua = UserAgent()
random_user_agent = ua.random
app = Flask(__name__)
CORS(app)

# Define the custom filter
def intcomma(value):
    return "{:,}".format(value)

# Register the filter
app.jinja_env.filters['intcomma'] = intcomma


session_cookies = None

def get_csrf_token(session):
    url = "https://moz.com/login"
    response = session.get(url)
    # You need to parse the response to extract the CSRF token. 
    # This will depend on how the token is embedded in the HTML.
    # Assuming the token is in a meta tag like <meta name="csrf-token" content="...">
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
    return csrf_token

def login_auth():
    global session_cookies
    url = "https://moz.com/app-api/jsonrpc"
    session = requests.Session()
    
    csrf_token = get_csrf_token(session)

    payload = json.dumps({
        "id": "d28c58d9-f1f5-44ef-8e8f-10c055e557d5",
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "data": {
                "email": "musefoka@ryteto.me",
                "password": "iPxbgjVM*Xu4uh9"
            }
        }
    })
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'cookie': f'csrf_token={csrf_token}',  # Include the CSRF token in the cookies or headers as required
        'dpr': '1',
        'origin': 'https://moz.com',
        'priority': 'u=1, i',
        'referer': 'https://moz.com/login',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': random_user_agent,
        'viewport-width': '1280'
    }

    response = session.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        session_cookies = response.cookies
        return True
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
    return False

@app.route('/', methods=['POST'])
def process():
    global session_cookies

    text_data = request.form['textArea']
    links = text_data.split()
    url = "https://mozbar.moz.com/bartender/url-metrics"
    links = links[:10]
    payload = json.dumps(links)
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': random_user_agent,
        'origin': 'chrome-extension://eakacpaijcpapndcfffdgphdiccmpknp',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'none',
        'x-bartender-version': '2'
    }

    if not session_cookies:
        if not login_auth():
            return "Login failed"

    response = requests.post(url, headers=headers, cookies=session_cookies, data=payload)

    if response.status_code == 401:
        if login_auth():
            response = requests.post(url, headers=headers, cookies=session_cookies, data=payload)
        else:
            return "Login failed"

    if response.status_code != 200:
        print(f"Request failed: {response.status_code} - {response.text}")
        return f"Request failed: {response.status_code}"

    try:
        response_data = response.json()
        for i, domain in enumerate(links):
            if i < len(response_data):
                response_data[i]['domain'] = domain
    except json.JSONDecodeError:
        print(f"JSON decode error: {response.text}")
        return f"Failed to decode JSON response: {response.text}"

    return render_template('index.html', response=response_data, links=links)

@app.route('/')
def index():
    return render_template('index.html', response=[], links=[])



def token_auth():

    url = "https://app.neilpatel.com/api/get_token?debug=app_norecaptcha"

    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'mutiny.user.token=927ed82b-3eea-496b-a8bb-9cbbbfb01398; _vwo_uuid_v2=D7CC0651439E8CF8D7A0280EDA53118D1|bc1427bd640a33470c8a9a11fa5de447; _gid=GA1.2.543291984.1715717916; __cf_bm=941R9aQTLLtN4EvJqpAbAJBEoZJVD5JnU7nHzwn6rdA-1715747598-1.0.1.1-bJsIA3urhlvB6EUDXxfsRDY_lbt40r7Cy3CGg0hvZ6KbmJzWj3.lVjeJZEg__aUjrnItrDnpqKQQxkmcwQiV4w; mutiny.user.session=089be544-113d-4ca6-a15b-704f9eb3519f; mutiny.user.session=089be544-113d-4ca6-a15b-704f9eb3519f; mutiny.user.session_number=2; mutiny.user.session_number=2; km_vs=1; km_ni=muhammadtaimur142%40gmail.com; _clck=15j6jkw%7C2%7Cfls%7C0%7C1596; _tt_enable_cookie=1; _ttp=irSwq_wsJb3Ca0eXo_JWkH_1Zj9; _gcl_au=1.1.1588408342.1715747658; __hstc=240018588.2cc88398044e1d07a0b63a14eaae8478.1715747658524.1715747658524.1715747658524.1; hubspotutk=2cc88398044e1d07a0b63a14eaae8478; __hssrc=1; __zlcmid=1LmmifXMDkRutC3; _gat_UA-16137731-1=1; _uetsid=23ada280122f11ef82968905aacb502f; _uetvid=23ae9cb0122f11ef92fab31b2018b3bc; _ga=GA1.2.491695115.1715717913; __hssc=240018588.2.1715747658526; _clsk=hxdeu%7C1715747818832%7C5%7C1%7Cv.clarity.ms%2Fcollect; state="eyJuZXh0IjoiL2VuL3RyYWZmaWNfYW5hbHl6ZXIvb3ZlcnZpZXc_ZG9tYWluPWtlZHVwbGljYXRlYmlsbC5jb20ucGsmbGFuZz1lbiZsb2NJZD0yODQwJm1vZGU9ZG9tYWluIiwicmVmZXJyZXJfaG9zdCI6Imh0dHBzOi8vYXBwLm5laWxwYXRlbC5jb20ifQ=="; id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTA4Nzk5Njc3NjM5ODU0MjE1MDgzIiwiZXhwIjoxNzE1OTIwNjMwfQ.qksSjWuQCPA1mFIIPwLkyedfMjlmCNJjdDU7SSgIUik; _ga_6QNYJFNF1D=GS1.1.1715747649.2.1.1715747831.20.0.0; _ga_PE1RZ8MRZD=GS1.1.1715747649.2.1.1715747831.19.0.0; kvcd=1715747835791; km_lv=1715747836; amp_276990=MfUpfNsQ75JylxQ_e0S6va.MTA4Nzk5Njc3NjM5ODU0MjE1MDgz..1htt8ept8.1htt8khqp.2.0.2; km_ai=muhammadtaimur142%40gmail.com; mp_0f47aae0dbedc03b9054b3be104ea557_mixpanel=%7B%22distinct_id%22%3A%20%22muhammadtaimur142%40gmail.com%22%2C%22%24device_id%22%3A%20%2218f7a8767f7ad1-0ffcea1c8e10f9-76574611-1fa400-18f7a8767f7ad1%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fneilpatel.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22neilpatel.com%22%2C%22%24user_id%22%3A%20%22muhammadtaimur142%40gmail.com%22%7D',
        'priority': 'u=1, i',
        'referer': 'https://app.neilpatel.com/en/traffic_analyzer/overview?domain=keduplicatebill.com.pk&lang=en&locId=2840&mode=domain',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': random_user_agent,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = response.json()
    token = response_data['token']
    return token


@app.route('/keyword-volume/', methods=['POST'])
def keyword_process():
    keyword = request.form['keyword']
    import requests

    url = f"https://app.neilpatel.com/api/keyword_info?keyword={keyword}&language=en"
    token = token_auth()
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {token}',
    'cookie': 'lifetime_offer_until=2024-05-17T12:16:26+00:00; mutiny.user.token=8df08f9d-50da-4fdd-b2a5-a5d5d58976d0; _vwo_uuid_v2=DAE5A4348F2C27F5020B3F5683F2A94F3|5233b40431339d98d245162cb5e79bbb; __cf_bm=jvVFSvQsScK3Xv49xMlWt4bdlssH885QP5kTf97uy8k-1720545455-1.0.1.1-agx.il_ZJCKkmkZNMbwYCSVdRvHH64_2YzxnUVsatDuW4.ZvibOrjtwoaUZr3mmJaKSEHKrC3S1o61chGCoFpQ; mutiny.user.session=505a831b-4bec-49cd-8252-95e458d1591d; mutiny.user.session_number=3; _gid=GA1.2.1685844522.1720545462; _gat_UA-16137731-1=1; km_ai=BML%2F3ntIZUfO0TdECxJxcxBstxo%3D; km_vs=1; _tt_enable_cookie=1; _ttp=hfMSqhXEhr-ZoALlsl4Su1mJ5L6; _clck=3k1wxa%7C2%7Cfnb%7C0%7C1651; __zlcmid=1Mfmr7Eu2m4RA4l; mutiny.user.session_number=3; _gcl_au=1.1.9063481.1720545470; state="eyJuZXh0IjoiaHR0cHM6Ly9hcHAubmVpbHBhdGVsLmNvbS9lbi9sb2dpbiIsInJlZmVycmVyX2hvc3QiOiJodHRwczovL2FwcC5uZWlscGF0ZWwuY29tIn0="; id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTA4Nzk5Njc3NjM5ODU0MjE1MDgzIiwiZXhwIjoxNzIwNzE4Mjc0fQ.BhPr5i3TkYE8V5R7NvaJHr7xhTHdHvXLU9Zr4svfyuA; __hstc=240018588.f621e2eb29267bc53b98ae8879270427.1720545476009.1720545476009.1720545476009.1; hubspotutk=f621e2eb29267bc53b98ae8879270427; __hssrc=1; kvcd=1720545476667; km_lv=1720545477; _uetsid=26e980803e1711ef913935337d7f4ff4; _uetvid=f7894e80190811efb01e9786734665e6; _ga=GA1.2.2080131192.1716471178; __hssc=240018588.2.1720545476009; km_ni=muhammadtaimur142%40gmail.com; mp_0f47aae0dbedc03b9054b3be104ea557_mixpanel=%7B%22distinct_id%22%3A%20%22muhammadtaimur142%40gmail.com%22%2C%22%24device_id%22%3A%20%2219098806460868-09c71270bab59e-11462c6f-140000-19098806460868%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fapp.neilpatel.com%2Fen%2Flogin%22%2C%22%24initial_referring_domain%22%3A%20%22app.neilpatel.com%22%2C%22%24user_id%22%3A%20%22muhammadtaimur142%40gmail.com%22%7D; amp_276990=9u5VaQGtmMmkT1R0Luao1D.MTA4Nzk5Njc3NjM5ODU0MjE1MDgz..1i2c80k32.1i2c81ce6.2.0.2; _clsk=o0iei3%7C1720545490607%7C3%7C1%7Co.clarity.ms%2Fcollect; _ga_6QNYJFNF1D=GS1.1.1720545462.3.1.1720545521.1.0.0; _ga_PE1RZ8MRZD=GS1.1.1720545461.3.1.1720545521.60.0.0',
    'priority': 'u=1, i',
    'referer': 'https://app.neilpatel.com/en/ubersuggest/overview?ai-keyword=deezer%20premium%20apk&keyword=deezer%20premium%20apk&lang=en&locId=0000&mode=keyword',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'ts': '1720545521',
    'user-agent': random_user_agent
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Request failed: {response.status_code} - {response.text}")
        return f"Request failed: {response.status_code}"

    try:
        response_data = response.json()
        keyword_info = response_data['keywordInfo']
    except json.JSONDecodeError:
        print(f"JSON decode error: {response.text}")
        return f"Failed to decode JSON response: {response.text}"

    return render_template('keyword-volume.html', keyword_info=keyword_info)


@app.route('/keyword-volume/')
def keywords():
    return render_template('keyword-volume.html', response=[], links=[])


@app.route('/semrush-bulk/', methods=['GET'])
def semrush_bulk():
    return render_template('semrush.html')


@app.route('/check_domains', methods=['POST'])
def check_domains():
    domains = request.form.get('domains').split()
    results = []

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'ref_code=__default__; refer_source=""; cookiehub=eyJhbnN3ZXJlZCI6ZmFsc2UsInJldmlzaW9uIjoxLCJkbnQiOmZhbHNlLCJhbGxvd1NhbGUiOnRydWUsImltcGxpY3QiOnRydWUsInJlZ2lvbiI6IkcwIiwidG9rZW4iOiJEeWdhSGMzM0dlcWlTUTNqNGVtSTBrRmQ0a3VzSDJnemw0QWdwREl0SFd4REZLRzE3ekV1V2E1bXRsU2M0ajJLIiwidGltZXN0YW1wIjoiMjAyMy0xMS0yN1QxNDo1Mjo1NC43NjhaIiwiYWxsQWxsb3dlZCI6dHJ1ZSwiY2F0ZWdvcmllcyI6W10sInZlbmRvcnMiOltdLCJzZXJ2aWNlcyI6W119; _mkto_trk=id:519-IIY-869&token:_mch-semrush.com-1701096776566-16378; _tt_enable_cookie=1; _ttp=R-npYYfWtZMXs46e4eWjhV0NPpr; PHPSESSID=815b81b3d946c7f93e4e554a1101d5cd; SSO-JWT=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTViODFiM2Q5NDZjN2Y5M2U0ZTU1NGExMTAxZDVjZCIsImlhdCI6MTcwMTA5Njc4NiwiaXNzIjoic3NvIiwidWlkIjoxODI0MTUzOH0.Mr14ut2ZfYenpO3TVPpgs_oTc9G5aoWIsljnpUJvdSWptumSoEmtZ3pqUc0qZwNYoLsPe2UZ4gKjNb1kCOVp8Q; sso_token=b6df251f6ec10a5fa4640ee2fef15938fd87cd3822e5e9c4ff261fc22eb49e96; _uetvid=a6009fc08d3411ee8e29271c28c3a2e0|3tasoo|1701096794111|2|1|bat.bing.com/p/insights/c/o; _ga_HYWKMHR981=GS1.1.1701096774.1.1.1701096796.39.0.0; _ga_BPNLXP3JQG=GS1.1.1701096774.1.1.1701096796.0.0.0; _ga=GA1.2.1013714350.1701096775',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'none',
        'user-agent': random_user_agent,
    }

    for domain in domains:
        url = f"https://seoquake.publicapi.semrush.com/info.php?url={domain}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            data = {
                'domain': domain,
                'keywords': root.findtext('keywords'),
                'traffic': root.findtext('traffic'),
                'costs': root.findtext('costs'),
                'rank': root.findtext('rank'),
            }
            results.append(data)
        else:
            results.append({'domain': domain, 'error': 'Failed to fetch data'})
    
    return render_template('results.html', results=results)


def get_similarweb_data(domain):
    
    if not domain:
        return jsonify({'error': 'Domain parameter is required'}), 400
    
    url = f"https://data.similarweb.com/api/v1/data?domain={domain}"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'none',
        'user-agent': random_user_agent,
        'x-extension-version': '6.11.5'
    }

    params = {
        'domain': domain
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code


@app.route('/domain-overview/', methods=['GET', 'POST'])
def domain_overview():
    if request.method == 'POST':
        domain = request.form.get('domain')
        if not domain:
            return jsonify({'error': 'No domain provided'}), 400

        url = f"https://app.neilpatel.com/api/backlinks_overview?domain={domain}&mode=domain"
        token = token_auth()  # Assuming token_auth() is defined elsewhere and returns a valid token
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {token}',
            'user-agent': random_user_agent,
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Request failed: {response.status_code} - {response.text}")
            return f"Request failed: {response.status_code}"

        try:
            response_data = response.json()
           
        except json.JSONDecodeError:
            print(f"JSON decode error: {response.text}")
            return f"Failed to decode JSON response: {response.text}"

        return render_template('domain_overview.html', domain_info=response_data)
    
    return render_template('domain_overview.html')


def format_number(number):
    """Formats a number with commas or abbreviates it."""
    if number >= 1_000_000:
        return f"{number // 1_000_000}M"
    elif number >= 1_000:
        return f"{number // 1_000}K"
    else:
        return str(number)
# Domain OverView API
@app.route('/api-domain-overview/', methods=['POST'])
def domain_overview_api():
    alldata = {}
    data = request.get_json()
    url = data.get('domain')
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if not domain:
        return jsonify({'error': 'No domain provided'}), 400

    url = f"https://app.neilpatel.com/api/backlinks_overview?domain={domain}&mode=domain"
    token = token_auth()
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'user-agent': random_user_agent,
    }

    response = requests.get(url, headers=headers)
    moz_data = response.json()


    if response.status_code != 200:

        print(f"Request failed: {response.status_code} - {response.text}")
        return jsonify({'error': f"Request failed: {response.status_code}", 'message': response.text}), response.status_code

    try:
        alldata = {
            'da': format_number(moz_data['domainAuthority']),
            'backlinks': format_number(moz_data['backlinks']),
            'refDomains': format_number(moz_data['refDomains']),
        }
        similarweb_data = get_similarweb_data(domain)
        similarweb_data = similarweb_data.data
        decoded_data = similarweb_data.decode('utf-8')
        similarweb_data = json.loads(decoded_data)
        alldata.update({
            'top_keywords': similarweb_data.get('TopKeywords', []),
            'EstimatedMonthlyVisits': similarweb_data.get('EstimatedMonthlyVisits', {}),
            'TrafficSources': similarweb_data.get('TrafficSources', {}),
        })
    except json.JSONDecodeError:
        print(f"JSON decode error: {response.text}")
        return jsonify({'error': 'Failed to decode JSON response', 'message': response.text}), 500

    return jsonify(alldata)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8003)
