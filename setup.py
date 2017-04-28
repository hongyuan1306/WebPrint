from setuptools import setup, find_packages

setup(
    name='webprint',
    version='0.1',
    description='Printer Server for Web Applications',
    author='Hong Yuan',
    author_email='hongyuan@homemaster.cn',
    packages=find_packages(),
    install_requires=[
        'wxPython>=4.0',
        'sqlalchemy',
        'autobahn',
        'hm.wxx'
    ]
)
