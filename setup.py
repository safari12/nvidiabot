from setuptools import setup

with open('requirements.txt') as requirements:
    install_requires = requirements.read()

setup(
    name='nvidiabot',
    version='1.0.0',
    packages=['nvidiabot'],
    install_requires=install_requires,
    keywords='nvidiabot bot',
    entry_points={
        'console_scripts': [
            'nvidiabot = nvidiabot.__main__:app'
        ]
    }
)
