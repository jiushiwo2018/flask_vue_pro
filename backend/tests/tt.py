import requests
import json
# s = requests.Session()
# resg = requests.get("http://10.239.220.59:5005/login",stream=True)

data = json.dumps({
  "ingredients": [
    {
      "name": "Battery",
      "platforms": [
        "BXTM-RSP-Win10-DT",
        "CHT-T3-RS3-Cons"
      ],
      "version": "222"
    }
  ]
})
headers={'Content-Type':'application/json'}
rev = "feature/powrtest"
locator= ""
url = "http://10.239.52.24:5000/api/0/rev/{}/manifest/ingredients{}".format(rev, locator)
url1 = "http://10.239.46.6:5000/api/0/rev/feature/powrtest/manifest/ingredients?locator=ingredient:EC"
resg = requests.get(url)
# resg = requests.patch(url, data=data, headers=headers)
print("post-----", resg.status_code)
print(resg.text)
#
a = """'Access-Control-Allow-Methods':'GET, POST, PATCH', 'Access-Control-Allow-Credentials':'true', 'Server':'Werkzeug/0.15.5 Python/3.6.8'"""



# class TestV2exApi(object):
#
#     domain = 'https://www.v2ex.com/'
#
#     @pytest.fixture(params=['python', 'java', 'go', 'nodejs'])
#     def lang(self, request):
#         return request.param
#
#     def test_node_1(self):
#         path = 'api/nodes/show.json?name=python'
#         url = self.domain + path
#         res = requests.get(url)
#         assert res.status_code == 200
#         ret = res.json()
#         assert ret['id'] == 90
#         assert ret['name'] == 'python'
#         assert 0
#
#     def test_node_2(self, lang):
#         path = f'api/nodes/show.json?name={lang}'
#         url = self.domain + path
#         res = requests.get(url)
#         assert res.status_code == 200
#         ret = res.json()
#         assert ret['name'] == lang
#         assert 0
#
#     @pytest.mark.parametrize('name,node_id', [('python', 90), ('java', 63), ('go', 375), ('nodejs', 436)])
#     def test_node_3(self, name, node_id):
#         path = 'api/nodes/show.json?name=%s' % (name)
#         url = self.domain + path
#         res = requests.get(url).json()
#         assert res['name'] == name
#         assert res['id'] == node_id
#         assert 0
#
#
