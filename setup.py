import sys


VERSION = "0.0.1"


if len(sys.argv) > 1 and sys.argv[1] == "--version":

    print(VERSION)

else:
    from setuptools import setup, find_namespace_packages

    def get_long_description():
        return "%s\n" % (
            open("./README.md").read(),
            # open("./HISTORY.md").read(),
        )

    def get_packages():
        packages = ['elastipy']
        packages += find_namespace_packages(include=['elastipy.*'])
        return packages

    setup(
        name='elastipy',
        version=VERSION,
        description='Elasticsearch search-API wrapper',
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url='https://netzkolchose.de',
        author='Netzkolchose',
        author_email='s.berke+elastipy@netzkolchose.de',
        license='MIT',
        packages=get_packages(),
        zip_safe=False,
        keywords="elasticsearch aggregation",
        python_requires='>=3.3, <4',
        install_requires=[
            'elasticsearch>=7.10.1',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
