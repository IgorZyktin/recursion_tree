from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="RecursionTree",
    version="2.0",
    author="Igor Zyktin",
    author_email="nicord@yandex.ru",
    description="Builds recursive calls tree and saves it as an SVG file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IgorZyktin/recursion_tree",
    packages=find_packages(),
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    include_package_data=True, zip_safe=False)
