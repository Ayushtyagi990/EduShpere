#!/usr/bin/env python3
"""
All-in-one microservices manager
- Creates FastAPI structure for all services
- Starts all services on unique ports
- Manages service lifecycle
"""

import subprocess
import os
import sys
import time
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Service to Port mapping
SERVICES = {
    "api_gateway": {"port": 8000, "with_db": True},
    "users_service": {"port": 8001, "with_db": True},
    "academic_service": {"port": 8002, "with_db": True},
    "accounts_service": {"port": 8003, "with_db": True},
    "analytics_service": {"port": 8004, "with_db": True},
    "attendance_service": {"port": 8005, "with_db": True},
    "doucment_service": {"port": 8006, "with_db": True},
    "examination_service": {"port": 8007, "with_db": True},
    "inventory_service": {"port": 8008, "with_db": True},
    "leave_service": {"port": 8009, "with_db": True},
    "library_service": {"port": 8010, "with_db": True},
    "notification_service": {"port": 8011, "with_db": True},
    "timetable_service": {"port": 8012, "with_db": True},
    
}    

processes = {}
failed_services = set()


# ==================== FILE CREATION FUNCTIONS ====================

def create_main_py(service_name, port, with_db=True):
    """Create main.py for FastAPI service"""
    if with_db:
        return f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import os
from database import init_db

# FastAPI app
app = FastAPI(
    title="{service_name}",
    description="Microservice for {service_name}",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={{"check_same_thread": False}} if "sqlite" in DATABASE_URL else {{}},
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
)

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db(engine)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "service": "{service_name}"}}

@app.get("/")
def root():
    """Root endpoint"""
    return {{"message": "Welcome to {service_name}", "version": "1.0.0"}}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", {port}))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
'''
    else:
        # API Gateway without database
        return f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# FastAPI app
app = FastAPI(
    title="{service_name}",
    description="API Gateway for routing requests",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "service": "{service_name}"}}

@app.get("/")
def root():
    """Root endpoint"""
    return {{"message": "Welcome to {service_name}", "version": "1.0.0"}}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", {port}))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
'''


def create_database_py():
    """Create database.py for database initialization"""
    return '''from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

def init_db(engine):
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def get_session(engine):
    """Get database session"""
    SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
    with SessionLocal() as session:
        yield session
'''


def create_model_py():
    """Create model.py with base models"""
    return '''from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Base(SQLModel):
    """Base model for all entities"""
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

# Add your models here
# Example:
# class User(Base, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     email: str = Field(unique=True)
'''


def create_pyproject_toml(service_name):
    """Create pyproject.toml for the service"""
    return f'''[tool.poetry]
name = "{service_name}"
version = "1.0.0"
description = "Microservice for {service_name}"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{{include = "."}}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.104.0"
uvicorn = {{version = "^0.24.0", extras = ["standard"]}}
sqlmodel = "^0.0.14"
pydantic = "^2.0.0"
python-dotenv = "^1.0.0"
sqlalchemy = "^2.0.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
black = "^23.0.0"
pylint = "^3.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
'''


def setup_service_files(service_name, port, with_db=True):
    """Create FastAPI service files"""
    service_dir = os.path.join(BASE_DIR, service_name)
    
    # Create directory if it doesn't exist
    if not os.path.exists(service_dir):
        os.makedirs(service_dir)
    
    # Create main.py
    main_file = os.path.join(service_dir, "main.py")
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write(create_main_py(service_name, port, with_db))
        return True
    return False


def setup_all_services():
    """Setup all FastAPI services"""
    print("\n📦 Setting up FastAPI services...\n")
    
    created_count = 0
    for service_name, config in SERVICES.items():
        if setup_service_files(service_name, config["port"], config["with_db"]):
            created_count += 1
            print(f"✅ Created: {service_name}/main.py")
    
    if created_count == 0:
        print("⏭️  All services already set up!")
    else:
        print(f"\n✅ {created_count} new services created!")


# ==================== SERVICE STARTUP FUNCTIONS ====================

def start_service(service_name, port):
    """Start a single microservice"""
    service_dir = os.path.join(BASE_DIR, service_name)
    
    if not os.path.exists(service_dir):
        print(f" {service_name}: Directory not found at {service_dir}")
        failed_services.add(service_name)
        return
    
    # Check if main.py exists
    main_file = os.path.join(service_dir, "main.py")
    if not os.path.exists(main_file):
        print(f"⏭️  {service_name}: Skipped (no main.py found)")
        failed_services.add(service_name)
        return
    
    try:
        # Start the service with poetry and uvicorn on specified port
        process = subprocess.Popen(
            ["poetry", "run", "uvicorn", "main:app", "--reload", "--port", str(port)],
            cwd=service_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes[service_name] = process
        print(f"✅ {service_name}: Started (PID: {process.pid}) → http://localhost:{port}")
    except Exception as e:
        print(f" {service_name}: Failed to start - {str(e)}")
        failed_services.add(service_name)


def start_all_services():
    """Start all microservices"""
    print("\n🚀 Starting all microservices...\n")
    
    for service_name, config in SERVICES.items():
        start_service(service_name, config["port"])
        time.sleep(0.5)  # Small delay between starting services
    
    print(f"\n{'='*70}")
    print(f"✅ All {len(processes)} services started!")
    print(f"{'='*70}\n")
    
    print("📝 Service URLs:\n")
    for service_name, config in SERVICES.items():
        if service_name in processes:
            print(f"   • {service_name:40} http://localhost:{config['port']:5}/docs")
    
    print(f"\n{'='*70}")
    print("Press Ctrl+C to stop all services...")
    print(f"{'='*70}\n")


def monitor_services():
    """Monitor running services"""
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has terminated
            for service_name, process in list(processes.items()):
                if process.poll() is not None:
                    if service_name not in failed_services:
                        failed_services.add(service_name)
                        print(f"\n {service_name}: Process terminated (exit code: {process.returncode})")
                        
                        # Try to read error output
                        try:
                            stdout, _ = process.communicate(timeout=1)
                            if stdout:
                                print(f"   Error output:\n{stdout[-500:]}")  # Last 500 chars
                        except:
                            pass
    
    except KeyboardInterrupt:
        stop_all_services()


def stop_all_services():
    """Stop all running services"""
    print("\n\n🛑 Stopping all services...\n")
    
    # Terminate all processes
    for service_name, process in processes.items():
        try:
            process.terminate()
            print(f"⏹️  {service_name}: Stopped")
        except:
            pass
    
    # Wait for all processes to terminate
    time.sleep(2)
    
    # Kill any remaining processes
    for service_name, process in processes.items():
        if process.poll() is None:
            try:
                process.kill()
            except:
                pass
    
    print("\n✅ All services stopped.")
    sys.exit(0)


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🏥 HOSPITAL MANAGEMENT MICROSERVICES - ALL-IN-ONE LAUNCHER")
    print("="*70)
    
    # Step 1: Setup all services
    setup_all_services()
    
    # Step 2: Start all services
    start_all_services()
    
    # Step 3: Monitor services
    monitor_services()


if __name__ == "__main__":
    main()

