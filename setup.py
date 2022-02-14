from setuptools import setup

setup(
    name="niche-scraper",
    version="0.2.0",
    description="A web scraper for niche.com.",
    py_modules=[
        "nscraper",
        "main"
    ],
    install_requires=[
        "requests",
        "time",
        "csv",
        "json",
        "bs4"
    ],
)
