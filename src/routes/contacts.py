from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, ContactUpdate
from src.database.models import User
from src.repository import contacts as repository_contacts
from .auth import auth_service
from datetime import date

router = APIRouter(prefix='/contacts')


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    today = date.today()
    upcoming_birthdays = (
        await repository_contacts
        .get_upcoming_birthdays(db, current_user, today)
    )
    return upcoming_birthdays


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contacts = (
        await repository_contacts
        .get_contacts(skip, limit, current_user, search, db)
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    contact = (
        await repository_contacts
        .get_contact(contact_id, current_user, db)
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post(
        "/",
        response_model=ContactResponse,
        status_code=status.HTTP_201_CREATED
)
async def create_contact(
    body: ContactModel,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return await repository_contacts.create_contact(body, current_user, db)


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    contact = (
        await repository_contacts
        .update_contact(contact_id, body, current_user, db)
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    contact = (
        await repository_contacts
        .remove_contact(contact_id, current_user, db)
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact