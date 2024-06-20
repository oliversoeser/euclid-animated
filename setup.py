from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Manim plugin for animating Euclid's elements."
LONG_DESCRIPTION  = "A Manim plugin for animating Euclid's elements."

if __name__ == "__main__":
    setup(
        name="manim_euclid",
        version=VERSION,
        author="Oliver Soeser",
        author_email="hello@oliversoeser.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=["manim", "geometry", "euclid", "animation"],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
    )