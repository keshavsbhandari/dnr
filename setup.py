# @copyright: AlertAvert.com (c) 2016. All rights reserved.

from setuptools import setup

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'md')

except ImportError:
    long_description = """
    RNN based word2vec implementation for news recommendation

    Use Recommendation module to make your own content based news recommendation
    using the fact that reader can news next news provided that they had read certain news

    More information at: https://github.com/keshavsbhandari/dnr
"""

setup(name='dnr',
      description='RNN based word2vec implementation for news recommendation',
      long_description=long_description,
      version='0.1',
      url='https://github.com/keshavsbhandari/dnr',
      author='Keshav Bhandari',
      author_email='keshav.s.bhandari@gmail.com',
      license='copyright',
      classifiers=[
          'Development Status :: 1 - Beta',
          'Intended Audience :: AI Developer/Data Scientist/Software Developer',
          'License :: OSI Approved :: None',
          'Programming Language :: Python :: 3'
      ],
      packages=['dnr'],
      install_requires=[
            'gensim==3.4.0',
            'numpy==1.14.2',
            'scipy==1.0.1'
      ],
      entry_points={}
      )
