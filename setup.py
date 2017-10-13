from os import path

from setuptools import setup


here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, "README.rst")) as f:
    long_description = f.read()

classifiers = ["License :: OSI Approved :: Apache Software License",
               "Topic :: Software Development :: Testing",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: MacOS :: MacOS X"] + [
                  ("Programming Language :: Python :: %s" % x) for x in
                  "2.7 3.4 3.5".split()]


def main():
    setup(
        name="easyium",
        description="easy use of selenium and appium",
        long_description=long_description,
        install_requires = ['selenium>=3.6.0', 'appium-python-client>=0.24'],
        version="1.2.7",
        keywords="selenium appium test testing framework automation",
        author="Karl Gong",
        author_email="karl.gong@outlook.com",
        url="https://github.com/KarlGong/easyium-python",
        license="Apache",
        classifiers=classifiers,
        packages=["easyium"],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()