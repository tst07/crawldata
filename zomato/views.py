from django.shortcuts import render
from django.http import HttpResponse

import urllib2
import json
from bs4 import BeautifulSoup

import ast
import csv

# Create your views here.

num_list = ['0','1','2','3','4','5','6','7','8','9']

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
				writer.writerow([i["name"],i["contact"]])
			return response
		else:
			if 'b2' in request.POST:
				dt = request.POST["addmore"]
				output_list = ast.literal_eval(dt)
			count = len(output_list)
			url = request.POST["url"]
			zomatopage = urllib2.urlopen(url)
			soup = BeautifulSoup(zomatopage, "html.parser")

			#print soup
			#print soup
			li = []
			for a in soup.find_all("a", {"class" : "readmorebtn" , "target" : "_self"}):
				li.append(a['href'])

			#print li

			for detailurl in li:
				temp = detailurl.split("/")
				company = temp[1]

				print company

				detailurl = 'http://www.vcsdata.com/' + detailurl
				detailpage = urllib2.urlopen(detailurl)
				soup = BeautifulSoup(detailpage, "html.parser")
				companydet = soup.find("div", {"class" : "content"})
				companydet = str(companydet)

				ind = companydet.find('Mobile No',0)
				mobile_number = companydet[ind + 37:ind + 48]

				if mobile_number[0] not in num_list:
					continue

				print mobile_number
				output_list.append({'name' : company, 'contact' : mobile_number})							
	return render(request,'zomato/home.html',{ 'infos' : output_list })