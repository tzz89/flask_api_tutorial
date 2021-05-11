from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes} "


if not os.path.exists("src\database.db"):
    db.create_all()  # we only want to create once
    print("#"*20+" DB created" + "#"*20)

names = {"tim": {"age": 19, "gender": "male"},
         "bill": {"age": 70, "gender": "male"}
         }


class Helloworld(Resource):  # handles GET POST DELETE requests
    def get(self, name):
        # we need to make sure that the information is serializable eg python
        # json serializable
        # dictionary - json object
        # list/tuples - json array
        # int/float - json numbers
        # None - json null
        return names[name]

    def post(self):
        return "posted!"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)  # like error message
video_put_args.add_argument(
    "views", type=int, help="views of the video is required", required=True)  # like error message
video_put_args.add_argument(
    "likes", type=int, help="likes of the video is required", required=True)  # like error message


def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video does not exist")


def abort_if_video_id_exist(video_id):
    if video_id in videos:
        abort(409, message="Video already exist")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def put(self, video_id):  # create new entry
        # print(request.form)  # returns something like dictionary
        args = video_put_args.parse_args()
        video_entry = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])

        db.session.add(video_entry)
        db.session.commit()

        return video_entry, 201  # 201 means created

    # this will help to serialize the instance of the videoModel object when returning
    @marshal_with(resource_fields)
    def get(self, video_id):
        # returns an instance of VideoModel object
        result = VideoModel.query.filter_by(id=video_id).first()
        return result, 200

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return {"status": "failed"}, 204  # 204 mean sucessful


        # passing parameters into the request
api.add_resource(Helloworld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
