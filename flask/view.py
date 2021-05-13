from flask import Flask,json,request,render_template
from flask_pymongo import PyMongo


app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"
mongo = PyMongo(app)

@app.route('/')
def index():
	pull_=list(mongo.db['repo_pull_model'].find())
	push_=list(mongo.db['repo_push_model'].find())
	merge_=list(mongo.db['repo_merged_model'].find())
	return render_template('api.html', pull=pull_, push=push_,merged=merge_)

@app.route('/git/',methods=['POST'])
def get_git():
	if request.headers['Content-Type']=='application/json':
		event = request.headers.get('X-Github-Event','ping')
		merged_=False
		if event=='pull_request':
			req_json=request.json
			author_=req_json['sender']['login']
			to_branch_=req_json['pull_request']['head']['ref']
			from_branch_=req_json['pull_request']['base']['ref']
			time_stamp_=req_json['pull_request']['updated_at']
			try:
				merged_= req_json['pull_request']['merged']
			except KeyError as e:
				print("some error-merged",e)
			val={'author':author_,'to_branch':to_branch_,'from_branch':from_branch_,'time_stamp':time_stamp_}
			if merged_:
				mongo.db['repo_merged_model'].insert_one(val)
			else:
				mongo.db['repo_pull_model'].insert_one(val)
		elif event=='push':
			req_json=request.json
			author_=req_json['pusher']['name']
			to_branch_=req_json['ref'].split('/')[-1]
			time_stamp_=req_json['head_commit']['timestamp']
			val={'author':author_,'to_branch':to_branch_,'time_stamp':time_stamp_}
			mongo.db['repo_push_model'].insert_one(val)
		return ''

if __name__ == '__main__':
	app.run(debug=True)