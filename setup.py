from setuptools import setup

setup(
    name="nbt2json",
    author="martmists",
    author_email="mail@martmists.com",
    license="MIT",
    zip_safe=False,
    version="1.1",
    description="Easy interface for minecraft NBT files",
    url="https://github.com/martmists/NBT2JSON",
    packages=["."],
    install_requires=["nbt"],
    entry_points={
        "console_scripts": ["nbt2json = nbt2json:main"]
    },
    keywords=["nbt", "python", "json", "tree"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console", "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.5"
)
