#!/usr/bin/env python3

import os
import sys
import time
import threading
import subprocess

# Base directory where all services are located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Service -> Port mapping
SERVICES = {
    "api_gateway": 8000,
    "users_service": 8001,
    "academic_service": 8002,
    "accounts_service": 8003,
    "analytics_service": 8004,
    "attendance_service": 8005,
    "doucment_service": 8006,
    "examination_service": 8007,
    "inventory_service": 8008,
    "leave_service": 8009,
    "library_service": 8010,
    "notification_service": 8011,
    "timetable_service": 8012,

}

processes = {}
failed_services = set()


def stream_logs(service_name, process):
    """
    Continuously stream logs from the service.
    """
    try:
        for line in iter(process.stdout.readline, ""):
            if line:
                print(f"[{service_name}] {line}", end="")
    except Exception as e:
        print(f"[{service_name}] Log reader error: {e}")


def start_service(service_name, port):
    """
    Start a single microservice.
    """

    service_dir = os.path.join(BASE_DIR, service_name)

    if not os.path.isdir(service_dir):
        print(f"❌ {service_name}: Directory not found")
        failed_services.add(service_name)
        return

    main_file = os.path.join(service_dir, "main.py")

    if not os.path.isfile(main_file):
        print(f"⏭ {service_name}: main.py not found")
        failed_services.add(service_name)
        return

    try:
        process = subprocess.Popen(
            [
                "poetry",
                "run",
                "uvicorn",
                "main:app",
                "--reload",
                "--port",
                str(port),
            ],
            cwd=service_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        processes[service_name] = process

        threading.Thread(
            target=stream_logs,
            args=(service_name, process),
            daemon=True,
        ).start()

        print(
            f"✅ {service_name}: Started "
            f"(PID {process.pid}) "
            f"http://localhost:{port}"
        )

    except Exception as e:
        print(f"❌ {service_name}: {e}")
        failed_services.add(service_name)


def stop_all():
    print("\nStopping all services...\n")

    for service_name, process in processes.items():
        if process.poll() is None:
            try:
                process.terminate()
            except Exception:
                pass

    time.sleep(2)

    for service_name, process in processes.items():
        if process.poll() is None:
            try:
                process.kill()
            except Exception:
                pass

    print("✅ All services stopped.")


def main():

    print("=" * 70)
    print("Starting Microservices")
    print("=" * 70)

    for service_name, port in SERVICES.items():
        start_service(service_name, port)
        time.sleep(0.5)

    print("\n" + "=" * 70)
    print("Service URLs")
    print("=" * 70)

    for service_name, port in SERVICES.items():
        if service_name in processes:
            print(f"{service_name:<40} http://localhost:{port}/docs")

    print("\nPress Ctrl+C to stop all services.\n")

    try:

        while True:

            time.sleep(1)

            for service_name in list(processes.keys()):

                process = processes[service_name]

                if process.poll() is not None:

                    if service_name not in failed_services:

                        failed_services.add(service_name)

                        print(
                            f"\n❌ {service_name} exited "
                            f"(exit code {process.returncode})"
                        )

    except KeyboardInterrupt:

        stop_all()
        sys.exit(0)


if __name__ == "__main__":
    main()
    