import os
from toolchain import *
# from os.path import join
# import sh


class PeeweeRecipe(PythonRecipe):
    version = "2.8.5"
    url = "https://github.com/coleifer/peewee/archive/{version}.tar.gz"
    depends = ["python"]

    def install_python_package(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()

        dest_dir = join(self.ctx.dist_dir, "root", "python")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python2.7', 'site-packages')
        shprint(hostpython, "setup.py", "install", "-O2", "--prefix", dest_dir, _env=build_env)


recipe = PeeweeRecipe()
