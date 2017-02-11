from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.

margin = 20

jt_map = {
	'B2B Sales' : {
		'price' : 270,
		'turnup' : 4, 
	},
	'Delivery Boy' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Telecaller(Basic English)' : {
		'price' : 200,
		'turnup' : 4, 
	},	
	'Telecaller(Fluent English)' : {
		'price' : 275,
		'turnup' : 5, 
	},	
	'Waiter' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Cooks' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Helper/Housekeeping/Security' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Driver' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Accountant' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Data Entry' : {
		'price' : 150,
		'turnup' : 5, 
	},	
	'Field Executive(Payment/Document/Purchase)' : {
		'price' : 150,
		'turnup' : 5, 
	},	
}

jobtitles = [
"Delivery Boy",
"B2B Sales",
"Telecaller(Basic English)",
"Telecaller(Fluent English)",
"Waiter",
"Cooks",
"Helper/Housekeeping/Security",
"Driver",
"Accountant",
"Data Entry",
"Field Executive(Payment/Document/Purchase)"
]

def index(request):
	resp = {'jt' : '' , 'vac' : '' , 'cost' : '' , 'jobtitles' : jobtitles}
	if request.method == 'POST':
		jt = request.POST['jt']
		vacancy = int(request.POST['vac'])

		price = jt_map[jt]['price']
		turnup = jt_map[jt]['turnup']

		x = price*turnup*vacancy
		our_cost = (margin * x)/100
		resp['cost'] = x + our_cost
		resp['vac'] = vacancy
		resp['jt'] = jt
	return render(request,'home.html',resp)

def addview(request):
	return HttpResponse('........')
	if request.method == 'POST':
		jt = request.POST['jt']
		margin = request.POST['mar']
		price = request.POST['price']
		jt_map[jt] = {}
		jt_map[jt]['price'] = int(price)
		jt_map[jt]['margin'] = int(margin)
		return redirect('index')
	return render(request,'add.html')