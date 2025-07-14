import requests


testpost1 = requests.post(url='http://127.0.0.1:5000/reviews', json='Хорошо сделано')
testpost2 = requests.post(url='http://127.0.0.1:5000/reviews', json='{"text": "Хорошо сделано"}')
testpost3 = requests.post(url='http://127.0.0.1:5000/reviews', json='{"text": "Плохо сделано"}')
print(testpost1, testpost2.text, testpost3.text)

testget = requests.get(url='http://127.0.0.1:5000/reviews?sentiment=positive')
print(testget.text)