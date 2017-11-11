from setuptools import setup
setup(
    name = 'pyMRA',
    packages = ['pyMRA'], # this must be the same as the name above
    version = '0.1',
    description = 'Multi-resolution approximation for spatial Gaussian processes',
    author = 'Marcin Jurek',
    author_email = 'marcinjurek1988@gmail.com',
    url = 'https://github.com/marcinjurek/pyMRA', # use the URL to the github repo
    download_url = 'https://github.com/marcinjurek/pyMRA/archive/0.1.tar.gz',
    #download_url = 'https://github.com/peterldowns/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
    keywords = ['Gaussian process', 'multi-resolution', 'sparse', 'approximation', 'spatial', 'statistics'], # arbitrary keywords
    classifiers = [],
)
