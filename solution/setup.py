from setuptools import setup

PROGRAM_NAME = "program"

setup(
    name=PROGRAM_NAME,
    version="1.0.0",
    py_modules=["solution"],
    entry_points={
        "console_scripts": [
            f"{PROGRAM_NAME}=solution:main",
        ],
    },
    install_requires=['tqdm']
)