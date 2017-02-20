from django.shortcuts import render

import urllib2
import json
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

import ast
import csv
from django.http import HttpResponse


# Create your views here.

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def lalaland(temp,a):
	if temp.find(a) != -1:
		ind = temp.find(a)
		temp = temp[:ind-1] + ',' + temp[ind:]
	return temp

def index(request):
	li = ['','Automobiles','Call Centres','Pharmaceuticals/ BioTech/ Research','BPO / KPO','Agriculture/Dairy','Electrical/Electronics',
	'Hospitals/Healthcare','Courier/ Logistics/ Packaging/ Transportation','Paints','Construction / Real  Estate',
	'Accounting/Consulting/ Taxation','Architectural Services/ Interior Designing','Mutual Fund/ Stock Broking',
	'Institutes - Others/ Universities','Export Houses','Hotels / Resorts','Metals/Mining','Paper/Publishing/ Printing/ Stationary'
	'Retail','Advertising/Event Mgmt/ PR/MR','Banks','Chemical','Engineering','FMCG','IT-Software Services','Placement / HR / Training Consultants','Travel / Tourism'
	]
	details = []
	urls = []
	if request.method == 'POST':
		if 'dict' in request.POST:
			#print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
			dt = request.POST["dict"]
			dt = ast.literal_eval(dt)
			#print dt
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="cid.csv"'
			writer = csv.writer(response)

			writer.writerow(["state","city","pin","website","turnover","mobile","phone","jd"])

			for i in dt:
				writer.writerow([i["state"],i["city"],i["pin"],i["website"],i["turnover"],i["mobile"].encode("UTF-8"),i["phone"],i["jd"]])
			return response
		else:
			if 'b2' in request.POST:
				dt = request.POST["addmore"]
				details = ast.literal_eval(dt)
			cat = request.POST['cat']
			page = request.POST['page']
			cat = cat.split(" ")
			cat = "%20".join(cat)

			print cat,page
			#add page and catagory
			url = 'http://www.companiesindelhi.com/ajax.php?gofor=show_listing&location=Delhi&page='+page+'&category='+cat
			cidpage = urllib2.urlopen(url)
			soup = BeautifulSoup(cidpage, "html.parser")
			for a in soup.find_all("a", {"class" : "readmorebtn" , "target" : "_blank"}):
				urls.append('http://www.companiesindelhi.com/'+a['href'])
			for url in urls:	
				cidinfopage = urllib2.urlopen(url)
				soup = BeautifulSoup(cidinfopage, "html.parser")
				temp = ''
				for info in soup.find('div',{'class':'content'}).findAll('div'):
					op = strip_tags(str(info))
					if op not in temp:
						temp = temp + op
				if temp.find('City') != -1:
					ind = temp.find('City')
					temp = temp[:ind-1] + ',' + temp[ind:]
				temp=' '.join(unique_list(temp.split()))
				temp = lalaland(temp,'City')
				temp = lalaland(temp,'Pin')
				temp = lalaland(temp,'Website')
				temp = lalaland(temp,'Company Description')
				temp = lalaland(temp,'Level')
				temp = lalaland(temp,'Sector')
				temp = lalaland(temp,'Total Turnover')
				temp = lalaland(temp,'No Employees')
				temp = lalaland(temp,'Office')
				temp = lalaland(temp,'Mobile')
				temp = lalaland(temp,'Phone')
				temp = temp.split(",")
				qw = {}

				for t in temp:
					if 'State' in t:
						t = t.replace('State','')
						qw['state'] = t
					if 'City' in t:
						t = t.replace('City','')
						qw['city'] = t
					if 'Pin Code' in t:
						t = t.replace('Pin Code','')
						qw['pin'] = t
					if 'Website' in t:
						t = t.replace('Website','')
						qw['website'] = t
					if 'Total Turnover' in t:
						t = t.replace('Total Turnover','')
						qw['turnover'] = t
					if 'Mobile' in t:
						t = t.replace('Mobile','')
						qw['mobile'] = t
					if 'Phone' in t:
						t = t.replace('Phone','')
						qw['phone'] = t
					if 'Company Description Key Figures Contact Details' in t:
						t = t.replace('Company Description Key Figures Contact Details','')
						qw['jd'] = t
				details.append(qw)
	return render(request,'cid/home.html',{'details' : details,'trades' : li})
