from setuptools import find_packages,setup

HYPHEN_DOT_E = "-e ."
def get_requirements(text_file):
    with open(text_file,"r") as file:
        requirements = file.read().splitlines()

    if HYPHEN_DOT_E in requirements:
        requirements.remove(HYPHEN_DOT_E)

    return requirements


setup(
    name= "SQL Agent",
    version= "0.0.0.1",
    description= "This app helps the user to write sql query",
    long_description= "A user friendly app is created to write sql query and give output in the layman term",
    author= "Deepak Pawar",
    author_email="deepakpw234@gmail.com",
    packages = find_packages(),
    install_req = get_requirements("requirements.txt")
)