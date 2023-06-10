import os
import subprocess
import sys

def check_dependencies():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Docker is required. Please install it first.")
        sys.exit(1)

def get_input(prompt, default_value):
    value = input(f"{prompt} [{default_value}]: ").strip()
    return value if value else default_value

def main():
    check_dependencies()

    postgres_db = get_input("Enter database name", "mydb")
    postgres_user = get_input("Enter database user", "myuser")
    postgres_password = get_input("Enter database password", "mypassword")
    container_name = get_input("Enter container name", "mypostgres")

    print("This will take couple of minutes...")

    try:
        subprocess.run(
            [
                "docker", "pull", "postgres:latest"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Failed to pull the PostgreSQL Docker image.")
        sys.exit(1)

    try:
        subprocess.run(
            [
                "docker", "run", "-d", "--name", container_name,
                "-e", f"POSTGRES_DB={postgres_db}",
                "-e", f"POSTGRES_USER={postgres_user}",
                "-e", f"POSTGRES_PASSWORD={postgres_password}",
                "-p", "5432:5432",
                "postgres:latest"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print(f"PostgreSQL container is running. Connect using: host=localhost, port=5432, dbname={postgres_db}, user={postgres_user}, password={postgres_password}")
    except subprocess.CalledProcessError:
        print("Failed to start the PostgreSQL container.")
        sys.exit(1)

if __name__ == "__main__":
    main()
