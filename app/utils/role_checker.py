from fastapi import HTTPException, status, Depends
from app.utils.auth import get_current_user

def require_roles(allowed_roles: list):
    def role_checker(user = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return role_checker