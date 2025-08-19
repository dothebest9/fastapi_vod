from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# 성별을 위한 Enum 정의
class Gender(str, Enum):
    male = "male"
    female = "female"

# 유저 생성 요청 데이터의 스키마
class UserCreateRequest(BaseModel):
    username: str = Field(..., example="johndoe")
    age: int = Field(..., ge=0, example=30)
    gender: Gender = Field(..., example="male")


# 유저 업데이트 요청 데이터의 스키마
class UserUpdateRequest(BaseModel):
    # Optional[str]는 Python 3.9 이하에서 사용되며,
    # Python 3.10 이상에서는 str | None으로 쓸 수 있습니다.
    username: Optional[str] = None
    age: Optional[int] = None


# 유저 검색 파라미터의 스키마
class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: Optional[str] = None
    # 'age' 필드에 'gt=0' 제약 조건을 적용
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[Gender] = None
