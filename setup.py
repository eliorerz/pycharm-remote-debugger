import os
import sys

import setuptools

ROOT = os.path.dirname(__file__)

if sys.version_info < (3, 6, 0):
    sys.exit("Python 3.6.0 is the minimum required version")

with open(os.path.join(ROOT, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(ROOT, "requirements.txt")) as f:
    requirements = f.readlines()


setuptools.setup(
    name="pycharm_remote_debugger",
    setup_requires=["vcversioner"],
    vcversioner={"vcs_args": ["git", "describe", "--tags", "--long"]},
    description="Easily debug your remote project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliorerz/pycharm-remote-debugger",
    author="Elior Erez",
    author_email="elior123@gmail.com",
    license="MIT",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            "remote_debugger = pycharm_remote_debugger.__main__:main"
        ]
    },
    install_requires=requirements,
    tests_require=requirements,
    include_package_data=True,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Debuggers ",
    ],
)
