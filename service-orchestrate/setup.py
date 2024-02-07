"""Set up Orchestrate service and add entrypoints.
"""

from setuptools import find_packages, setup


setup(
    name="service-orchestrate",
    version="1.0.0",
    description="Sends commands to various service endpoints in AI system",
    author="Jorge Galdos",
    author_email="jorgegaldosjr@gmail.com",
    url="",
    platforms=["any"],
    license="",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "psutil==5.9.2",
        "pydantic==2.5.3",
        "faust==1.10.4",
    ],
    python_requires="~=3.9",
    entry_points={
        "console_scripts": ["prod = orchestrate.produce:main"],
    },
)
