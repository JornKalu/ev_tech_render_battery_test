from fastapi import APIRouter, Request, Depends, HTTPException, Response
from database.db import get_session
from sqlalchemy.orm import Session
from database.schema import SyncBatteryModel, SyncBatteryResponseModel, BatteryModel, ErrorResponse
from fastapi.encoders import jsonable_encoder
from modules.batteries.battery import process_battery_request, process_battery_request_main, sync_battery_request, sync_battery_details, get_single_battery_by_code, get_single_battery_by_id, process_battery_request_get
import json

router = APIRouter(
    # prefix="/battery",
    tags=["v1_bat"]
)

@router.get("/gp")
async def get_process(request: Request, db: Session = Depends(get_session), ii: str=None, t: str=None, c: str=None, v: str=None, bID: str=None, SOC: str=None, s: str=None, LT: str=None, LG: str=None):
    ip_address = request.client.host
    return process_battery_request_get(db=db, ip_address=ip_address, initial_instruction=ii, t=t, c=c, v=v, bID=bID, SOC=SOC, s=s, LT=LT, LG=LG)

@router.post("/process")
async def post_requests(request: Request, db: Session = Depends(get_session)):
    body = await request.body()
    ip_address = request.client.host
    # data = process_battery_request(db=db, data=body, ip_address=ip_address)
    data = process_battery_request_main(db=db, data=body, ip_address=ip_address)
    return Response(content=data, media_type="text/plain")
    # return data

@router.post("/sync", response_model=SyncBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def sync(fields: SyncBatteryModel, db: Session = Depends(get_session)):
    original_values = json.dumps(jsonable_encoder(fields))
    req = sync_battery_details(db=db, battery_id=fields.battery_id, initial_instruction=fields.initial_instruction, original_values=original_values, voltage=fields.voltage, temperature=fields.temperature, charge=fields.charge, electric_current=fields.electric_current, latitude=fields.latitude, longitude=fields.longitude, charge_status=fields.charge_status, discharge_status=fields.discharge_status, enable_status=fields.enable_status, disable_status=fields.disable_status)
    return req

@router.get("/by_id/{battery_id}", response_model=BatteryModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_id(db: Session = Depends(get_session), battery_id: int = 0):
    return get_single_battery_by_id(db=db, id=battery_id)

@router.get("/by_code/{battery_code}", response_model=BatteryModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_code(db: Session = Depends(get_session), battery_code: str = None):
    return get_single_battery_by_code(db=db, code=battery_code)
