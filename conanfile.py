import os
import shutil

from conans import ConanFile, tools, AutoToolsBuildEnvironment, RunEnvironment


class AreaDetector(ConanFile):
    name = "ADKafkaPlugin"
    version = "0.0"
    license = ""
    url = "git@github.com:ess-dmsc/ad-kafka-interface.git"
    description = 'An EPICS areaDetector plugin which sends areaDetector ' \
                  'data serialised using flatbuffers to a Kafka broker.'
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "gcc"
    requires = 'epics/3.16.1-4.6.0-dm6@ess-dmsc/stable', \
               'synapps/6.0@devel/epics'
    submodules = ["PluginKafka"]

    def get_epics_info(self):
        epics_base = self.deps_cpp_info["epics"].rootpath.replace('/package/',
                                                                  '/build/')

        epics_version = [folder for folder in os.listdir(path=epics_base) if
                         folder.startswith('base-')]
        if epics_version:
            epics_base += '/' + epics_version[0]
            epics_version = epics_version[0].split('-')[1]
            return epics_base, epics_version
        return '', ''

    def get_module_info(self, modulename):
        result = None
        try:
            result = self.deps_cpp_info[modulename]
        except Exception as e:
            print(e)
        return result

    # def _replace_release(self, install_location):
    #     source = os.path.join("configure", "RELEASE")
    #     tools.replace_in_file(source, "#INSTALL_LOCATION_APP=<fullpathname>",
    #                           "#INSTALL_LOCATION_APP=" + install_location)
    #
    # def _replace_release_support_local(self, support):
    #     source = os.path.join("configure", "RELEASE_SUPPORT.local")
    #     orig = "SUPPORT=/corvette/home/epics/devel"
    #     edit = "SUPPORT=" + support
    #     tools.replace_in_file(source, orig, edit)
    #
    # def _replace_release_libs_local(self, support, install_location):
    #     source = os.path.join("configure", "RELEASE_LIBS.local")
    #
    #     orig = "ASYN=$(SUPPORT)/asyn-4-35"
    #     edit = [x for x in os.listdir(support) if "asyn" in x][0]
    #     tools.replace_in_file(source, orig, "ASYN=$(SUPPORT)/" + edit)
    #
    #     orig = "AREA_DETECTOR=$(SUPPORT)/areaDetector-3-5"
    #     edit = [x for x in os.listdir(support) if "areaDetector" in x][0]
    #     tools.replace_in_file(source, orig, "AREA_DETECTOR=$(SUPPORT)/" + edit)
    #
    #     orig = "EPICS_BASE=/corvette/usr/local/epics-devel/base-7.0.2"
    #     edit = "EPICS_BASE=" + self.get_epics_info()[0]
    #     tools.replace_in_file(source, orig, edit)
    #
    #     orig = "#PVA=/corvette/usr/local/epics-devel/epicsV4/EPICS-CPP-4.6.0"
    #     edit = "PVA=" + self.get_pva()
    #     tools.replace_in_file(source, orig, edit)
    #
    #     tools.replace_in_file(source, "#PVCOMMON=$(PVA)/pvCommonCPP",
    #                           "PVCOMMON=$(PVA)/pvCommonCPP")
    #     tools.replace_in_file(source, "#PVACCESS=$(PVA)/pvAccessCPP",
    #                           "PVACCESS=$(PVA)/pvAccessCPP")
    #     tools.replace_in_file(source, "#PVDATA=$(PVA)/pvDataCPP",
    #                           "PVDATA=$(PVA)/pvDataCPP")
    #     tools.replace_in_file(source, "#PVDATABASE=$(PVA)/pvDatabaseCPP",
    #                           "PVDATABASE=$(PVA)/pvDatabaseCPP")
    #     tools.replace_in_file(source,
    #                           "#NORMATIVETYPES=$(PVA)/normativeTypesCPP",
    #                           "NORMATIVETYPES=$(PVA)/normativeTypesCPP")
    #
    #     tools.replace_in_file(source, "#INSTALL_LOCATION_APP=<fullpathname>",
    #                           "#INSTALL_LOCATION_APP=" + install_location)
    #
    # def _replace_release_prods_local(self, support, install_location):
    #     source = os.path.join("configure", "RELEASE_PRODS.local")
    #
    #     orig = "ASYN=$(SUPPORT)/asyn-4-35"
    #     edit = [x for x in os.listdir(support) if "asyn" in x][0]
    #     tools.replace_in_file(source, orig, "ASYN=$(SUPPORT)/" + edit)
    #
    #     orig = "AREA_DETECTOR=$(SUPPORT)/areaDetector-3-5"
    #     edit = [x for x in os.listdir(support) if "areaDetector" in x][0]
    #     tools.replace_in_file(source, orig, "AREA_DETECTOR=$(SUPPORT)/" + edit)
    #
    #     orig = "AUTOSAVE=$(SUPPORT)/autosave-5-9"
    #     edit = [x for x in os.listdir(support) if "autosave" in x][0]
    #     tools.replace_in_file(source, orig, "AUTOSAVE=$(SUPPORT)/" + edit)
    #
    #     orig = "BUSY=$(SUPPORT)/busy-1-7"
    #     edit = [x for x in os.listdir(support) if "busy" in x][0]
    #     tools.replace_in_file(source, orig, "BUSY=$(SUPPORT)/" + edit)
    #
    #     orig = "CALC=$(SUPPORT)/calc-3-7"
    #     edit = [x for x in os.listdir(support) if "calc" in x][0]
    #     tools.replace_in_file(source, orig, "CALC=$(SUPPORT)/" + edit)
    #
    #     tools.replace_in_file(source,
    #                           "SNCSEQ=$(SUPPORT)/seq-2-2-5",
    #                           "#SNCSEQ=$(SUPPORT)/seq-2-2-5")
    #
    #     orig = "SSCAN=$(SUPPORT)/sscan-2-11-1"
    #     edit = [x for x in os.listdir(support) if "sscan" in x][0]
    #     tools.replace_in_file(source, orig, "SSCAN=$(SUPPORT)/" + edit)
    #
    #     tools.replace_in_file(source,
    #                           "DEVIOCSTATS=$(SUPPORT)/devIocStats-3-1-15",
    #                           "#DEVIOCSTATS=$(SUPPORT)/devIocStats-3-1-15")
    #     # orig = "DEVIOCSTATS=$(SUPPORT)/devIocStats-3-1-15"
    #     # edit = [x for x in os.listdir(support) if "devIocStats" in x][0]
    #     # tools.replace_in_file(source, orig, "DEVIOCSTATS=$(SUPPORT)/"+edit)
    #
    #     orig = "EPICS_BASE=/corvette/usr/local/epics-devel/base-7.0.2"
    #     edit = "EPICS_BASE=" + self.get_epics_info()[0]
    #     tools.replace_in_file(source, orig, edit)
    #
    #     orig = "#PVA=/corvette/usr/local/epics-devel/epicsV4/EPICS-CPP-4.6.0"
    #     edit = "PVA=" + self.get_pva()
    #     tools.replace_in_file(source, orig, edit)
    #
    #     tools.replace_in_file(source, "#PVCOMMON=$(PVA)/pvCommonCPP",
    #                           "PVCOMMON=$(PVA)/pvCommonCPP")
    #     tools.replace_in_file(source, "#PVACCESS=$(PVA)/pvAccessCPP",
    #                           "PVACCESS=$(PVA)/pvAccessCPP")
    #     tools.replace_in_file(source, "#PVDATA=$(PVA)/pvDataCPP",
    #                           "PVDATA=$(PVA)/pvDataCPP")
    #     tools.replace_in_file(source, "#PVDATABASE=$(PVA)/pvDatabaseCPP",
    #                           "PVDATABASE=$(PVA)/pvDatabaseCPP")
    #     tools.replace_in_file(source,
    #                           "#NORMATIVETYPES=$(PVA)/normativeTypesCPP",
    #                           "NORMATIVETYPES=$(PVA)/normativeTypesCPP")
    #
    #     tools.replace_in_file(source, "#INSTALL_LOCATION_APP=<fullpathname>",
    #                           "INSTALL_LOCATION_APP=" + install_location)
    #
    # def _replace_config_site(self, install_location):
    #     source = os.path.join("configure", "CONFIG_SITE")
    #     tools.replace_in_file(source,
    #                           "#INSTALL_LOCATION=</path/name/to/install/top>",
    #                           "INSTALL_LOCATION=" + install_location)
    #
    # def _replace_config_site_local(self):
    #     source = os.path.join("configure", "CONFIG_SITE.local")
    #     tools.replace_in_file(source, "WITH_GRAPHICSMAGICK     = YES",
    #                           "WITH_GRAPHICSMAGICK     = NO")
    #
    # def _edit_config(self):
    #     for f in ['RELEASE', 'RELEASE_SUPPORT', 'RELEASE_LIBS',
    #               'RELEASE_PRODS', 'CONFIG_SITE']:
    #         shutil.copyfile(
    #             os.path.join("configure", 'EXAMPLE_' + f + '.local'),
    #             os.path.join("configure", f + '.local')
    #         )
    #
    #     support = os.path.join(self.deps_cpp_info[
    #         "synapps"].build_paths[0].replace(
    #         '/package/', '/build/'),
    #         'synApps', 'support')
    #     install_location = os.getcwd()
    #
    #     # edit RELEASE
    #     self._replace_release(install_location)
    #
    #     # edit RELEASE_SUPPORT.local
    #     self._replace_release_support_local(support)
    #
    #     # edit RELEASE_LIBS.local
    #     self._replace_release_libs_local(support, install_location)
    #
    #     # edit RELEASE_PRODS.local
    #     self._replace_release_prods_local(support, install_location)
    #
    #     self._replace_config_site(install_location)
    #
    #     self._replace_config_site_local()
    #
    #     source = os.path.join("configure", "CONFIG")
    #     tools.replace_in_file(source, "INSTALL_LOCATION = $(TOP)",
    #                           "INSTALL_LOCATION = " + install_location)

    def source(self):
        git = tools.Git()
        git.clone(self.url)
        # for submodule in self.submodules:
        #     git.run("submodule update --init " + submodule)

    def build(self):
        pass

        # self._edit_config()
        #
        # with tools.environment_append({'EPICS_HOST_ARCH': 'linux-x86_64'}):
        #     autotools = AutoToolsBuildEnvironment(self)
        #     env_build = RunEnvironment(self)
        #
        #     autotools.make(vars=env_build.vars)

            #    def package(self):
            #
            #        if tools.os_info.is_linux:
            #            arch = "linux-x86_64"
            #        elif tools.os_info.is_macos:
            #            arch = "darwin-x86"
            #
            #        for module in self._list_wanted_modules():
            #            path = os.path.join('synApps/support', module, 'lib', arch)
            #            if os.path.isdir(path):
            #                self.copy("*.a", dst="lib", src=path, keep_path=False)
            #                self.copy("*.so", dst="lib", src=path, keep_path=False)
            #                self.copy("*.dylib", dst="lib", src=path, keep_path=False)
            #            path = os.path.join('synApps/support', module, 'include')
            #            if os.path.isdir(path):
            #                self.copy("*.h", dst="include", src=path, keep_path=False)
            #
            #    def package_info(self):
            #        self.cpp_info.libs = self.collect_libs()
            #
