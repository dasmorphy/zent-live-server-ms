from swagger_server.repository.event_live_repository import EventLiveRepository


class EventLiveUseCase:

    def __init__(self, event_live_repository: EventLiveRepository):
        self.event_live_repository = event_live_repository

    def suscribe_logbook_channel(self, internal, external):
        return self.event_live_repository.suscribe_logbook_channel(internal, external)