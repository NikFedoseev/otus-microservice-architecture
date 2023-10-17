from enum import Enum

class CartOperation(Enum):
    REPLENISHMENT = 'REPLENISHMENT'
    DEBITING = 'DEBITING'
    REFUNDING = 'REFUNDING'