from django.shortcuts import render

import urllib2
import json
from bs4 import BeautifulSoup

import ast
import csv
from django.http import HttpResponse


# Create your views here.

def index(request):
	details = []
	urls = []
	if request.method == 'POST':
		if 'dict' in request.POST:
			#print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
			dt = request.POST["dict"]
			dt = ast.literal_eval(dt)
			#print dt
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="naukri.csv"'
			writer = csv.writer(response)

			for i in dt:
				temp = []
				for j in i:
					temp.append(j)
				writer.writerow(temp)
			return response
		else:
			if 'b2' in request.POST:
				dt = request.POST["addmore"]
				details = ast.literal_eval(dt)
			url = request.POST['url']
			shinepage = urllib2.urlopen(url)
			soup = BeautifulSoup(shinepage, "html.parser")
			for a in soup.find_all("a", {"class" : "cls_searchresult_a" , "target" : "_blank"}):
				urls.append('https://www.shine.com'+a['href'])
			for url in urls: 
				shineinfopage = urllib2.urlopen(url)
				soup = BeautifulSoup(shineinfopage, "html.parser")
				for li in soup.find('div',{'class':'ropen cls_rect_detail_div'}).findAll('ul'):
					li = str(li)
					if len(li) > 19:
						li = li[8:-10]
						li = li.split("</li><li>")
						#print li
						resp = []
						for l in li:
							if '</strong>' in l:
								l = l.split("</strong>")[1]
							l.replace("<br/>","")
							resp.append(l)
						details.append(resp)
	return render(request,'shine/home.html',{'details' : details})