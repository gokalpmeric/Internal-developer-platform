import subprocess
import sys

def check_dependencies():
    try:
        subprocess.run(["oc"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("The 'oc' command-line tool is required. Please install it first.")
        sys.exit(1)

def get_input(prompt):
    value = input(f"{prompt}: ").strip()
    return value

def main():
    check_dependencies()

    openshift_server = get_input("Enter the OpenShift server URL")
    login_method = get_input("Enter '1' for login with token or '2' for login with username/password")

    if login_method == "1":
        token = get_input("Enter the OpenShift token")
        login_cmd = ["oc", "login", openshift_server, "--token", token]
    else:
        openshift_username = get_input("Enter the OpenShift username")
        openshift_password = get_input("Enter the OpenShift password")
        login_cmd = ["oc", "login", openshift_server, "--username", openshift_username, "--password", openshift_password]

    project_name = get_input("Enter the project name")
    elasticsearch_service = get_input("Enter the Elasticsearch service name")
    local_port = get_input("Enter the local port to forward to Elasticsearch")

    try:
        subprocess.run(login_cmd, check=True)
        print("Logged into OpenShift successfully.")
    except subprocess.CalledProcessError:
        print("Failed to log into OpenShift.")
        sys.exit(1)

    try:
        subprocess.run(["oc", "project", project_name], check=True)
        print(f"Switched to project '{project_name}' successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to switch to project '{project_name}'.")
        sys.exit(1)

    try:
        subprocess.run(["oc", "port-forward", f"svc/{elasticsearch_service}", f"{local_port}:9200"])
        print(f"Port forwarding Elasticsearch service to localhost:{local_port}...")
    except subprocess.CalledProcessError:
        print("Failed to port forward the Elasticsearch service.")
        sys.exit(1)

if __name__ == "__main__":
    main()
