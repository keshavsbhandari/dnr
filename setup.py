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
      version='0.8',
      url='https://github.com/keshavsbhandari/dnr',
      download_url = 'https://github.com/keshavsbhandari/dnr/archive/master.zip',
      author='Keshav Bhandari',
      author_email='keshav.s.bhandari@gmail.com',
      license='copyright',
      keywords = ['recommendation', 'recommendersystem', 'rnn','lstm','word2vec','gensim'], # arbitrary keywords
      classifiers=[],
      packages=['dnr'],
      install_requires=[
            'gensim<=3.4.0',
            'numpy<=1.14.2',
            'scipy<=1.0.1'
      ],
      entry_points={}
      )
