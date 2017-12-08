from setuptools import setup, find_pages

setup(
    name='Flask_Youtube',
    version='0.1',
    license='MIT',
    description='Flask extension of allow embedding of YouTube videos',
    author='Jack Stouffer',
    author_email='example@gamil.com',
    platforms='any',
    install_required=['Flask'],
    packages=find_pages()
)
