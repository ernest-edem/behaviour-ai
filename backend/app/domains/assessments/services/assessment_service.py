from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.domains.assessments.repositories.assessment_repository import AssessmentRepository
from app.domains.assessments.schemas import AssessmentCreate, AssessmentResponse, AssessmentUpdate

class AssessmentService:
    """Business logic for handling health assessments.

    * Validates input data.
    * Enforces domain rules (e.g., required fields).
    * Delegates persistence to :class:`AssessmentRepository`.
    * Raises HTTPException for API layer consumption.
    """

    def __init__(self, db: Session = Depends(get_db)):
        self.repo = AssessmentRepository(db)

    def create_assessment(self, payload: AssessmentCreate) -> AssessmentResponse:
        # Any domain‑specific validation can be added here
        assessment = self.repo.create_assessment(**payload.dict())
        return AssessmentResponse.from_orm(assessment)

    def get_assessment(self, assessment_id: int) -> AssessmentResponse:
        assessment = self.repo.get(assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found",
            )
        return AssessmentResponse.from_orm(assessment)

    def list_assessments(self, user_id: int | None = None) -> List[AssessmentResponse]:
        # Optional filtering by user
        assessments = self.repo.list_by_user(user_id) if user_id else self.repo.list()
        return [AssessmentResponse.from_orm(a) for a in assessments]

    def update_assessment(self, assessment_id: int, payload: AssessmentUpdate) -> AssessmentResponse:
        assessment = self.repo.get(assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found",
            )
        updated = self.repo.update_assessment(assessment, **payload.dict(exclude_unset=True))
        return AssessmentResponse.from_orm(updated)

    def delete_assessment(self, assessment_id: int) -> None:
        assessment = self.repo.get(assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found",
            )
        self.repo.delete(assessment)
