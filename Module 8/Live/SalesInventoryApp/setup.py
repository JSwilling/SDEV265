from setuptools import setup, find_packages

setup(
    name="SalesInventoryApp",
    version="1.0.0",
    description="Sales Inventory Management Application",
    author="Your Name",
    packages=find_packages(include=["app", "app.*"]),
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "pygame",
        "pillow"
    ],
    entry_points={
        "console_scripts": [
            "sales_inventory_app=main:main",
        ],
    },
)
