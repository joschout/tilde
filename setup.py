from setuptools import setup

setup(name='tilde',
      version='0.1',
      packages='tilde',
      entry_points={
          'console_scripts': [
              'tilde=tilde.main:main'

          ]

      }, install_requires=['problog', 'scikit-learn'])

