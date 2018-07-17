from setuptools import setup

setup(
    name="aioblinker",
    version='0.0.1',
    packages=['aioblinker'],
    author='Petrunnik Aleksey',
    author_email='petrunnik.a@mail.ru',
    description='Fast, simple object-to-object and broadcast signaling',
    keywords='signal emit events broadcast',
    url='https://bitbucket.org/alex925/aioblinker/',
    install_requires=[
        'blinker>=1.4'
    ]
)
