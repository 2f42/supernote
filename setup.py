from setuptools import setup


setup(
    name="supernote",
    version='0.1',
    py_modules=['supernote'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        supernote=supernote:cli
    ''',
)
