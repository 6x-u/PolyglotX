from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PolyglotX",
    version="1.0.0",
    author="MERO",
    author_email="contact@mero.dev",
    description="Advanced multilingual exception handler and translator for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6x-u/polyglotx",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: Arabic",
        "Natural Language :: Turkish",
        "Natural Language :: Japanese",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Spanish",
        "Natural Language :: Hindi",
        "Natural Language :: French",
        "Natural Language :: Russian",
        "Natural Language :: German",
        "Natural Language :: Portuguese",
    ],
    python_requires=">=3.6",
    install_requires=[
        "deep-translator>=1.11.0",
        "translatepy>=2.3",
        "requests>=2.25.0",
        "colorama>=0.4.4",
        "pyyaml>=5.4.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "twine>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "polyglotx=PolyglotX.cli.commands:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "translation", "internationalization", "i18n", "localization", "l10n",
        "exception", "error", "handler", "multilingual", "arabic", "turkish",
        "japanese", "chinese", "spanish", "hindi", "french", "russian",
        "german", "portuguese", "kurdish", "error-handling", "debugging"
    ],
    project_urls={
        "Bug Reports": "https://github.com/6x-u/polyglotx/issues",
        "Source": "https://github.com/6x-u/polyglotx",
        "Documentation": "https://github.com/6x-u/polyglotx/wiki",
        "Telegram": "https://t.me/QP4RM",
    },
)
