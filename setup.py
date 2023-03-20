import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="controller-randomizer",
    version="0.1.0",
    author="Tanikai",
    author_email="kai@anter.dev",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tanikai/controller-randomizer",
    project_urls={
        "Bug Tracker": "https://github.com/Tanikai/controller-randomizer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["controller_randomizer"],
    python_requires=">=3.0",
    install_requires=[
        "XInput-Python",
        "vgamepad",
        "strenum",
    ]
)
