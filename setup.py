from setuptools import setup, find_packages
import chess_robot
import os


def requirements():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")) as f:
        return [i.strip() for i in f.readlines()]


setup(name='chess_robot',
      version=chess_robot.__version__,
      description='Python package powering my chess playing robot.',
      author=chess_robot.__author__,
      author_email=chess_robot.__email__,
      url='https://github.com/macaquedev/chess-robot',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'chess_robot = chess_robot.__main__:main'
          ]
      },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Programming Language :: Python :: 3.8'
      ],
      install_requires=requirements()
      )
