#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / 'README.md'
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ''

setup(
    name='naviko-lab',
    version='1.4.0',
    description='自分で考えて成長するAI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Naviko LAB Team',
    author_email='7716no70@gmail.com',
    url='https://github.com/7716no70-sudo/naviko-lab',
    license='MIT',
    
    packages=find_packages(),
    
    install_requires=[
        'groq>=0.4.0',
        'requests>=2.31.0',
    ],
    
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
    },
    
    python_requires='>=3.8',
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    
    keywords='ai autonomous code-generation llm naviko',
    
    project_urls={
        'Bug Reports': 'https://github.com/7716no70-sudo/naviko-lab/issues',
        'Source': 'https://github.com/7716no70-sudo/naviko-lab',
    },
)
