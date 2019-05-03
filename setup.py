from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='rsttace',
      version='0.1',
      description='RST-Tace',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Rethorical Structure Theory :: Evaluation',
      ],
      keywords='rethorical structure theory',
      url='https://github.com/tkutschbach/Rst-Tace',
      author='Tino Kutschbach',
      license='MIT',
      packages=[
          'rsttace',
          'rsttace.core',
          'rsttace.controller',
          'rsttace.input',
          'rsttace.output'
      ],
      package_dir={'': '.'},
      install_requires=[
          'anytree', 'scipy'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['rsttace=rsttace.commandline:cli'],
      },
      include_package_data=True,
      zip_safe=False)
