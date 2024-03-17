import abc

from sqlalchemy.orm import Session

from src.architecture_python.chapter02.database import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference) -> model.Batch:
        batches = (
            self.session.query(model.Batch)
            .filter_by(reference=reference)
            .limit(1)
            .all()
        )

        return batches[0] if batches else None

    def list(self):
        return self.session.query(model.Batch).all()

    def list_all_orderlines(self):
        return self.session.query(model.OrderLine).all()