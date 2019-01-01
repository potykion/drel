import setuptools

with open("README.md") as f:
    long_description = f.read()

install_requires = [
    "django>=1.11",
    "requests>=2.18.0",
    "elasticsearch>=6.0.0,<7.0.0",
    "marshmallow>=2.16.0,<3.0.0",
    "attrs>=18.1.0"
]

setuptools.setup(
    name="drel",
    version="0.4.1",
    author="Leybovich Nikita",
    author_email="potykion@gmail.com",
    description="Django request ElasticSearch logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/potykion/drel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)
