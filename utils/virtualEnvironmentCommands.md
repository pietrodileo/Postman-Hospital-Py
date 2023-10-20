
# Python Virtual Environment

## What is a virtual environment?

A virtual environment in Python is a self-contained directory that contains its own Python interpreter and library dependencies. It allows you to isolate and manage project-specific dependencies, ensuring that different projects can have different versions of packages without interfering with each other. This isolation is particularly valuable when you're working on multiple Python projects that have distinct requirements.

## What it is useful for?

Virtual environments are useful for several reasons:

1. **Isolation:** They keep project dependencies separate, avoiding conflicts and ensuring that changes to one project don't affect others.
2. **Dependency Management:** You can install project-specific packages without affecting the global Python environment.
3. **Version Control:** You can track and manage the exact package versions required for a project by using a requirements file.
4. **Portability:** Virtual environments can be easily shared, allowing collaborators to reproduce the same environment.

## Commands

### To create a Python Virtual Environment

To create a Python virtual environment, you can use the following command:

```bash
python -m venv venv
```

This command initializes a virtual environment named "venv" in the current directory. You can replace "venv" with your desired environment name.

### To activate the environment on VSC (Windows)

Activate the virtual environment in Visual Studio Code (Windows) using the following command in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

This command sets up your terminal to use the virtual environment, ensuring that the Python interpreter and packages within the environment are used.

### To install requirements from a requirements file

You can install the project-specific requirements from a requirements file using the following command:

```
pip install -r requirements.txt
```

This command reads the package names and versions from the `requirements.txt` file and installs them into the virtual environment. It's an essential step to ensure that your project has the required dependencies.

### To create a requirements file

You can create a requirements file to document the packages and their versions used in your project with the following command:

```
pip freeze > requirements.txt
```

This command generates a `requirements.txt` file containing a list of installed packages along with their versions. It's a good practice for managing dependencies and allows others to easily recreate the same environment.

### To quit the environment

To deactivate the virtual environment and return to the global Python environment, use the following command:

```bash
deactivate
```

This command ensures that you exit the virtual environment, and your terminal returns to using the system-wide Python interpreter and packages.
