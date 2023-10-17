from enum import Enum

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    DELIVERING = 'DELIVERING'
    DONE = 'DONE'
    CANCEL = 'CANCEL'