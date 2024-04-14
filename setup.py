from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name='pyconn-monitor',
    version='0.1.3',
    author='ParisNeo',
    author_email='parisneoai@gmail.com',
    description='A Python library to monitor and log network connections of untrusted programs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ParisNeo/pyconn-monitor',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pyconn-monitor=pyconn_monitor.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
