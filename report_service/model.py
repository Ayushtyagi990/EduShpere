from sqlmodel import Field, Relationship, SQLModel
from datetime import date, datetime


class ReportType(SQLModel, table=True):
    """ storing report type information, e.g. fee_collection, pending_fees """
    __tablename__ = "report_type"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    code : str | None = Field(default = None)
    description : str | None = Field(default = None)
    is_active : bool = Field(default = True)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)



class Report(SQLModel, table=True):
    """ storing generated report information """
    __tablename__ = "report"
    id : int | None = Field(primary_key = True)
    report_type_id : int | None = Field(foreign_key = "report_type.id")
    report_type : ReportType  = Relationship()
    title : str | None = Field(default = None)
    academic_year_id : int | None = Field(default = None)
    program_id : int | None = Field(default = None)
    date_from : date | None = Field(default = None)
    date_to : date | None = Field(default = None)
    file_format : str | None = Field(default = None) 
    status : str | None = Field(default = "pending", index = True)  
    file_path : str | None = Field(default = None)
    file_size : int | None = Field(default = None)
    error_message : str | None = Field(default = None)
    generated_by : int | None = Field(default = None)
    completed_at : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class ReportSchedule(SQLModel, table=True):
    """ storing recurring report schedule information """
    __tablename__ = "report_schedule"
    id : int | None = Field(primary_key = True)
    report_type_id : int | None = Field(foreign_key = "report_type.id")
    report_type : ReportType | None = Relationship()
    name : str | None = Field(default = None)
    frequency : str | None = Field(default = None) 
    file_format : str | None = Field(default = None)  
    academic_year_id : int | None = Field(default = None)
    program_id : int | None = Field(default = None)
    recipients : str | None = Field(default = None)  
    is_active : bool = Field(default = True)
    last_run_at : datetime | None = Field(default = None)
    next_run_at : datetime | None = Field(default = None, index = True)
    created_by : int | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

   


class ReportDownload(SQLModel, table=True):
    """ storing report download log information """
    __tablename__ = "report_download"
    id : int | None = Field(primary_key = True)
    report_id : int | None = Field(foreign_key = "report.id")
    report : Report = Relationship()
    downloaded_by : int | None = Field(default = None)
    downloaded_at : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

   