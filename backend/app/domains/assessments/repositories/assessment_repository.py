from typing import List, Optional
from sqlalchemy.orm import Session
from app.domains.common.base_repository import BaseRepository
from app.domains.assessments.models.assessment import Assessment

class AssessmentRepository(BaseRepository[Assessment]):
    """CRUD operations for Assessment domain"""

    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_user(self, user_id: int) -> List[Assessment]:
        return self.session.query(Assessment).filter(Assessment.user_id == user_id).all()

    def create_assessment(self, **kwargs) -> Assessment:
        assessment = Assessment(**kwargs)
        self.session.add(assessment)
        self.session.commit()
        self.session.refresh(assessment)
        return assessment
