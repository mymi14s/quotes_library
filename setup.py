from setuptools import setup, find_packages

setup(
    name='quotes_library',
    version='0.1',
    packages=find_packages(),
    install_requires=[

    ],
    author='Anthony Emmanuel',
    author_email='hackacehuawei@gmail.com',
    description='This python library generates quotes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mymi14s/quotes_library',
    python_requires = '>=3.7',
    include_package_data=True
)