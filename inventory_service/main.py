from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import Category, Supplier, Warehouse, Item, Stock, StockMovement
from database import get_session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()

# Same signing key/algorithm as the users service, since tokens are issued
# there and only verified here.
SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc"
)

app.add_middleware(JWTMiddleware)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


# --------------------------------------------------------------------------
# Category
# --------------------------------------------------------------------------
@app.post("/category")
def create_category(
    category: Category,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    category.created_at = datetime.now()
    category.updated_at = datetime.now()
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@app.get("/category")
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


@app.get("/category/{category_id}")
def get_category_by_id(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/category/{category_id}")
def update_category_by_id(category_id: int, data: Category, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    category.updated_at = datetime.now()

    session.commit()
    session.refresh(category)
    return category


@app.delete("/category/{category_id}", status_code=204)
def delete_category_by_id(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"details": f"category {category_id} deleted"}


# --------------------------------------------------------------------------
# Supplier
# --------------------------------------------------------------------------
@app.post("/supplier")
def create_supplier(
    supplier: Supplier,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    supplier.created_at = datetime.now()
    supplier.updated_at = datetime.now()
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    return supplier


@app.get("/supplier")
def get_suppliers(session: Session = Depends(get_session)):
    return session.exec(select(Supplier)).all()


@app.get("/supplier/{supplier_id}")
def get_supplier_by_id(supplier_id: int, session: Session = Depends(get_session)):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@app.put("/supplier/{supplier_id}")
def update_supplier_by_id(supplier_id: int, data: Supplier, session: Session = Depends(get_session)):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(supplier, key, value)
    supplier.updated_at = datetime.now()

    session.commit()
    session.refresh(supplier)
    return supplier


@app.delete("/supplier/{supplier_id}", status_code=204)
def delete_supplier_by_id(supplier_id: int, session: Session = Depends(get_session)):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    session.delete(supplier)
    session.commit()
    return {"details": f"supplier {supplier_id} deleted"}


# --------------------------------------------------------------------------
# Warehouse
# --------------------------------------------------------------------------
@app.post("/warehouse")
def create_warehouse(
    warehouse: Warehouse,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    warehouse.created_at = datetime.now()
    warehouse.updated_at = datetime.now()
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse


@app.get("/warehouse")
def get_warehouses(session: Session = Depends(get_session)):
    return session.exec(select(Warehouse)).all()


@app.get("/warehouse/{warehouse_id}")
def get_warehouse_by_id(warehouse_id: int, session: Session = Depends(get_session)):
    warehouse = session.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse


@app.put("/warehouse/{warehouse_id}")
def update_warehouse_by_id(warehouse_id: int, data: Warehouse, session: Session = Depends(get_session)):
    warehouse = session.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(warehouse, key, value)
    warehouse.updated_at = datetime.now()

    session.commit()
    session.refresh(warehouse)
    return warehouse


@app.delete("/warehouse/{warehouse_id}", status_code=204)
def delete_warehouse_by_id(warehouse_id: int, session: Session = Depends(get_session)):
    warehouse = session.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    session.delete(warehouse)
    session.commit()
    return {"details": f"warehouse {warehouse_id} deleted"}


# --------------------------------------------------------------------------
# Item
# --------------------------------------------------------------------------
@app.post("/item")
def create_item(
    item: Item,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if item.category_id is not None and not session.get(Category, item.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    if item.supplier_id is not None and not session.get(Supplier, item.supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")

    item.created_at = datetime.now()
    item.updated_at = datetime.now()
    session.add(item)
    try:
        session.commit()
        session.refresh(item)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Item with this SKU already exists")
    return item


@app.get("/item")
def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()


@app.get("/item/{item_id}")
def get_item_by_id(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/item/{item_id}/stock")
def get_item_stock(item_id: int, session: Session = Depends(get_session)):
    """Total quantity currently on hand for this item across all warehouses."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    stocks = session.exec(select(Stock).where(Stock.item_id == item_id)).all()
    total = sum(s.quantity or 0 for s in stocks)
    reserved = sum(s.reserved_quantity or 0 for s in stocks)
    return {
        "item_id": item_id,
        "total_quantity": total,
        "reserved_quantity": reserved,
        "available_quantity": total - reserved,
        "by_warehouse": stocks,
    }


@app.put("/item/{item_id}")
def update_item_by_id(item_id: int, data: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    item.updated_at = datetime.now()

    session.commit()
    session.refresh(item)
    return item


@app.delete("/item/{item_id}", status_code=204)
def delete_item_by_id(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"details": f"item {item_id} deleted"}


# --------------------------------------------------------------------------
# Stock
# --------------------------------------------------------------------------
@app.post("/stock")
def create_stock(
    stock: Stock,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not session.get(Item, stock.item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not session.get(Warehouse, stock.warehouse_id):
        raise HTTPException(status_code=404, detail="Warehouse not found")

    stock.quantity = stock.quantity or 0
    stock.reserved_quantity = stock.reserved_quantity or 0
    stock.created_at = datetime.now()
    stock.updated_at = datetime.now()
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


@app.get("/stock")
def get_stocks(session: Session = Depends(get_session)):
    return session.exec(select(Stock)).all()


@app.get("/stock/{stock_id}")
def get_stock_by_id(stock_id: int, session: Session = Depends(get_session)):
    stock = session.get(Stock, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@app.put("/stock/{stock_id}")
def update_stock_by_id(stock_id: int, data: Stock, session: Session = Depends(get_session)):
    stock = session.get(Stock, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(stock, key, value)
    stock.updated_at = datetime.now()

    session.commit()
    session.refresh(stock)
    return stock


@app.delete("/stock/{stock_id}", status_code=204)
def delete_stock_by_id(stock_id: int, session: Session = Depends(get_session)):
    stock = session.get(Stock, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    session.delete(stock)
    session.commit()
    return {"details": f"stock {stock_id} deleted"}


# --------------------------------------------------------------------------
# StockMovement
# --------------------------------------------------------------------------
def _get_or_create_stock(session: Session, item_id: int, warehouse_id: int) -> Stock:
    stock = session.exec(
        select(Stock).where(Stock.item_id == item_id, Stock.warehouse_id == warehouse_id)
    ).first()
    if not stock:
        stock = Stock(
            item_id=item_id,
            warehouse_id=warehouse_id,
            quantity=0,
            reserved_quantity=0,
            created_at=datetime.now(),
        )
    return stock


@app.post("/stock-movement")
def create_stock_movement(
    stock_movement: StockMovement,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not session.get(Item, stock_movement.item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not session.get(Warehouse, stock_movement.warehouse_id):
        raise HTTPException(status_code=404, detail="Warehouse not found")
    if not stock_movement.quantity or stock_movement.quantity <= 0:
        raise HTTPException(status_code=400, detail="quantity must be greater than zero")
    if stock_movement.movement_type not in ("in", "out"):
        raise HTTPException(
            status_code=400,
            detail="movement_type must be 'in' or 'out' (there is only one warehouse_id on this "
                   "model, so a 'transfer' between two warehouses can't be represented as a single "
                   "movement row — record it as an 'out' movement from the source warehouse plus an "
                   "'in' movement to the destination warehouse)",
        )

    stock = _get_or_create_stock(session, stock_movement.item_id, stock_movement.warehouse_id)

    if stock_movement.movement_type == "in":
        stock.quantity = (stock.quantity or 0) + stock_movement.quantity
    else:  # "out"
        available = (stock.quantity or 0) - (stock.reserved_quantity or 0)
        if stock_movement.quantity > available:
            raise HTTPException(status_code=409, detail="Not enough available stock for this movement")
        stock.quantity = (stock.quantity or 0) - stock_movement.quantity

    stock.updated_at = datetime.now()
    session.add(stock)

    stock_movement.movement_date = stock_movement.movement_date or datetime.now()
    stock_movement.performed_by = stock_movement.performed_by or payload.get("id")
    stock_movement.created_at = datetime.now()
    stock_movement.updated_at = datetime.now()

    session.add(stock_movement)
    try:
        session.commit()
        session.refresh(stock_movement)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to record stock movement with these details")
    return stock_movement


@app.get("/stock-movement")
def get_stock_movements(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    movements = session.exec(select(StockMovement)).all()
    return {"user": payload, "stock_movements": movements}


@app.get("/stock-movement/{stock_movement_id}")
def get_stock_movement_by_id(stock_movement_id: int, session: Session = Depends(get_session)):
    movement = session.get(StockMovement, stock_movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return movement


@app.get("/stock-movement/item/{item_id}")
def get_stock_movements_by_item(item_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(StockMovement)
        .where(StockMovement.item_id == item_id)
        .order_by(StockMovement.movement_date)
    ).all()


@app.delete("/stock-movement/{stock_movement_id}", status_code=204)
def delete_stock_movement_by_id(stock_movement_id: int, session: Session = Depends(get_session)):
    """Deletes the ledger row only — does not reverse its effect on Stock,
    since that would let history be silently rewritten. Post an offsetting
    movement instead if a correction is needed."""
    movement = session.get(StockMovement, stock_movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    session.delete(movement)
    session.commit()
    return {"details": f"stock movement {stock_movement_id} deleted"}