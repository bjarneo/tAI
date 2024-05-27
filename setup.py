from setuptools import setup, find_packages


setup(
    name="terminal-ai-assistant",
    version="3.0.1",
    description="TAI [Terminal AI], a terminal AI assistant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bjarne Oeverli",
    author_email="bjarneocodes@gmail.com",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points={"console_scripts": ["tai=tai.cli:main"]},
)
