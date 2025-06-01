from typing import Protocol


class TransactionManager(Protocol):
    def commit(self):
        raise NotImplementedError()
