from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import List

import models
import schemas
from database import SessionLocal, init_db, engine

app = FastAPI()

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    addresses = db.query(models.Address).offset(skip).limit(limit).all()
    return addresses


@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address


@app.get("/addresses/within/", response_model=List[schemas.Address])
def get_addresses_within(latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)):
    addresses = db.query(models.Address).all()
    center = (latitude, longitude)
    nearby_addresses = [
        address for address in addresses
        if geodesic(center, (address.latitude, address.longitude)).km <= distance
    ]
    return nearby_addresses

