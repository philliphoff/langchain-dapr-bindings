from setuptools import setup

setup(
    name='daprai',
    version='0.0.1',
    install_requires=[
        'dapr',
        'langchain',
        'importlib-metadata; python_version == "3.10"',
    ],
)
