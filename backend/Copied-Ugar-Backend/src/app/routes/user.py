from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
def register_user():
    pass


@router.post("/login")
def login_user():
    pass


@router.get("/me")
def read_user():
    pass


@router.post("/verify-email/{verification_code}")
def verify_email():
    pass
