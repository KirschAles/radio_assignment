from setuptools import setup

PROGRAM_NAME = "program"

setup(
    name=PROGRAM_NAME,
    version="1.0.0",
    # I belive that this should be string
    # will either fix or be proven wrong
    py_modules=[solution],
    entry_points={
        "console_scripts": [
            f"{PROGRAM_NAME}=solution:main",
        ],
    },
    install_requires=['tqdm']
)