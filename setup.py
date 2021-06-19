import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = f.read().split("\n")

setuptools.setup(
    name="phoenyx",
    version="0.3.3",
    author="Thomas Byr",
    author_email="thomas-c2000@outlook.fr",
    description="A drawing and physics engine for Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThomasByr/phoenyx.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requires,
)
