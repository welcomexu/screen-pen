from setuptools import setup, find_packages

setup(
    name="screen-pen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.5.0",
        "Pillow>=9.5.0",
        "pyobjc-framework-Quartz>=9.0.1",
    ],
    entry_points={
        'console_scripts': [
            'screen-pen=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A screen annotation tool for macOS",
)
