from setuptools import setup, find_packages

setup(
    name="text_to_speech",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "wave",
        "simpleaudio",
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)