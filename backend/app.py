import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

load_dotenv()

from config import Config
from extensions import db, jwt
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.courses import courses_bp, wrong_book_bp
from routes.marketing import marketing_bp, orders_bp
from routes.points import points_bp
from routes.questions import questions_bp
from routes.learning import learning_bp
from routes.teacher import teacher_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(points_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(wrong_book_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(marketing_bp)
    app.register_blueprint(orders_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "status": "ok"})

    return app


app = create_app()


def wait_for_db(max_retries=30):
    for i in range(max_retries):
        try:
            with app.app_context():
                db.engine.connect()
            return True
        except Exception:
            time.sleep(2)
    return False


def init_mongo():
    client = MongoClient(app.config["MONGO_URI"])
    app.mongo_db = client.get_default_database()


with app.app_context():
    if wait_for_db():
        db.create_all()
        init_mongo()
        from scripts.seed import run_seed

        run_seed(app)
