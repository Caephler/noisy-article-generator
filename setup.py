from setuptools import setup, find_packages

setup(
  name="noisy-article-generator",
  version="1.0",
  description="Noisy Article Generator",
  author="Gabriel Tan",
  author_email="caephler@gmail.com",
  url="https://github.com/Caephler/noisy-article-generator",
  packages=find_packages(),
  install_requires=[
    'numpy',
    'progressbar2',
    'Pillow',
    'lorem',
    'pathlib'
  ],
  entry_points={
    'console_scripts': [
      'noisy-article-generate = generator.__main__:main'
    ]
  }
)