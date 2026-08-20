class EventNotFound(Exception):
    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} not found")


class EventAlreadyExists(Exception):
    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} already exists")
