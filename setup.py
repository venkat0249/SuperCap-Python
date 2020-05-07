from distutils.core import setup
setup(
  name = 'supercap',
  packages = ['supercap'],
  version = '0.3',
  license='MIT',
  description = 'Supercapacitor Modelling package for Python',   
  author = 'Daniel Lavin and Venkatesh Pampana',
  author_email = 'venkatmr.perfect@gmail.com',
  url = 'https://github.com/venkat0249/SuperCap-Python',
  download_url = 'https://github.com/venkat0249/SuperCap-Python/archive/v_03.tar.gz',
  keywords = ['supercapacitor', 'energy', 'simulation','modelling','model'],
  install_requires=[ 
          'pandas',
          'numpy',
		  'prompt_toolkit',
      ],
  classifiers=[
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)