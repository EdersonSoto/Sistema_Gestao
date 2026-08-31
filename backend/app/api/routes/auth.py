from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import CurrentUser, LoginRequest, TokenResponse, UserCreate, UserRead

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def _user_to_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        full_name=user.full_name,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
    )


def _user_to_current(user: User) -> CurrentUser:
    return CurrentUser(
        id=user.id,
        full_name=user.full_name,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> CurrentUser:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token_data = decode_token(credentials.credentials)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = db.query(User).filter(User.username == token_data.subject).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not available")

    return _user_to_current(user)


def require_roles(*allowed_roles: str):
    def dependency(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(
        full_name=payload.full_name,
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _user_to_read(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenResponse(access_token=create_token(user.username))


@router.get("/me", response_model=CurrentUser)
def me(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return current_user


@router.get("/me/admin", response_model=CurrentUser)
def me_admin(current_user: CurrentUser = Depends(require_roles("admin"))) -> CurrentUser:
    return current_user


@router.get("/users", response_model=list[UserRead])
def list_users(
    _: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[UserRead]:
    users = db.query(User).order_by(User.full_name.asc()).all()
    return [_user_to_read(user) for user in users]
