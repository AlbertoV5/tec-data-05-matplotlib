import setuptools

setuptools.setup(
    name="pyberlib",
    version="0.1.0",
    author="Alberto Valdez",
    author_email="avq5ac1@gmail.com",
    description="Plotting utilities.",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"pyberlib": ["py.typed"]},
    python_requires=">=3.7",
    install_requires=[
        "matplotlib==3.5.2",
        "numpy==1.21.6",
        "pandas==1.3.5",
        "scipy==1.7.3",
    ]
)