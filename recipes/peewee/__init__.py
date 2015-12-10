import os
from toolchain import *
# from os.path import join
# import sh


class PeeweeRecipe(PythonRecipe):

    version = "2.7.3"

    name="peewee"

    depends = ["hostpython", "host_setuptools", "python", "ios"]

    url = "https://github.com/coleifer/peewee/archive/{version}.tar.gz"

    def install_python_package(self, name=None, env=None, is_dir=True):
        """Automate the installation of a Python package into the target
        site-packages.

        It will works with the first filtered_archs, and the name of the recipe.
        """
        arch = self.filtered_archs[0]
        if name is None:
            name = self.name
        if env is None:
            env = self.get_recipe_env(arch)
        print("Install {} into the site-packages".format(name))
        build_dir = self.get_build_dir(arch.arch)
        chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        iosbuild = join(build_dir, "iosbuild")
        shprint(hostpython, "setup.py", "install", "-O2",
                "--prefix", iosbuild,
                _env=env)

        self.remove_junk(iosbuild)

        dest_file = join(self.ctx.site_packages_dir, "peewee.pyo")
        dest_dir = join(self.ctx.site_packages_dir, "playhouse")

        if exists(dest_file):
            os.remove(dest_file)

        if exists(dest_dir):
            shutil.rmtree(dest_dir)

        shutil.copy(
            join(iosbuild, "lib",
                 self.ctx.python_ver_dir, "site-packages", "peewee.pyo"),
            dest_file)

        shutil.copytree(
            join(iosbuild, "lib",
                 self.ctx.python_ver_dir, "site-packages", "playhouse"),
            dest_dir)


recipe = PeeweeRecipe()
