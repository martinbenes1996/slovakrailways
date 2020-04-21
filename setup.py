from distutils.core import setup
setup(
  name = 'slovakrailways',
  packages = ['slovakrailways'],
  version = '0.0.1',
  license='MIT',
  description = 'Python envelope of Slovak Railways API',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  url = 'https://github.com/martinbenes1996/slovakrailways',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/martinbenes1996/slovakrailways/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['API', 'Railway', 'Train', 'Slovakia', 'Data', 'REST API'],
  install_requires=[],
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