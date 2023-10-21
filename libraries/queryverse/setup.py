from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="queryverse",
    version="0.1.1",
    description="A lightweight prompting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="temiloluwa adeoti",
    author_email="temilolu74@gmail.com",
    url="https://github.com/temiloluwa/lingua_trainer/queryverse",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="lightweight llm prompting library",
    install_requires=[
        "openai", "python-dotenv"
    ],
    python_requires=">=3.9",
)
