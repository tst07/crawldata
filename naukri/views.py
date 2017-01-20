from django.shortcuts import render
import urllib2
import json
from bs4 import BeautifulSoup

import ast
import csv
from django.http import HttpResponse

# Create your views here.

def index(request):
	output_list = []
	if request.method == 'POST':
		if 'dict' in request.POST:
			dt = request.POST["dict"]
			dt = ast.literal_eval(dt)
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="naukri.csv"'
			writer = csv.writer(response)

			for i in dt:
				writer.writerow([i["number"],i["RecruiterName"],i["tel"],i["Website"],i["EmailAddress"],i["Address"].encode("UTF-8"),i["ContactCompany"]])
			return response
		else:
			count = 0
			url = request.POST["url"]
			pageurl = url
			for page in range(1,5):
				print pageurl
				naukripage = urllib2.urlopen(pageurl)
				soup = BeautifulSoup(naukripage, "html.parser")

				li = []

				for a in soup.find_all("a", {"class" : "content" , "target" : "_blank"}):
					li.append(a['href'])

				#print li

				for infourl in li:
				    x = infourl.split("years-")
				    x = x[1].split("?")[0]

				    infourl = 'https://www.naukri.com/jd/contactDetails?file=' + x
				    #print infourl
				    response = urllib2.urlopen(infourl)
				    data = json.loads(response.read())

				    #print data['fields']['Telephone']
				    
				    if "fields" in data.keys():
						#print "xxxxxxxxxxxxxxxxxxxxxxxxxx"
						data = data['fields']
						jobdata_dict = {
							"number" : count ,
						    "tel" : data.get("Telephone", ""),
						    "RecruiterName" : data.get("Recruiter Name", ""),
						    "Website" : data.get("Website", ""),
						    "EmailAddress" : data.get("Email Address", {}).get("title", ""),
						    "Address" : data.get("Address", ""),
						    "ContactCompany" : data.get("Contact Company", "")
						}
						#print jobdata_dict
						output_list.append(jobdata_dict)
						count = count + 1
				pageurl = url + "-" + str(page)
			#print output_list
	return render(request,'naukri/home.html',{'infos' : output_list})