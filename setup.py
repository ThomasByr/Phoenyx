import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requires = f.read().split("\n")

setuptools.setup(
    name="phoenyx",
    version="0.1.1",
    author="Thomas B",
    author_email="tbouyer2000@gmail.com",
    description="An engine for pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Thomas2-bot/phoenyx.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requires,
)
