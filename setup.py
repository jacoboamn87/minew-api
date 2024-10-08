from setuptools import setup, find_packages

setup(
    name="minew_rest",
    version="1.0.0",
    description="Minew ESL Cloud API Client",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires='>=3.6',
)
