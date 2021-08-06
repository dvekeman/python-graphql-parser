import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphql-parser",
    version="0.0.1",
    author="Dieter Vekeman",
    author_email="dieter.vekeman@gmail.com",
    description="Parse a graphql string into an AST",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/dvekeman/python-graphql-parser",
    project_urls={
        "Bug Tracker": "https://github.com/dvekeman/python-graphql-parser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "graphql_parser"},
    packages=setuptools.find_packages(where="graphql_parser"),
    python_requires=">=3.7",
)