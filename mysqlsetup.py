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

    mysql_db = get_input("Enter database name", "mydb")
    mysql_user = get_input("Enter database user", "myuser")
    mysql_password = get_input("Enter database password", "mypassword")
    mysql_root_password = get_input("Enter root password", "myrootpassword")
    container_name = get_input("Enter container name", "mysql")

    try:
        subprocess.run(
            [
                "docker", "pull", "mysql:latest"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Failed to pull the MySQL Docker image.")
        sys.exit(1)

    try:
        subprocess.run(
            [
                "docker", "run", "-d", "--name", container_name,
                "-e", f"MYSQL_DATABASE={mysql_db}",
                "-e", f"MYSQL_USER={mysql_user}",
                "-e", f"MYSQL_PASSWORD={mysql_password}",
                "-e", f"MYSQL_ROOT_PASSWORD={mysql_root_password}",
                "-p", "3306:3306",
                "mysql:latest"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print(f"MySQL container is running. Connect using: host=localhost, port=3306, dbname={mysql_db}, user={mysql_user}, password={mysql_password}")
    except subprocess.CalledProcessError:
        print("Failed to start the MySQL container.")
        sys.exit(1)

if __name__ == "__main__":
    main()
