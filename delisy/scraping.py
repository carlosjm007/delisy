# import libraries
import sys, json, requests

# specify the url
URL = 'https://www.ubereats.com/rtapi/eats/v2/marketplaces'
# https://www.ubereats.com/rtapi/eats/v1/allstores?plugin=StorefrontFeedPlugin
# https://www.ubereats.com/rtapi/eats/v1/allstores?plugin=StorefrontFeedPlugin
client = requests.session()

# Retrieve the CSRF token first
page = client.get("https://www.ubereats.com/es-NZ/stores/")  # sets cookie
pagina = str(page.content)
ubicacion_csrf = pagina.find("window.csrfToken")
bandera = True
csrftoken = ""
while(bandera):
	csrftoken = csrftoken + pagina[ubicacion_csrf]
	ubicacion_csrf = ubicacion_csrf + 1
	if pagina[ubicacion_csrf] == ";":
		bandera = False
csrftoken = csrftoken.replace("window.csrfToken","").replace(" = ","").replace("\\'","")
print(csrftoken)
headers={
	"Referer":"https://www.ubereats.com/es-NZ/stores/",
	"x-csrf-token":csrftoken,
	"content-type": "application/json",
	"x-requested-with": "XMLHttpRequest"}

#data='{targetLocation:{latitude:-36.8505351,longitude:174.7646794,reference:"EiNRdWVlbiBTdHJlZXQsIEF1Y2tsYW5kLCBOZXcgWmVhbGFuZA",type:"google_places",address:{title:"Queen Street",address1:"Queen St, Auckland",city:"Auckland"}},hashes:{stores:""},feed:"combo",feedTypes:["STORE","SEE_ALL_STORES"],feedVersion:2}'
data='{"targetLocation":{"latitude":-36.8505351,"longitude":174.7646794,"reference":"EiNRdWVlbiBTdHJlZXQsIEF1Y2tsYW5kLCBOZXcgWmVhbGFuZA","type":"google_places","address":{"title":"Queen Street","address1":"Queen St, Auckland","city":"Auckland"}},"hashes":{"stores":""},"feed":"combo","feedTypes":["STORE","SEE_ALL_STORES"],"feedVersion":2}'

'''

data = '{"pageInfo":{"offset":80,"pageSize":80},"targetLocation":{"latitude":-36.8505351,"longitude":174.7646794,"reference":"EiNRdWVlbiBTdHJlZXQsIEF1Y2tsYW5kLCBOZXcgWmVhbGFuZA","type":"google_places","address":{"title":"Queen Street","address1":"Queen St, Auckland","city":"Auckland"}},"sortAndFilters":[{"uuid":"1c7cf7ef-730f-431f-9072-26bc39f7c021","options":[{"uuid":"3c7cf7ef-730f-431f-9072-26bc39f7c022"}]}]}'

'''

r = client.post(URL, headers=headers, json=json.loads(data))
data = r.json()
print(r.status_code)
#print(r.content)
for ind, i in enumerate(data["marketplace"]["feed"]["feedItems"]):
	if "storePayload" in i["payload"]:
		print(ind, i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"])	