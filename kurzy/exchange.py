import httpx

r = httpx.get('https://www.cnb.cz/en/financial-markets/foreign-exchange-market/exchange-rate-fixing/daily.txt')

print(r.text)
print(r.status_code)

lines = r.text.split('\n')
print(lines[0])
