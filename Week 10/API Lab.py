import requests

url = "https://safeut.test.med.utah.edu/apidemo/RestService/Quote"

req = requests.get(url)
print("Status code:", req.status_code)

return_value = req.json()
print(return_value)

# If there is anything the nonconformist hates worse than a conformist, it’s another nonconformist who doesn’t conform to the prevailing standard of nonconformity.
