from setuptools import setup
from solution import PROGRAM_NAME
from solution import VERSION

setup(
    name=PROGRAM_NAME,
    version=VERSION,
    py_modules=["solution"],
    entry_points={
        "console_scripts": [
            f"{PROGRAM_NAME}=solution:main",
        ],
    },
    install_requires=['tqdm']
)