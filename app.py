from flask import Flask, render_template, request, send_file,jsonify
import requests
import pandas as pd
app = Flask(__name__)
import json
from fake_useragent import UserAgent
ua = UserAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process():
    # Get data from the form
    # Get data from the form textarea and remove line breaks
    text_data = request.form['textArea']
    links = text_data.split()
    # Define the chunk size
    chunk_size = 10

    # List to store chunks of data
    chunked_data = []

    # Loop through the data in chunks
    for i in range(0, len(links), chunk_size):
        # Get the current chunk of items
        chunk = links[i:i + chunk_size]

        # Append the chunk to the new_items list


        # Join the links with '&' operator
        links_pairs = [f'links%5B%5D={link}' for link in chunk]
        payload = {
            'links[]': links_pairs,
            'url': 0,
            'domain': 0,
            'tool_id': 1,
            'parent_id': 1
        }

        # Manually format the payload string
        payload_string = '&'.join(
            payload['links[]'] + [f'url={payload["url"]}', f'domain={payload["domain"]}', f'tool_id={payload["tool_id"]}',
                                  f'parent_id={payload["parent_id"]}'])

        headers = {
            'authority': 'www.dapachecker.org',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '_ga=GA1.1.659888179.1695963785; XSRF-TOKEN=eyJpdiI6ImNSSzc0RGNKaWNWUFhTNDlSR2IvQ2c9PSIsInZhbHVlIjoiMWt4ZXAyR0lrOTFUZDNuMGkwZjdTbGM3b0o4alNHV2t1UFQyWU9CUjBtdW5jR1hzS1llOXB3QVhtTWZUNkZCdmtpSnB3dWZkbUMrZnN6cm8vRkVaNkFUbXd4dG9qL1dZU1VnR3FCOGZ2QzF2dmlrbVFYRHBBR1NpaitDc3ZGSjkiLCJtYWMiOiIzNDliNWZhNTQwNDJhZDZlYmM4NjM4NGRmOGFlZWZkMGIwMzE5NjY2OTEyODA2NTkzN2M3MDFjNzcyMDAwZDgzIiwidGFnIjoiIn0%3D; dapa_checker_session=eyJpdiI6IlNNQmxIMVRvSWUvSVFVV1pEeEpzU3c9PSIsInZhbHVlIjoiWHBvUlRhUzdXL2YrbTlpSkQxYmtxdk1ucit2NWhDTlRaS2pPTUNMbTZaL3pxVyt1S1pldUpqcHdRc2dIczkzWmJmN0tEZHRtQUtRRlBTQ3lyMWg3Y0hJckQ1QmEvWjJYZjFSV29lUkI3eFZ4ekwzVVZSb2xPTEF2ZHVaaVdlNlAiLCJtYWMiOiIyOTM2MTRjMWVkY2YzNTliMjM4ZDFlODUyNDY5Y2M5MmVjZTU2ZTA1YTQ5OTg1MzllMzg5YzQ5Y2YwMWE2ODAzIiwidGFnIjoiIn0%3D; _clck=gpmu5t|2|ffj|0|1332; _ga_RGRCDVMELW=GS1.1.1696338900.4.0.1696338900.0.0.0; _clsk=1ap6n5b|1696338900876|1|1|o.clarity.ms/collect; TawkConnectionTime=0; twk_uuid_64d5deadcc26a871b02e9a02=%7B%22uuid%22%3A%221.WrsRFVRYy8K2dGTRHvkMawTC4Wzsc1nkT38lvDPXTeF6mcbIlm0oIHJ6OqCc1mJjXDrfrQS0D8c3x8YNZKYXMNrQaurg5yGkPkaGvLqpYVAAOIdvVnjA8TFCZ%22%2C%22version%22%3A3%2C%22domain%22%3A%22dapachecker.org%22%2C%22ts%22%3A1696338910508%7D',
            'origin': 'https://www.dapachecker.org',
            'pragma': 'no-cache',
            'referer': 'https://www.dapachecker.org/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ua.random,
            'x-csrf-token': 'ZqYLkNZnHNnRf2kTN8odsT5FiCczWrlfcR0a4Qt8',
            'x-requested-with': 'XMLHttpRequest'
        }
        # 'user-agent': ua.random,
        url = "https://www.dapachecker.org/checkDA_new"
        response = requests.request("POST", url, headers=headers, data=payload_string)
        response_data = json.loads(response.text)
        chunked_data.extend(response_data['data'])

        # Pass the sorted data and Excel filename to the template
    sorted_chunked_data = sorted(chunked_data, key=lambda x: x['site_da'], reverse=True)

    return render_template('index.html', sorted_chunked_data=sorted_chunked_data)

@app.route('/download/<filename>')
def download_excel(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
