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
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "responses>=0.13.0",
            "flake8>=3.8.0",
            "mypy>=0.800"
        ],
    },
    python_requires='>=3.6',
)
