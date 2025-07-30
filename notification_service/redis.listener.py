import redis
import json
from notification import ws_manager

def listen_for_alerts():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe('fire_alerts')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            ws_manager.emit_fire_alert(data)
