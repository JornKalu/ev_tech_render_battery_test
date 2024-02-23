from typing import Optional
from pydantic import BaseModel

class CreateStationModel(BaseModel):
    code: str
    name: str
    description: str
    address: str
    city: str
    state: str
    image: Optional[str] = None

    class Config:
        orm_mode = True

class StationModel(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image: Optional[str] = None
    autonomy_charge: Optional[str] = None
    autonomy_charge_time: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: int
    created_by: int
    created_at: str

    class Config:
        orm_mode = True

class CreateStationResponseModel(BaseModel):
    status: bool
    message: str
    data: StationModel

    class Config:
        orm_mode = True

class UpdateStationModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GeneralStationResponse(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True