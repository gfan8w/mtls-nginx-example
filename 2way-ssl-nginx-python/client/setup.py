import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open('requirements.txt') as f:
    required = f.read().splitlines()

tests_require = [
]

setup(
    name='demoapiclient',
    version='0.0',
    description='API Client',
    long_description='Demo',
    classifiers=[
        'Programming Language :: Python',
    ],
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
    },
    install_requires=required,
    entry_points={},
)
