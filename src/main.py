from flask import Flask, render_template,make_response,send_file,abort,request,redirect
from flask_restful import Api,Resource,fields,reqparse,marshal_with,marshal
from flask_cors import CORS
import ollama

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'bacaa3381e4c453088449ccd04f270cf'
CORS(app)

add = '127.0.0.1:5000'

loc_parser = reqparse.RequestParser()
loc_parser.add_argument('location',type=str,required = True)

class AkashBot:
    def __init__(self):
        ollama.pull(model='deepseek-r1:latest')
        self.client = ollama.Client()
        self.client.create(model='InfrastructureInsight',from_ = 'deepseek-r1:latest', messages=[{'role':'system','content':
                                                                                            'You are a infrastructure insight specialist who looks at soil content and natural diasters in that particular area.You will only have the area name. You then advices builders on how to build their buildings. DO NOT INTRODUCE YOURSELF. Do not mention the user, only generate a professional report. No Comments'}])
    def generate_response(self,loc):
        response = self.client.chat(model = 'InfrastructureInsight',messages=[{'role':'system','content':
                                                                                            'You are a infrastructure insight specialist who looks at soil content and natural diasters in that particular area.You will only have the area name. You then advices builders on how to build their buildings. DO NOT INTRODUCE YOURSELF. Do not mention the user, only generate a professional report. No Comments'},{'role':'user','content':'The location is '+loc}])
        return response
class Home(Resource):
    def post(self):
        args = loc_parser.parse_args()
        loc = args['location']
        print(loc)
        a1 = AkashBot()
        response = a1.generate_response(loc)
        message = response['message']['content']
        return {'advice':response['message']['content'][message.index('</think>')+10:]}

api.add_resource(Home,'/ai/')

app.run(debug=True)