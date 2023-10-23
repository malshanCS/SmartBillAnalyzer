import json
import pickle
import requests

url = "https://ocr.asprise.com/api/v1/receipt"
image = "aspire\example1.jpeg"

res = requests.post(url, 
                    data = {
                        'api.key': 'TEST',
                        'recognizer': 'auto',
                        'ref_no': 'ocr_python_123'
                    },
                    files = {
                        'file': open(image, 'rb')
                    })    


with open("response1.json", "w") as f:
    data = json.dump(json.loads(res.text),f)

print(data['receipts'][0].keys())

# items = data['receipts'][0]['items']

# print(f"Your purchase is {data['receipts'][0]['merchant_name']}")

# for item in items:
#     print(f"{item['description']} - {data['receipts'][0]['currency']} {item['amount']}")

# print("-" * 30)
