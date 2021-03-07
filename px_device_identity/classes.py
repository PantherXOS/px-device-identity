'''Key runtime parameter'''

from dataclasses import dataclass


@dataclass
class OperationProperties:
    '''Attributes related primarily to a user input; for ex. via CLI'''
    action: str
    force_operation: bool
