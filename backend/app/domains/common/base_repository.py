from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: Session):
        self.session = session

    def get(self, model: type[T], id: int) -> Optional[T]:
        return self.session.get(model, id)

    def list(self, model: type[T]) -> List[T]:
        return self.session.query(model).all()

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self) -> None:
        self.session.commit()

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()
