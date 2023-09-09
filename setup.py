import setuptools
from distutils.core import Extension
from distutils.command.build_py import build_py
import urllib.request
import shutil
import subprocess
import os
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()


class custom_build_py(build_py):
    def run(self):
        urllib.request.urlretrieve("https://sourceforge.net/projects/perfmon2/files/libpfm4/libpfm-4.12.0.tar.gz", "libpfm.tar.gz")
        
        shutil.unpack_archive("libpfm.tar.gz", extract_dir=self.build_lib)
        extract_dir = os.path.join(self.build_lib, "libpfm-4.12.0")
        subprocess.run(["make"], cwd=extract_dir, check=True)

        python_dir = os.path.join(extract_dir, "python")

        # Fix init file
        self.copy_file("perfmon/__init__.py", os.path.join(python_dir, "src"))

        # Generate python files
        subprocess.run([sys.executable, "setup.py", "build"], cwd=python_dir, check=True)

        # Install python files
        subprocess.run([sys.executable, "setup.py", "build", "-f"], cwd=python_dir, check=True)
        subprocess.run([sys.executable, "setup.py", "install"], cwd=python_dir, check=True)
        super().run()
        # os.remove("libpfm.tar.gz")


setuptools.setup(
    cmdclass={"build_py": custom_build_py},
    name="performance_features",
    version="0.2.6",
    packages=["performance_features"],
    package_dir={"performance_features": "performance_features"},
    py_modules=["performance_features.profiler"],
    install_requires=["pandas", "scipy"],
    author="Alok Kamatar",
    author_email="alokvk2@uchicago.edu",
    description="perf event wrapper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VitorRamos/performance_features",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
