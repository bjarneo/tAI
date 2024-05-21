from setuptools import setup, find_packages


setup(
    name="lfg-llama",
    version="2.2.3",
    description="LFG, It Really Whips the Llama's Ass 🦙🦙🦙🦙",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bjarne Oeverli",
    author_email="bjarneocodes@gmail.com",
    packages=find_packages(),
    install_requires=["openai"],
    entry_points={"console_scripts": ["lfg=lfg.cli:main", "ask=lfg.cli:main"]},
)
