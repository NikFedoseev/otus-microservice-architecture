from enum import Enum

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    IN_WORK = 'IN_WORK'
    DONE = 'DONE'
    CANCEL = 'CANCEL'