
import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'slovakrailways',
  version = '0.0.5',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Python envelope of Slovak Railways API',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MIT',
  url = 'https://github.com/martinbenes1996/slovakrailways',
  download_url = 'https://github.com/martinbenes1996/slovakrailways/archive/v0.0.5.tar.gz',
  keywords = ['API', 'Railway', 'Train', 'Slovakia', 'Data', 'REST API'],
  install_requires=[],
  package_dir={'': '.'},
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