import re
import sys

VERSION = None

# get the version without parsing the package
#   because requirements might not be installed
with open("elastipy/_version.py") as fp:
    text = fp.read()
    for match in re.finditer(r"version = \((\d+), (\d+), (\d+)\)", text, re.MULTILINE):
        VERSION = "%s.%s.%s" % tuple(match.groups())


if not VERSION:
    raise ValueError("Can not read version from elastipy/_version.py")


if len(sys.argv) > 1 and sys.argv[1] == "--version":
    print(VERSION)

else:
    from setuptools import setup, find_namespace_packages

    def get_long_description():
        return "%s\n%s" % (
            open("./README.md").read(),
            open("./CHANGELOG.md").read(),
        )

    def get_packages():
        packages = ['elastipy']
        packages += find_namespace_packages(include=['elastipy.*'])
        return packages

    setup(
        name='elastipy',
        version=VERSION,
        description='A python wrapper to make elasticsearch queries and aggregations more fun.',
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url='https://github.com/netzkolchose/elastipy/',
        author='netzkolchose',
        author_email='s.berke+elastipy@netzkolchose.de',
        license='Apache 2.0',
        packages=get_packages(),
        zip_safe=False,
        keywords="elasticsearch aggregation pandas dataframe backend",
        python_requires='>=3.3, <4',
        install_requires=[
            'elasticsearch>=7.10.1',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Database :: Front-Ends',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Typing :: Typed',
        ],
    )
