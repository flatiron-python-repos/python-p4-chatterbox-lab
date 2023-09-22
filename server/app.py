from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from sqlalchemy import asc
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET","POST"])
def messages():
    if(request.method == "GET"):
        messages = Message.query.order_by(asc(Message.id)).all()
        
        resp = [
            {
                "id":message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at
            }
            for message in messages
        ]

        return make_response(jsonify(resp))
    else:
        new_client_message = request.get_json()

        new_message = Message(
            body = new_client_message['body'],
            username = new_client_message['username']
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(
            jsonify(
                {
                "id": new_message.id,
                "body": new_message.body,
                "username": new_message.username,
                "created_at": new_message.created_at
                }
            ), 201)

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first_or_404()

    if(request.method == "PATCH"):
        data_from_db = request.get_json()
        
        message.body = data_from_db['body']
        db.session.commit()

        return make_response(jsonify({
            "id": message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at
        }), 200)
    elif(request.method == "DELETE"):
        db.session.delete(message)
        db.session.commit()

        return make_response(jsonify({
            "message": "User deleted successfully"
        }), 200)




if __name__ == '__main__':
    app.run(port=5555)
