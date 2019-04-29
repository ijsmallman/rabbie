from distutils.core import setup

setup(
    name='rabbie',
    version='0.0.1',
    author='Joe Smallman',
    author_email='ijsmallman@gmail.com',
    description='Package to add smart home monitoring to holiday cottage in Scotland',
    packages=[
      'rabbie'
    ],
    entry_points={
        'console_scripts': [
        ],
    }
)
