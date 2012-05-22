from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='collective.socialpublisher',
      version=version,
      description="Manage and automate social publishing on Plone sites",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Simone Orsi [simahawk]',
      author_email='simahawk@gmail.com',
      url='https://github.com/simahawk/collective.socialpublisher',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.twitter.accounts',
          'tweepy',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
