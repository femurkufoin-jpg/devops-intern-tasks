import os
import redis
from flask import jsonify

def register_routes(app):
   redis_client = redis.Redis(
       host=os.getenv("REDIS_HOST", "redis"),
       port=int(os.getenv("REDIS_PORT", 6379)),
       decode_responses=True
   )
   @app.route("/")
   def home():
       return jsonify({
           "message": "Docker Compose Flask Application is running!"
       })
   @app.route("/health")
   def health():
       try:
           redis_client.ping()
           return jsonify({
               "status": "healthy",
               "redis": "connected"
           }), 200
       except redis.RedisError:
           return jsonify({
               "status": "unhealthy",
               "redis": "disconnected"
           }), 503
   @app.route("/visits")
   def visits():
       count = redis_client.incr("visits")
       return jsonify({
           "visits": count
       })
