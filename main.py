from enum import Enum
from typing import Optional

import uvicorn
from pydantic import BaseModel, Field


# 성별을 위한 Enum 정의
class Gender(str, Enum):
    male = "male"
    female = "female"


# 유저 생성 요청 데이터의 스키마에 age와 gender 필드 추가
class UserCreateRequest(BaseModel):
    username: str
    email: str
    age: int
    gender: Gender



class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[Gender] = None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
