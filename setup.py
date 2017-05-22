import sys
from setuptools import setup, find_packages

version = '0.1.0'

requirements = ['lxml']

if sys.version_info.major >= 3:
    requirements.append('suds-py3')
else:
    requirements.append('suds')

setup(
    name="lather_ui",
    version=version,
    author="Adam Clemons",
    author_email="adam@adamclmns.com",
    description="A simple SOAP client UI.",
    packages=find_packages('.', exclude=['docs', 'tests']),
    entry_points={
        'gui_scripts': [
            'LatherUI=lather_ui.__main__:main'
        ]
    },
    install_requires=requirements,
    license='GPL',
)
