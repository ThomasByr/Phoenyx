import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

packages = ["phoenyx"]
meta_data: dict[str, str] = {}

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = f.read().split("\n")

with open(os.path.join(here, "phoenyx", "__version__.py"),
          "r",
          encoding="utf-8") as f:
    exec(f.read(), meta_data)

setuptools.setup(
    name=meta_data["__title__"],
    version=meta_data["__version__"],
    author=meta_data["__author__"],
    author_email=meta_data["__author_email__"],
    description=meta_data["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=meta_data["__url__"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requires,
)
