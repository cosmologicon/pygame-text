import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pygame-text",
    version="1.0.0",
    description="Convenience functions for drawing using the pygame.font module.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cosmologicon/pygame-text",
    author="cosmologicon",
    author_email="cosmologicon@gmail.com",
    license="CC0 1.0 Universal",
    classifiers=[
    ],
    python_requires=">=2.7",
    packages=["ptext"],
    include_package_data=True,
    install_requires=["pygame"],
)
