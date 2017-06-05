from distutils.core import setup

setup(
    name='rabbie',
    version='0.0.1',
    author='Joe Smallman',
    author_email='ijsmallman@gmail.com',
    description='Package to add smart home logging and notification funcionlity to holiday cottage in Scotland',
    packages=[
      'rabbie.level_logger',
      'rabbie.database'
    ],
    entry_points = {
        'console_scripts': ['log-level=rabbie.level_logger.main:main'],
    }
)
