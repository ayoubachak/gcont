from setuptools import setup, find_packages

setup(
    name="gcont",  # Name of the package
    version="0.1.4",  # Initial release version
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,  # Include files from MANIFEST.in
    install_requires=[
        "pyyaml",  # Include any dependencies your package needs
    ],
    entry_points={
        "console_scripts": [
            "gcont=gcont.main:main",  # This creates the command line tool 'gcont'
        ],
    },
    author="Ayoub Achak",
    author_email="ayoub.achak01@gmail.com",
    description="A tool for gathering and documenting project files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ayoubachak/gcont",  # Your project homepage
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
