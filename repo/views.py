from django.shortcuts import render
import json,ast
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,DetailView,TemplateView
from .models import Push_model,Pull_model,Merged_model
# Create your views here.

@csrf_exempt
def myview_data(request):
	event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')
	print(event)
	merged_=False
	if event=='pull_request':
		req_json=json.loads(request.body.decode('utf-8'))
		author_=req_json['sender']['login']
		to_branch_=req_json['pull_request']['head']['ref']
		from_branch_=req_json['pull_request']['base']['ref']
		time_stamp_=req_json['pull_request']['updated_at']
		try:
			merged_= req_json['pull_request']['merged']
		except KeyError as e:
			print("some error-merged",e)
		if merged_:
			Merged_model.objects.create(author=author_,to_branch=to_branch_,from_branch=from_branch_,time_stamp=time_stamp_)
		else:
			Pull_model.objects.create(author=author_,to_branch=to_branch_,from_branch=from_branch_,time_stamp=time_stamp_)
	elif event=='push':
		req_json=json.loads(request.body.decode('utf-8'))
		author_=req_json['pusher']['name']
		to_branch_=req_json['ref'].split('/')[-1]
		time_stamp_=req_json['head_commit']['timestamp']
		Push_model.objects.create(author=author_,to_branch=to_branch_,time_stamp=time_stamp_)
	return HttpResponse('done')

def myview(request):
	return render(request,"api.html",{"push":Push_model.objects.all(),"pull":Pull_model.objects.all(),"merged":Merged_model.objects.all()})
