from timeit import default_timer
from flask import Response, request, stream_with_context
from flask.views import MethodView
from loguru import logger

from swagger_server.repository.event_live_repository import EventLiveRepository
from swagger_server.uses_cases.event_live_use_case import EventLiveUseCase
from swagger_server.utils.transactions.transaction import generate_internal_transaction_id


class EventLiveView(MethodView):
    def __init__(self):
        self.logger = logger
        event_live_repository = EventLiveRepository()
        self.event_live_use_case = EventLiveUseCase(event_live_repository)

    def get_live_all_logbooks(self):  # noqa: E501
        internal_transaction_id = str(generate_internal_transaction_id())
        external_transaction_id = request.args.get('externalTransactionId')

        try:
            return Response(
                stream_with_context(
                    self.event_live_use_case.suscribe_logbook_channel(internal_transaction_id, external_transaction_id)
                ),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"  # IMPORTANTE si usas Nginx
                }
            )
        
        except Exception as exception:
            logger.error("Error inicializando SSE", str(exception), internal=internal_transaction_id, external=external_transaction_id)
            return {"message": "Error iniciando stream"}, 500