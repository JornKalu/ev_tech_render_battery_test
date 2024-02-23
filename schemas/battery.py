from typing import Optional, Any, List
from pydantic import BaseModel

class CreateBatteryModel(BaseModel):
    code: str
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class BatteryModel(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    voltage: Optional[str] = None
    temperature: Optional[str] = None
    charge: Optional[str] = None
    humidity: Optional[str] = None
    electric_current: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[int] = 0
    created_by: int
    created_at: str

    class Config:
        orm_mode = True

class CreateBatteryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[BatteryModel] = None

    class Config:
        orm_mode = True

class UpdateBatteryModel(BaseModel):
    code: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GeneralBatteryResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class SyncBatteryModel(BaseModel):
    battery_id: int
    initial_instruction: Optional[str] = None
    voltage: Optional[str] = None
    temperature: Optional[str] = None
    charge: Optional[str] = None
    electric_current: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    # is_docked_charging: Optional[int] = None
    # is_docked_discharging: Optional[int] = None
    charge_status: Optional[int] = None
    discharge_status: Optional[int] = None
    enable_status: Optional[int] = None
    disable_status: Optional[int] = None

    class Config:
        orm_mode = True

class SyncBatteryDataResponseModel(BaseModel):
    host_id: Optional[str] = None
    charge: Optional[int] = None
    discharge: Optional[int] = None
    hotlist: Optional[int] = None
    shutdown: Optional[int] = None
    idle: Optional[int] = None

    class Config:
        orm_mode = True


class SyncBatteryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[SyncBatteryDataResponseModel] = None

    class Config:
        orm_mode = True
