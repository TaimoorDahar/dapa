import json
from flask import Flask, request, render_template
import requests
from fake_useragent import UserAgent

ua = UserAgent()
random_user_agent = ua.random
app = Flask(__name__)

def login_auth():
    url = "https://moz.com/app-api/jsonrpc"

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
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'ajs_anonymous_id=86847119-7505-444d-8f1b-62021d6ac042; hubspotutk=158388b424a7af5554e74bf791938145; __stripe_mid=89478b88-a8df-41ba-95e0-889618d572c164f4f5; ajs_user_id=18870361; ajs_group_id=20880309; _ga_DS7K9Q3S5W=GS1.1.1704184204.21.0.1704184212.0.0.0; _ga_QLCPR2NDVP=GS1.1.1705826255.25.0.1705826255.0.0.0; _ga_LGQZKGRBE5=GS1.1.1705826075.24.1.1705826255.60.0.0; opt_out=1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Feb+01+2024+21%3A42%3A24+GMT%2B0500+(Pakistan+Standard+Time)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=69438842-69f7-44fe-b955-671e7b3f33b0&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A0%2CC0005%3A0%2CC0002%3A0%2CC0003%3A0%2CV2STACK42%3A0&genVendors=&AwaitingReconsent=false; _CEFT=Q%3D%3D%3D; _uetvid=2bca95e086a711ee84c2c716a9c38975; _gcl_au=1.1.1505053673.1714297957; _rdt_uuid=1714297960919.9eae42bd-2767-479a-905d-d043b8877c74; cf_clearance=zHZ99X1iYQwAvh.ldqWA9WMW8Iq79v1iG2gPY9QHgNA-1714297968-1.0.1.1-BhluVsdLFwcj8c5Sdcx0ktXVOGq6TPF6L_ul7YjwXKYFpJW_D_CM7ok9vLhw.Nxudw8UayILUoYACZ762qh18Q; __cf_bm=Sh1mPoyx0j8gYcsyvlQ16SbjhGJ1ncactgqfKJuEuhU-1715242595-1.0.1.1-Xx3ll.aVA3j.BU5L7W.kcoBU3821yJWB8cAoUO5D4_bV3g65Kptayx.263CuMauGqMjSMaMQ7HCZTxdV0h.J4Q; _gid=GA1.2.1761423463.1715242627; _ce.irv=returning; cebs=1; _ce.clock_event=1; _ce.clock_data=529%2C110.37.41.139%2C1%2Cb78b4e2d6c0a362c418b145fe44ed73f; _moz_csrf=c1b5ee49750d5232fe2171bf07873460bd9ef7fc; __hstc=103427807.158388b424a7af5554e74bf791938145.1700376308078.1714297962361.1715242644841.29; __hssrc=1; __stripe_sid=869b48a5-db45-436f-97a8-192f07d31d427e5202; cf_clearance=u53dtwKHIIJVAQWeD514wxo3KnIrZWPEBd1Q_LDq.ic-1715242702-1.0.1.1-YuXXOKrxf8EhOxKNvBA19If.cpzcNpCbA.kfLroOzIIYPmxg8ZA_.cHHX4qf2i1owILNNISuSKrAYlm9ruXnCA; _ga=GA1.2.1739970936.1715242731; _gat=1; cebsp_=5; __hssc=103427807.4.1715242644841; _ce.s=v~9c14dd412831af1b1872aa87db6c08fe83df1dcb~lcw~1715243000554~lva~1715242639822~vpv~8~v11.fhb~1715242682883~v11.lhb~1715242993811~as~false~v11.cs~438892~v11.s~8fa00590-0ddc-11ef-90a1-115609bc10ea~v11.sla~1715243000549~gtrk.la~lvyze9mw~lcw~1715243000650; __cf_bm=2TBgqeA0qZWhouDFTcjoavyVbxDCHoRwg4D19K93wlc-1716836537-1.0.1.1-qgzz2NtFhTAJP.EO6tU35PZsdiNnEse95Kg2otI771feiMPPOBMSlSJ2Gxs8XzfSU00xZG5qKteugf81hesURw; _moz_csrf=c1b5ee49750d5232fe2171bf07873460bd9ef7fc; mozauth=U6brZ9QKisXeFTLTnNYyCQhaAWoYETQ2Seqxi6NuaEG0xiermo0GkEWQiR0mLrqK',
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

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True

