from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="RecursionTree",
    version="1.5",
    author="Igor Zyktin",
    author_email="nicord@yandex.ru",
    description="Builds recursive calls tree and saves it as a PNG file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IgorZyktin/recursion_tree",
    packages=find_packages(),
    package_data={'': ['RecursionTree/Excalibur-Monospace.ttf']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pillow>=3.4.0',
    ],
    include_package_data=True, zip_safe=False)
