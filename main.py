from typing import Annotated, List, Dict, Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from enum import Enum


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


class UserModel:
    _users = []
    _current_id = 0

    @classmethod
    def create_dummy(cls):
        """API 테스트를 위한 더미 사용자 데이터 생성"""
        cls.create(username="john.doe", email="john.doe@example.com", age=30, gender=Gender.male)
        cls.create(username="jane.smith", email="jane.smith@example.com", age=25, gender=Gender.female)

    @classmethod
    def create(cls, username: str, email: str, age: int, gender: Gender) -> Dict:
        """새로운 사용자 생성 및 저장"""
        cls._current_id += 1
        user = {"id": cls._current_id, "username": username, "email": email, "age": age, "gender": gender}
        cls._users.append(user)
        return user

    @classmethod
    def all(cls) -> List[Dict]:
        """모든 사용자 목록 반환"""
        return cls._users

    @classmethod
    def get(cls, id: int) -> Optional[Dict]:
        """특정 ID의 사용자 정보 반환"""
        for user in cls._users:
            if user['id'] == id:
                return user
        return None

    @classmethod
    def update(cls, id: int, data: Dict) -> Optional[Dict]:
        """
        특정 ID의 사용자 정보를 업데이트합니다.
        """
        user = cls.get(id=id)
        if user:
            user.update(data)
            return user
        return None

    @classmethod
    def delete(cls, id: int) -> bool:
        """
        특정 ID의 사용자를 삭제합니다.
        """
        user = cls.get(id=id)
        if user:
            cls._users.remove(user)
            return True
        return False

    @classmethod
    def filter(cls, **kwargs) -> List[Dict]:
        """쿼리 매개변수를 기반으로 사용자를 필터링합니다."""
        results = cls._users
        for key, value in kwargs.items():
            if value is not None:
                results = [user for user in results if user.get(key) == value]
        return results


app = FastAPI()

UserModel.create_dummy()


@app.post('/users', response_model=Dict)
async def create_user(data: UserCreateRequest):
    """
    새로운 사용자를 생성합니다.
    """
    # data.model_dump()는 UserCreateRequest의 모든 필드를 포함하므로,
    # 이제 age와 gender가 자동으로 전달됩니다.
    user = UserModel.create(**data.model_dump())
    return {"id": user.id}


@app.get('/users/search', response_model=List[UserResponse])
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    """
    쿼리 매개변수를 이용해 사용자를 검색합니다.
    예시: /users/search?username=john.doe&age=30
    """
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)

    if not filtered_users:
        raise HTTPException(status_code=404, detail="No users found with the given criteria")

    return filtered_users


@app.get('/users', response_model=List[UserResponse])
async def get_all_users():
    """
    모든 사용자 목록을 조회합니다.
    """
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result


@app.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: Annotated[int, Path(gt=0)]):
    """
    특정 ID를 가진 사용자 정보를 조회합니다.
    ID는 0보다 커야 합니다.
    """
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user


@app.patch('/users/{user_id}', response_model=UserResponse)
async def update_user(user_id: Annotated[int, Path(gt=0)], data: UserUpdateRequest):
    """
    특정 ID를 가진 사용자 정보를 부분적으로 수정합니다.
    """
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    update_data = data.model_dump(exclude_unset=True)
    user.update(update_data)

    return user


@app.delete('/users/{user_id}')
async def delete_user(user_id: Annotated[int, Path(gt=0)]):
    """
    특정 ID를 가진 사용자를 삭제합니다.
    """
    is_deleted = UserModel.delete(id=user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    return {'detail': f'User {user_id} successfully deleted.'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
