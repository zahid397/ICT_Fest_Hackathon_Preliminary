
"""Authentication endpoints: register, login, refresh, logout."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_token_payload,
    hash_password,
    revoke_access_token,
    verify_password,
    revoke_refresh_token,
)

from ..database import get_db
from ..errors import AppError
from ..models import Organization, User
from ..schemas import LoginRequest, RefreshRequest, RegisterRequest


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=201)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    org = (
        db.query(Organization)
        .filter(
            Organization.name == payload.org_name
        )
        .first()
    )


    role = "admin"


    if org is None:
        org = Organization(
            name=payload.org_name
        )

        db.add(org)
        db.commit()
        db.refresh(org)

    else:
        role = "member"



    existing = (
        db.query(User)
        .filter(
            User.org_id == org.id,
            User.username == payload.username
        )
        .first()
    )


    if existing:
        raise AppError(
            409,
            "USERNAME_TAKEN",
            "Username already exists"
        )



    user = User(
        org_id=org.id,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=role
    )


    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        raise AppError(
            409,
            "USERNAME_TAKEN",
            "Username already exists"
        )



    return {
        "user_id": user.id,
        "org_id": org.id,
        "username": user.username,
        "role": user.role,
    }



@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    org = (
        db.query(Organization)
        .filter(
            Organization.name == payload.org_name
        )
        .first()
    )


    user = None


    if org:

        user = (
            db.query(User)
            .filter(
                User.org_id == org.id,
                User.username == payload.username
            )
            .first()
        )


    if (
        user is None
        or not verify_password(
            payload.password,
            user.hashed_password
        )
    ):

        raise AppError(
            401,
            "INVALID_CREDENTIALS",
            "Invalid username or password"
        )


    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "bearer",
    }




@router.post("/refresh")
def refresh(
    payload: RefreshRequest,
    db: Session = Depends(get_db)
):

    data = decode_token(
        payload.refresh_token
    )


    if data.get("type") != "refresh":

        raise AppError(
            401,
            "UNAUTHORIZED",
            "Wrong token type"
        )


    if data.get("revoked"):

        raise AppError(
            401,
            "UNAUTHORIZED",
            "Token already used"
        )


    user = (
        db.query(User)
        .filter(
            User.id == int(data["sub"])
        )
        .first()
    )


    if user is None:

        raise AppError(
            401,
            "UNAUTHORIZED",
            "Unknown user"
        )


    # invalidate old refresh token
    revoke_refresh_token(
        payload.refresh_token
    )


    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "bearer",
    }




@router.post("/logout")
def logout(
    payload: dict = Depends(get_token_payload)
):

    revoke_access_token(payload)

    return {
        "status": "ok"
    }
