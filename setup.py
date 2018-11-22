from setuptools import setup

setup(
    name="aioblinker",
    version='0.1.0',
    packages=['aioblinker'],
    author='Petrunnik Aleksey',
    author_email='petrunnik.a@mail.ru',
    description=(
        'Simple implementation of the mechanism of slots '
        'and signals in pure python.'
    ),
    keywords='signal emit events broadcast',
    url='https://bitbucket.org/alex925/aioblinker/',
    install_requires=[
        'blinker>=1.4'
    ]
)
