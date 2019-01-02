import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recursion_tree",
    version="1.0.0",
    author="Igor Zyktin",
    author_email="nicord@yandex.ru",
    description="Builds recursive calls tree and saves it as a PNG file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IgorZyktin/recursion_tree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)
