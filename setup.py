import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="analner",
    version="0.0.6",
    author="Andrew Sorokin",
    author_email="i40mines@yandex.ru",
    description="Compiler of funny news based on onliner news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/40min/analner.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3',
    install_requires=[
        'beautifulsoup4==4.6.0',
        'bs4==0.0.1',
        'certifi==2018.4.16',
        'html5lib==1.0.1',
        'lxml==4.2.1',
        'markovify==0.7.1',
        'urllib3==1.22',
        'webencodings==0.5.1',
        'spacy==2.0.12'
    ],
    dependency_links=[
        'https://github.com/explosion/spacy-models/releases/download/xx_ent_wiki_sm-2.0.0/xx_ent_wiki_sm-2.0.0.tar.gz'
    ]
)