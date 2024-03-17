import logging

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.architecture_python.chapter02.database import model, schema
from src.architecture_python.chapter02.database.database import SessionLocal
from src.architecture_python.chapter02.database.repository import SqlAlchemyRepository

logger = logging.getLogger(__name__)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/allocate")
def create_allocation(
    order_line_params: list[schema.CreateOrderLine], db: Session = Depends(get_db)
):
    repository = SqlAlchemyRepository(db)
    batches = repository.list()

    lines = [
        model.OrderLine(line.orderid, line.sku, line.qty) for line in order_line_params
    ]
    
    for line in lines:
        try:
            model.allocate(line, batches)
        except model.OutOfStock as e:
            return HTTPException(500, "Out of Stock")
             
    db.commit()
    return 201


@app.get("/order-lines")
def get_order_lines(db: Session = Depends(get_db)):
    repository = SqlAlchemyRepository(db)
    return repository.list_all_orderlines()


@app.post("/batches/", response_model=schema.BatchBase)
def create_batch(batch: schema.BatchBase, db: Session = Depends(get_db)):
    repository = SqlAlchemyRepository(db)
    domain_batch = model.Batch(batch.ref, batch.sku, batch.qty, batch.eta)
    repository.add(domain_batch)
    db.commit()

    result = repository.get(batch.ref)
    logger.info(f"result: {result}, {result.to_dict()}")
    return result.to_dict()


@app.get("/batches/")
def list_batches(db: Session = Depends(get_db)):
    repository = SqlAlchemyRepository(db)
    return repository.list()
