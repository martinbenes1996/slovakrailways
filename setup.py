
from distutils.core import setup
setup(
  name = 'slovakrailways',
  packages = ['.'],
  version = '0.0.2',
  license='MIT',
  description = 'Python envelope of Slovak Railways API',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  url = 'https://github.com/martinbenes1996/slovakrailways',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/martinbenes1996/slovakrailways/archive/v0.0.1.tar.gz',    # I explain this later on
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