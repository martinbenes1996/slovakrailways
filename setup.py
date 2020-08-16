
# requirements
try:
  with open('requirements.txt') as f:
    reqs = f.read().splitlines()
except:
  reqs = []

import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'slovakrailways',
  version = '0.1.0',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Python envelope of Slovak Railways API',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MIT',
  url = 'https://github.com/martinbenes1996/slovakrailways',
  download_url = 'https://github.com/martinbenes1996/slovakrailways/archive/v0.1.0.tar.gz',
  keywords = ['API', 'Railway', 'Train', 'Slovakia', 'Data', 'REST API'],
  install_requires=reqs,
  package_dir={'': '.'},
  package_data={'': ['data/*.json','data/*.csv']},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)