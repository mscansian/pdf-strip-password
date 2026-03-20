from setuptools import setup

setup(
    name="pdf-strip-password",
    py_modules=["pdf_remove_pw"],
    install_requires=["pypdf", "argcomplete"],
    entry_points={
        "console_scripts": [
            "pdf-strip-pw = pdf_remove_pw:main",
        ],
    },
)