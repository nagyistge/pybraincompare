from setuptools import setup, find_packages

setup(
    # Application name:
    name="pybraincompare",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=["compare","annotate","template"],

    # Data
    package_data = {'template':['html/*.html']},

    # Details
    url="http://www.github.com/vsoch/pybraincompare",

    license="LICENSE.txt",
    description="image-based meta analysis and comparison for neuroimaging in python",

    install_requires = ['scikit-learn','nibabel','nilearn','pandas','matplotlib','scikit-image','nipy']
)
