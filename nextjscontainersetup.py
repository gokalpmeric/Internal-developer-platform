import os
import subprocess
import sys

def check_dependencies():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Docker is required. Please install it first.")
        sys.exit(1)

def get_input(prompt):
    value = input(f"{prompt}: ").strip()
    return value

def main():
    check_dependencies()

    project_directory = get_input("Enter the Next.js project directory")
    node_version = get_input("Enter the Node.js version")

    os.chdir(project_directory)

    dockerfile_content = f"""\
FROM node:{node_version}

EXPOSE 8080

WORKDIR /app

COPY . .

CMD ["yarn", "start"]
"""
    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    image_name = "nextjs_project"
    try:
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        print("Docker image built successfully.")
    except subprocess.CalledProcessError:
        print("Failed to build the Docker image.")
        sys.exit(1)

    try:
        subprocess.run(["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", image_name, "npm", "install"], check=True)
        subprocess.run(["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", image_name, "npm", "run", "build"],
                       check=True)
        print("Next.js project built successfully.")
    except subprocess.CalledProcessError:
        print("Failed to build the Next.js project.")
        sys.exit(1)


if __name__ == "__main__":
    main()
