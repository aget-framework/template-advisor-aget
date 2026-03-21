"""
AGET (CLI Agent Template) - Setup configuration
"""
from setuptools import setup, find_packages
import os

# Read the README for long description
def read_long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='aget-cli-agent-template',
    version='1.0.0',
    author='Gabor Melli',
    author_email='',
    description='AGET: The universal standard for making any codebase instantly CLI agent-ready',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/aget-framework/aget-cli-agent-template',
    project_urls={
        'Bug Reports': 'https://github.com/aget-framework/aget-cli-agent-template/issues',
        'Source': 'https://github.com/aget-framework/aget-cli-agent-template',
    },
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'examples.*']),
    python_requires='>=3.8',
    install_requires=[
        'click>=8.0.0',
        'rich>=13.0.0',
        'gitpython>=3.1.0',
        'pyyaml>=6.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'ruff>=0.1.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'aget=installer.install:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='cli agent ai coding assistant development automation',
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.yml', '*.yaml'],
        'patterns': ['**/*.py'],
        'scripts': ['*.py'],
        'templates': ['**/*'],
    },
)