from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date, time



class BookCategory(SQLModel, table=True):
    __tablename__ = "bookcategory"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Author(SQLModel, table = True):
    __tablename__ = "author"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    biography : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Publisher(SQLModel, table = True):
    __tablename__ = "publisher"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    age : int | None = Field(default = None)
    email : str | None = Field(default = None)
    phone : int | None = Field(default = None)
    address : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Book(SQLModel, table  = True):
    __tablename__ = "book"
    id : int | None = Field(primary_key = True)
    bookCategory_id : int | None = Field(foreign_key  = "bookcategory.id")
    bookcategory : BookCategory = Relationship()
    author_id : int | None = Field(foreign_key  = "author.id")
    author : Author = Relationship()
    publisher_id :  int | None = Field(foreign_key  = "publisher.id")
    publisher : Publisher = Relationship()
    title : str | None = Field(default = None)
    edition : str | None = Field(default = None)
    language : str | None = Field(default = None)
    publication_year : int | None = Field(default = None)
    total_copies : int | None = Field(default = None)
    available_copies: int | None = Field(default = None)
    shelf_no : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class BookCopy(SQLModel, table = True):
    __tabelname__ = "bookcopy"
    id : int | None = Field(primary_key = True)
    book_id : int | None = Field(foreign_key  = "book.id")
    book : Book =  Relationship()
    barcode : str | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class BookIssue(SQLModel, table = True):
    __tablename__ = "bookissue"
    id : int | None = Field(primary_key = True)
    bookCopy_id : int | None = Field(foreign_key  = "bookcopy.id")
    bookCopy : BookCopy =  Relationship()
    user_id : int
    issue_date : date | None = Field(default = None)
    due_date : date | None = Field(default = None)
    return_date : date | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Reservation(SQLModel, table = True):
    __tablename__ = "reservation"
    id : int | None = Field(primary_key = True)
    bookCopy_id : int | None = Field(foreign_key  = "bookcopy.id")
    bookCopy : BookCopy =  Relationship()
    user_id : int
    reservation_date : date | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Fine(SQLModel, table = True):
    __tablename__ = "fines"
    id : int | None = Field(primary_key = True)
    bookIssue_id : int | None = Field(foreign_key  = "bookissue.id")
    bookIssue : BookIssue =  Relationship()
    amount : float | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)
