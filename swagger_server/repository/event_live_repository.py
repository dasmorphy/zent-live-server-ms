import json
from loguru import logger
from swagger_server.resources.databases.redis import RedisClient


class EventLiveRepository:
    
    def __init__(self):
        self.redis_client = RedisClient()


    def suscribe_logbook_channel(self, internal, external):
        pubsub = self.redis_client.client.pubsub()
        pubsub.subscribe("logbook_channel")

        try:
            for message in pubsub.listen():
                if message["type"] == "message":
                    yield f"data: {message['data']}\n\n"

        except Exception as exception:
            logger.error('Error en SSE listener:', str(exception), internal=internal, external=external)

            error_event = json.dumps({
                "type": "error",
                "message": "Error en conexión en tiempo real"
            })

            yield f"data: {error_event}\n\n"

        finally:
            pubsub.close()