@app.route('/', methods=['POST'])
def process():
    text_data = request.form['textArea']
    links = text_data.split()
    url = "https://mozbar.moz.com/bartender/url-metrics"

    payload = json.dumps(links)
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=UTF-8',
        'cookie': '_moz_csrf=c1b5ee49750d5232fe2171bf07873460bd9ef7fc; __cf_bm=7cXFe6WmRXbekiTPUwoyDbPOTtdhjXCFO73OnkU2ASY-1716665909-1.0.1.1-zFi6_kRuGNiLamQx.LONrAcvrkqnsl0gcf5PhGnSix8xOzptPnD2kDEhshtVFZRJTLEQ0B.XJJ6mtkUQHzIbrg; ajs_anonymous_id=38750a7a-a42b-4046-8456-3c10956227cc; _gid=GA1.2.12856458.1716665912; _gcl_au=1.1.545002049.1716665912; _ce.irv=new; cebs=1; _ce.clock_event=1; __hstc=103427807.ade4407bbcafa81ec29deed2e956f16d.1716665913443.1716665913443.1716665913443.1; hubspotutk=ade4407bbcafa81ec29deed2e956f16d; __hssrc=1; _ce.clock_data=115%2C110.37.41.139%2C1%2Cd72690806e05ab108412ee33b4c5c3e1%2CChrome%2CPK; _CEFT=Q%3D%3D%3D; __stripe_mid=513dc677-64b0-41f4-b99f-c6bc18c4fe7ec465c3; __stripe_sid=6397ae5d-4935-4369-8dc9-2a3775e601d10715fb; mozauth=ZOPWYOniTUeFXhTJIqoCWtM5QRF3alGwgxwqM4ZHT1EIXyNzxwrSrTJ002vr0TSb; _ga_QLCPR2NDVP=GS1.1.1716665917.1.0.1716665925.0.0.0; ajs_user_id=18870361; ajs_group_id=20880309; _uetsid=5e6454a01ace11ef9ac7571b0846882f; _uetvid=5e648fa01ace11ef9ee44f50651fb907; _rdt_uuid=1716665912972.4d53d4e3-3a8b-49ca-a540-f45dfbb6e26c; cebsp_=3; _ga_LGQZKGRBE5=GS1.1.1716665912.1.1.1716665926.46.0.0; _ga_DS7K9Q3S5W=GS1.1.1716665914.1.1.1716665927.0.0.0; _ga=GA1.1.1112778104.1716665912; __hssc=103427807.3.1716665913443; _ce.s=v~586c73bf6984dcad2961b5d3583995c2b11c56c1~lcw~1716665964536~lva~1716665913055~vpv~0~v11.fhb~1716665914041~v11.lhb~1716665926800~v11.cs~438892~v11.s~5f8ce8b0-1ace-11ef-babb-ad8d6cb445b9~v11.sla~1716665966465~gtrk.la~lwmikpwr~lcw~1716665966465; __cf_bm=hjT7emo5sOpGZbcfkUKjGghxqltUYQIfNKpExhFO_5Q-1716665979-1.0.1.1-WwM9Kak.gHNLbWvsqcPGzeTU2r3mYFCYn0IymQf8O2ympFTmiKgj9d0FB4xiAupr6aMO9vVvWqC9rfbu5MsKAQ; __cf_bm=2TBgqeA0qZWhouDFTcjoavyVbxDCHoRwg4D19K93wlc-1716836537-1.0.1.1-qgzz2NtFhTAJP.EO6tU35PZsdiNnEse95Kg2otI771feiMPPOBMSlSJ2Gxs8XzfSU00xZG5qKteugf81hesURw; _moz_csrf=c1b5ee49750d5232fe2171bf07873460bd9ef7fc; mozauth=U6brZ9QKisXeFTLTnNYyCQhaAWoYETQ2Seqxi6NuaEG0xiermo0GkEWQiR0mLrqK; __cf_bm=oTbU_h5hIRL.GnxBCZcONF8irrCPPQ0Dvkjd8nIovi4-1716838263-1.0.1.1-hm_dQWYtUu4jnpstfTL8rOEJjaMpoN5_4YtRXrWsgcyqUpGxjvWmuooKJW1UAcad8n5jcMypWRXwka9Bq6h5JQ',
        'origin': 'chrome-extension://eakacpaijcpapndcfffdgphdiccmpknp',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'none',
        'user-agent': random_user_agent,
        'x-bartender-version': '2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status == 401:
        login_auth()
        response = requests.request("POST", url, headers=headers, data=payload)

    response_data = response.json()  # Parse the JSON response

    return render_template('index.html', response=response_data, links=links)

@app.route('/')
def index():
    return render_template('index.html', response=[], links=[])

if __name__ == "__main__":
    app.run(debug=True)
