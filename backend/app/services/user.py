from app.schemas import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from app.repository import UserRepository, CollegeRepository
from app.exceptions import UserAlreadyExistError, CollegeNotFoundError, CollegeAlreadyExistError, IncorrectCredentialError
from app.utils.hashing import hash_password, verify_password
from app.models import UserRole
from app.core.token import create_access_token, create_refresh_token

class UserService:
    def __init__(self, user_repo : UserRepository, college_repo: CollegeRepository):
        self.user_repo = user_repo
        self.college_repo = college_repo
        
    async def signup(self, data: SignupRequest):
        is_exist = await self.user_repo.is_email_exist(data.email)
        if is_exist:
            raise UserAlreadyExistError()
        
        hashed_password = hash_password(data.password)
        
        college = await self.college_repo.email_to_college(data.email)
        
        if college and data.role == UserRole.CAMPUS_ADMIN:
            raise CollegeAlreadyExistError()
        
        if data.role == UserRole.STUDENT and not college:
            raise CollegeNotFoundError()
        
        college_id = college.id if college else None
        new_user = await self.user_repo.create_user(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hashed_password,
            role=data.role,
            college_id=college_id
        )
        payload = {
            "sub": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role
        }
        if data.role == UserRole.STUDENT:
            new_student = await self.user_repo.create_student(user_id=new_user.id)
            payload["college_slug"] = college.slug
        elif data.role == UserRole.CAMPUS_ADMIN:
            new_campus_admin = await self.user_repo.create_campus_admin(user_id=new_user.id)
            
        access_token = create_access_token(payload=payload)
        refresh_token = create_refresh_token(payload=payload)
        return SignupResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def login(self, data: LoginRequest):
        is_exist = await self.user_repo.is_email_exist(data.email)
        if not is_exist:
            raise IncorrectCredentialError()
        
        user = await self.user_repo.get_user_by_email(data.email)
        
        if not verify_password(data.password, user.hashed_password):
            raise IncorrectCredentialError()
        
        slug = await self.college_repo.id_to_slug(user.college_id) if user.college_id else None
        
        payload = {
            "sub": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "college_slug": slug
        }
            
        access_token = create_access_token(payload=payload)
        refresh_token = create_refresh_token(payload=payload)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
        
        
        
        
            
        
        
        
        
        