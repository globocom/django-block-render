# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name=u'block_render',
    version="1.0.0",
    description=u"Lib django to render block",
    long_description=u"""""",
    keywords='django block template render',
    author=u'Romulo Jales',
    author_email='romulo.jales@corp.globo.com',
    license='Proprietary',
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers'],
    packages=find_packages(),
    package_dir={"block_render": "block_render"},
    include_package_data=True,
)
