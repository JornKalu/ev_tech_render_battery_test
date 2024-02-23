from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Battery(Base):

    __tablename__ = "batteries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    type_id = Column(BigInteger, default=0)
    slot_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    code = Column(String, nullable=True)
    imei_code = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    qr_code = Column(String, nullable=True)
    voltage = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    charge = Column(String, nullable=True)
    humidity = Column(String, nullable=True)
    electric_current = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    temp_host = Column(String, nullable=True)
    is_ejected = Column(SmallInteger, default=0)
    ejected_by = Column(BigInteger, default=0)
    temp_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_battery(db: Session, type_id: int = 0, slot_id: int = 0, mobility_device_id: int = 0, code: str = None, imei_code: str = None, name: str = None, description: str = None, qr_code: str = None, voltage: str = None, temperature: str = None, charge: str = None, humidity: str = None, electric_current: str = None, latitude: str = None, longitude: str = None, temp_host: str = None, is_ejected: int = 0, ejected_by: int = 0, temp_status: int = None, status: int = 0, created_by: int = 0, updated_by: int = 0):
    bat = Battery(type_id=type_id, slot_id=slot_id, mobility_device_id=mobility_device_id, code=code, imei_code=imei_code, name=name, description=description, qr_code=qr_code, voltage=voltage, temperature=temperature, charge=charge, humidity=humidity, electric_current=electric_current, latitude=latitude, longitude=longitude, temp_host=temp_host, is_ejected=is_ejected, ejected_by=ejected_by, temp_status=temp_status, status=status, created_by=created_by, updated_by=updated_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(bat)
    db.commit()
    db.refresh(bat)
    return bat

def update_battery(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Battery).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_battery(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Battery).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_battery_by_id(db: Session, id: int=0):
    return db.query(Battery).filter_by(id = id).first()

def get_single_battery_by_code(db: Session, code: str = None):
    return db.query(Battery).filter_by(code = code).first()

def get_all_batteries(db: Session):
    return db.query(Battery).filter(Battery.deleted_at == None).order_by(desc(Battery.id))

def search_batteries(db: Session, query: str = None):
    return db.query(Battery).filter(and_(or_(Battery.code.like('%' + str(query) + '%'), Battery.name.like('%' + str(query) + '%')), Battery.deleted_at == None)).order_by(desc(Battery.id))

def count_batteries(db: Session):
    return db.query(Battery).count()

def count_batteries_by_code(db: Session, code: str = None):
    return db.query(Battery).filter_by(code = code).count()

def check_if_battery_code_exists(db: Session, code: str = None):
    count = count_batteries_by_code(db=db, code=code)
    if count > 0:
        return True
    else:
        return False