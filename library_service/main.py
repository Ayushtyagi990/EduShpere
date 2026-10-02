from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import BookCategory, Author, Publisher, Book, BookCopy, BookIssue, Reservation, Fine
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

DEFAULT_LOAN_DAYS = 14
FINE_PER_DAY = 5.0


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


# --------------------------------------------------------------------------
# BookCategory
# --------------------------------------------------------------------------
@app.post("/book-category")
def create_book_category(
    book_category: BookCategory,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    book_category.created_at = datetime.now()
    book_category.updated_at = datetime.now()
    session.add(book_category)
    session.commit()
    session.refresh(book_category)
    return book_category


@app.get("/book-category")
def get_book_categories(session: Session = Depends(get_session)):
    return session.exec(select(BookCategory)).all()


@app.get("/book-category/{book_category_id}")
def get_book_category_by_id(book_category_id: int, session: Session = Depends(get_session)):
    book_category = session.get(BookCategory, book_category_id)
    if not book_category:
        raise HTTPException(status_code=404, detail="Book category not found")
    return book_category


@app.put("/book-category/{book_category_id}")
def update_book_category_by_id(book_category_id: int, data: BookCategory, session: Session = Depends(get_session)):
    book_category = session.get(BookCategory, book_category_id)
    if not book_category:
        raise HTTPException(status_code=404, detail="Book category not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(book_category, key, value)
    book_category.updated_at = datetime.now()

    session.commit()
    session.refresh(book_category)
    return book_category


@app.delete("/book-category/{book_category_id}", status_code=204)
def delete_book_category_by_id(book_category_id: int, session: Session = Depends(get_session)):
    book_category = session.get(BookCategory, book_category_id)
    if not book_category:
        raise HTTPException(status_code=404, detail="Book category not found")
    session.delete(book_category)
    session.commit()
    return {"details": f"book category {book_category_id} deleted"}


# --------------------------------------------------------------------------
# Author
# --------------------------------------------------------------------------
@app.post("/author")
def create_author(
    author: Author,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    author.created_at = datetime.now()
    author.updated_at = datetime.now()
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/author")
def get_authors(session: Session = Depends(get_session)):
    return session.exec(select(Author)).all()


@app.get("/author/{author_id}")
def get_author_by_id(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.put("/author/{author_id}")
def update_author_by_id(author_id: int, data: Author, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(author, key, value)
    author.updated_at = datetime.now()

    session.commit()
    session.refresh(author)
    return author


@app.delete("/author/{author_id}", status_code=204)
def delete_author_by_id(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"details": f"author {author_id} deleted"}


# --------------------------------------------------------------------------
# Publisher
# --------------------------------------------------------------------------
@app.post("/publisher")
def create_publisher(
    publisher: Publisher,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    publisher.created_at = datetime.now()
    publisher.updated_at = datetime.now()
    session.add(publisher)
    session.commit()
    session.refresh(publisher)
    return publisher


@app.get("/publisher")
def get_publishers(session: Session = Depends(get_session)):
    return session.exec(select(Publisher)).all()


@app.get("/publisher/{publisher_id}")
def get_publisher_by_id(publisher_id: int, session: Session = Depends(get_session)):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


@app.put("/publisher/{publisher_id}")
def update_publisher_by_id(publisher_id: int, data: Publisher, session: Session = Depends(get_session)):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(publisher, key, value)
    publisher.updated_at = datetime.now()

    session.commit()
    session.refresh(publisher)
    return publisher


@app.delete("/publisher/{publisher_id}", status_code=204)
def delete_publisher_by_id(publisher_id: int, session: Session = Depends(get_session)):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    session.delete(publisher)
    session.commit()
    return {"details": f"publisher {publisher_id} deleted"}


# --------------------------------------------------------------------------
# Book
# --------------------------------------------------------------------------
@app.post("/book")
def create_book(
    book: Book,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if book.bookCategory_id is not None and not session.get(BookCategory, book.bookCategory_id):
        raise HTTPException(status_code=404, detail="Book category not found")
    if book.author_id is not None and not session.get(Author, book.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    if book.publisher_id is not None and not session.get(Publisher, book.publisher_id):
        raise HTTPException(status_code=404, detail="Publisher not found")

    book.total_copies = book.total_copies or 0
    book.available_copies = book.available_copies if book.available_copies is not None else book.total_copies
    book.created_at = datetime.now()
    book.updated_at = datetime.now()

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/book")
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@app.get("/book/{book_id}")
def get_book_by_id(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/book/{book_id}")
def update_book_by_id(book_id: int, data: Book, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(book, key, value)
    book.updated_at = datetime.now()

    session.commit()
    session.refresh(book)
    return book


@app.delete("/book/{book_id}", status_code=204)
def delete_book_by_id(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"details": f"book {book_id} deleted"}


# --------------------------------------------------------------------------
# BookCopy
# --------------------------------------------------------------------------
@app.post("/book-copy")
def create_book_copy(
    book_copy: BookCopy,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    book = session.get(Book, book_copy.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_copy.status = book_copy.status or "available"
    book_copy.created_at = datetime.now()
    book_copy.updated_at = datetime.now()
    session.add(book_copy)
    try:
        session.commit()
        session.refresh(book_copy)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to create book copy with these details")

    # A new physical copy grows the book's totals.
    book.total_copies = (book.total_copies or 0) + 1
    if book_copy.status == "available":
        book.available_copies = (book.available_copies or 0) + 1
    book.updated_at = datetime.now()
    session.add(book)
    session.commit()

    return book_copy


@app.get("/book-copy")
def get_book_copies(session: Session = Depends(get_session)):
    return session.exec(select(BookCopy)).all()


@app.get("/book-copy/{book_copy_id}")
def get_book_copy_by_id(book_copy_id: int, session: Session = Depends(get_session)):
    book_copy = session.get(BookCopy, book_copy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    return book_copy


@app.put("/book-copy/{book_copy_id}")
def update_book_copy_by_id(book_copy_id: int, data: BookCopy, session: Session = Depends(get_session)):
    book_copy = session.get(BookCopy, book_copy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(book_copy, key, value)
    book_copy.updated_at = datetime.now()

    session.commit()
    session.refresh(book_copy)
    return book_copy


@app.delete("/book-copy/{book_copy_id}", status_code=204)
def delete_book_copy_by_id(book_copy_id: int, session: Session = Depends(get_session)):
    book_copy = session.get(BookCopy, book_copy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    session.delete(book_copy)
    session.commit()
    return {"details": f"book copy {book_copy_id} deleted"}


# --------------------------------------------------------------------------
# BookIssue
# --------------------------------------------------------------------------
@app.post("/book-issue")
def create_book_issue(
    book_issue: BookIssue,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    book_copy = session.get(BookCopy, book_issue.bookCopy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    if book_copy.status != "available":
        raise HTTPException(status_code=409, detail="This copy is not available to issue")

    book_issue.user_id = book_issue.user_id or payload.get("id")
    book_issue.issue_date = book_issue.issue_date or datetime.now().date()
    book_issue.due_date = book_issue.due_date or (book_issue.issue_date + timedelta(days=DEFAULT_LOAN_DAYS))
    book_issue.status = "issued"
    book_issue.created_at = datetime.now()
    book_issue.updated_at = datetime.now()

    session.add(book_issue)
    try:
        session.commit()
        session.refresh(book_issue)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to issue this copy")

    book_copy.status = "issued"
    book_copy.updated_at = datetime.now()
    session.add(book_copy)

    book = session.get(Book, book_copy.book_id)
    if book and book.available_copies:
        book.available_copies -= 1
        book.updated_at = datetime.now()
        session.add(book)

    session.commit()
    return book_issue


@app.get("/book-issue")
def get_book_issues(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    issues = session.exec(select(BookIssue)).all()
    return {"user": payload, "book_issues": issues}


@app.get("/book-issue/{book_issue_id}")
def get_book_issue_by_id(book_issue_id: int, session: Session = Depends(get_session)):
    book_issue = session.get(BookIssue, book_issue_id)
    if not book_issue:
        raise HTTPException(status_code=404, detail="Book issue not found")
    return book_issue


@app.get("/book-issue/user/{user_id}")
def get_book_issues_by_user(user_id: int, session: Session = Depends(get_session)):
    return session.exec(select(BookIssue).where(BookIssue.user_id == user_id)).all()


@app.post("/book-issue/{book_issue_id}/return")
def return_book_issue(
    book_issue_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """Marks a copy returned, frees it up, and raises a Fine if it came back late."""
    book_issue = session.get(BookIssue, book_issue_id)
    if not book_issue:
        raise HTTPException(status_code=404, detail="Book issue not found")
    if book_issue.status == "returned":
        raise HTTPException(status_code=409, detail="This issue has already been returned")

    book_issue.return_date = datetime.now().date()
    book_issue.status = "returned"
    book_issue.updated_at = datetime.now()
    session.add(book_issue)
    session.commit()
    session.refresh(book_issue)

    book_copy = session.get(BookCopy, book_issue.bookCopy_id)
    fine = None
    if book_copy:
        book_copy.status = "available"
        book_copy.updated_at = datetime.now()
        session.add(book_copy)

        book = session.get(Book, book_copy.book_id)
        if book:
            book.available_copies = (book.available_copies or 0) + 1
            book.updated_at = datetime.now()
            session.add(book)

    if book_issue.due_date and book_issue.return_date > book_issue.due_date:
        days_late = (book_issue.return_date - book_issue.due_date).days
        fine = Fine(
            bookIssue_id=book_issue.id,
            amount=round(days_late * FINE_PER_DAY, 2),
            status="unpaid",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(fine)

    session.commit()
    if fine:
        session.refresh(fine)

    return {"book_issue": book_issue, "fine": fine}


@app.delete("/book-issue/{book_issue_id}", status_code=204)
def delete_book_issue_by_id(book_issue_id: int, session: Session = Depends(get_session)):
    book_issue = session.get(BookIssue, book_issue_id)
    if not book_issue:
        raise HTTPException(status_code=404, detail="Book issue not found")
    session.delete(book_issue)
    session.commit()
    return {"details": f"book issue {book_issue_id} deleted"}


# --------------------------------------------------------------------------
# Reservation
# --------------------------------------------------------------------------
@app.post("/reservation")
def create_reservation(
    reservation: Reservation,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    book_copy = session.get(BookCopy, reservation.bookCopy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")

    reservation.user_id = reservation.user_id or payload.get("id")
    reservation.reservation_date = reservation.reservation_date or datetime.now().date()
    reservation.status = reservation.status or "pending"
    reservation.created_at = datetime.now()
    reservation.updated_at = datetime.now()

    session.add(reservation)
    try:
        session.commit()
        session.refresh(reservation)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to create reservation with these details")
    return reservation


@app.get("/reservation")
def get_reservations(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reservations = session.exec(select(Reservation)).all()
    return {"user": payload, "reservations": reservations}


@app.get("/reservation/{reservation_id}")
def get_reservation_by_id(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@app.put("/reservation/{reservation_id}")
def update_reservation_by_id(reservation_id: int, data: Reservation, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(reservation, key, value)
    reservation.updated_at = datetime.now()

    session.commit()
    session.refresh(reservation)
    return reservation


@app.delete("/reservation/{reservation_id}", status_code=204)
def delete_reservation_by_id(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    session.delete(reservation)
    session.commit()
    return {"details": f"reservation {reservation_id} deleted"}


# --------------------------------------------------------------------------
# Fine
# --------------------------------------------------------------------------
@app.get("/fine")
def get_fines(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    fines = session.exec(select(Fine)).all()
    return {"user": payload, "fines": fines}


@app.get("/fine/{fine_id}")
def get_fine_by_id(fine_id: int, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return fine


@app.put("/fine/{fine_id}/pay")
def pay_fine(fine_id: int, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    if fine.status == "paid":
        raise HTTPException(status_code=409, detail="This fine is already paid")

    fine.status = "paid"
    fine.updated_at = datetime.now()
    session.commit()
    session.refresh(fine)
    return fine


@app.delete("/fine/{fine_id}", status_code=204)
def delete_fine_by_id(fine_id: int, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    session.delete(fine)
    session.commit()
    return {"details": f"fine {fine_id} deleted"}