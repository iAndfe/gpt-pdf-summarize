import pkg_resources

required_packages = None
with open("requirements.txt", "r") as file:
    required_packages = [line.strip() for line in file]

for package in required_packages:
    try:
        pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        raise ModuleNotFoundError(f"Package '{package}' is missing from the virtual environment.")