from setuptools import setup, find_packages


def get_install_requires():
    install_requires = []

    with open("requirements.txt", "r") as req_txt:
        install_requires = map(lambda s: s.strip(), req_txt.readlines()[2:])

    return list(install_requires)


setup(
    name="lfg-llama",
    version="1.0.3",
    description="LFG, It Really Whips the Llama's Ass 🦙🦙🦙🦙",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bjarne Oeverli",
    author_email="bjarneocodes@gmail.com",
    packages=find_packages(),
    install_requires=["ollama"],
    entry_points={"console_scripts": ["lfg=lfg.cli:main"]},
)
