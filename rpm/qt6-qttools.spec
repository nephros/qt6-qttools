%global  qt_version 6.8.3

#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif

#global examples 1
# disable once Qt7 is stable and providing the apps
#global metainfo 1

Summary: Qt6 - QtTool components
Name:    qt6-qttools
Version: 6.8.3
Release: 3%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

# help lrelease/lupdate use/prefer qmake-qt6
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch1: qttools-run-qttools-with-qt6-suffix.patch

# 32-bit MIPS needs explicit -latomic
Patch2: qttools-add-libatomic.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

# borrowed from Flathub with adjustments for Fedora
Source31: io.qt.Designer.metainfo.xml
Source32: io.qt.Linguist.metainfo.xml
Source33: io.qt.qdbusviewer.metainfo.xml

BuildRequires: cmake
BuildRequires: ninja
BuildRequires: clang
BuildRequires: desktop-file-utils
#BuildRequires: libappstream-glib
BuildRequires: qt6-rpm-macros >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static >= %{qt_version}
BuildRequires: qt6-qtdeclarative-static >= %{qt_version}
BuildRequires: qt6-qtdeclarative >= %{qt_version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
#BuildRequires: clang-devel llvm-devel clang-tools-extra-devel
BuildRequires: libzstd-devel

Requires: %{name}-common = %{version}-%{release}

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch

%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
#Requires: %%{name}-libs-help%%{?_isa} = %%{version}-%%{release}
Requires: qt6-doctools = %{version}-%{release}
Requires: qt6-designer = %{version}-%{release}
Requires: qt6-linguist = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-designer
Summary: Qt6 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt6 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designercomponents
%{summary}.

#%%package libs-help
#Summary: Qt6 Help runtime library
#Requires: %%{name}-common = %%{version}-%%{release}
#%%description libs-help
#%%{summary}.

#%%package -n qt6-assistant
#Summary: Documentation browser for Qt6
#Requires: %%{name}-common = %%{version}-%%{release}
#%%description -n qt6-assistant
#%%{summary}.

%package -n qt6-designer
Summary: Design GUIs for Qt6 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n qt6-designer
%{summary}.

%package -n qt6-linguist
Summary: Qt6 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n qt6-linguist
Tools to add translations to Qt6 applications.

%package -n qt6-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt6:Requires: %{_qt6}%{?_isa} >= %{_qt6_version}}
%description -n qt6-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n qt6-doctools
Summary: Qt6 doc tools package
%description -n qt6-doctools
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%setup -q -n %{name}-%{version}/upstream

%patch -P1 -p1 -b .run-qttools-with-qt6-suffix
%ifarch %{mips32}
%patch -P2 -p1 -b .libatomic
%endif

%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF} \
  -DQT_FEATURE_assistant:BOOL=OFF

%cmake_build


%install
%cmake_install

# Add desktop files, --vendor=... helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt6" \
  %{SOURCE21} %{SOURCE22} %{SOURCE23}
#  %%{SOURCE20} %%{SOURCE21} %%{SOURCE22} %%{SOURCE23}

%if 0%{?metainfo}
install -Dm0644 -t %{buildroot}%{_metainfodir} \
  %{SOURCE31} %{SOURCE32} %{SOURCE33}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
%endif

# icons
#install -m644 -p -D src/assistant/assistant/images/assistant.png %%{buildroot}%%{_datadir}/icons/hicolor/32x32/apps/assistant-qt6.png
#install -m644 -p -D src/assistant/assistant/images/assistant-128.png %%{buildroot}%%{_datadir}/icons/hicolor/128x128/apps/assistant-qt6.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer-qt6.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt6.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt6.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt6.png
done

# hardlink files to {_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool| \
   qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator| \
   qtplugininfo|qdistancefieldgenerator|qdoc|qtdiag)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ln -sv ${i} ${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd



%files
%{_bindir}/qdbus-qt6
%{_qt6_bindir}/qdbus
%{_qt6_bindir}/qdbus-qt6
%{_qt6_libdir}/libQt6UiTools.so.6*

%files common
%license LICENSES/LGPL*

%files  libs-designer
%{_qt6_libdir}/libQt6Designer.so.6*
%dir %{_qt6_libdir}/cmake/Qt6Designer/
%{_qt6_plugindir}/designer/*

%files  libs-designercomponents
%{_qt6_libdir}/libQt6DesignerComponents.so.6*

#%%files  libs-help
#%%{_qt6_libdir}/libQt6Help.so.6*

#%%files -n qt6-assistant
#%%{_bindir}/assistant-qt6
#%%{_qt6_bindir}/assistant*
#%%{_datadir}/applications/*assistant.desktop
#%%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt6-doctools
#{_bindir}/qdoc*
#{_qt6_bindir}/qdoc*
%{_bindir}/qdistancefieldgenerator*
%{_qt6_bindir}/qdistancefieldgenerator*
#%%{_qt6_libexecdir}/qhelpgenerator*
%{_qt6_libexecdir}/qtattributionsscanner*

%files -n qt6-designer
%{_bindir}/designer*
%{_qt6_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.Designer.metainfo.xml
%endif

%files -n qt6-linguist
%{_bindir}/linguist*
%{_qt6_bindir}/linguist*
# phrasebooks used by linguist
%{_datadir}/qt6/phrasebooks/*.qph
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*.*
# linguist friends
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_qt6_bindir}/lconvert*
%{_qt6_bindir}/lrelease*
%{_qt6_bindir}/lupdate*
%{_qt6_libexecdir}/lprodump*
%{_qt6_libexecdir}/lrelease*
%{_qt6_libexecdir}/lupdate*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.Linguist.metainfo.xml
%endif

%files -n qt6-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt6_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.qdbusviewer.metainfo.xml
%endif

%files devel
%{_bindir}/pixeltool*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt6_bindir}/pixeltool*
%{_qt6_bindir}/qtdiag*
%{_qt6_bindir}/qtplugininfo*
%{_qt6_headerdir}/QtQDocCatch/
%{_qt6_headerdir}/QtQDocCatchConversions/
%{_qt6_headerdir}/QtQDocCatchGenerators/
%{_qt6_headerdir}/QtDesigner/
%{_qt6_headerdir}/QtDesignerComponents/
#%%{_qt6_headerdir}/QtHelp/
%{_qt6_headerdir}/QtUiPlugin
%{_qt6_headerdir}/QtUiTools/
%{_qt6_headerdir}/QtTools/
%{_qt6_libdir}/libQt6Designer*.so
#%%{_qt6_libdir}/libQt6Help.so
%{_qt6_libdir}/libQt6UiTools.so
%{_qt6_libdir}/cmake/Qt6/FindWrapLibClang.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Designer/*.cmake
%{_qt6_libdir}/cmake/Qt6DesignerComponentsPrivate/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchPrivate
%{_qt6_libdir}/cmake/Qt6QDocCatchPrivate/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchConversionsPrivate
%{_qt6_libdir}/cmake/Qt6QDocCatchConversionsPrivate/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate
%{_qt6_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate/*.cmake
#%%dir %%{_qt6_libdir}/cmake/Qt6Help/
#%%{_qt6_libdir}/cmake/Qt6Help/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Linguist
%{_qt6_libdir}/cmake/Qt6Linguist/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6LinguistTools
%{_qt6_libdir}/cmake/Qt6LinguistTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6UiPlugin/
%{_qt6_libdir}/cmake/Qt6UiPlugin/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Tools/
%{_qt6_libdir}/cmake/Qt6Tools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6ToolsTools/
%{_qt6_libdir}/cmake/Qt6ToolsTools/*.cmake
%{_qt6_libdir}/cmake/Qt6UiTools/
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatch_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatchconversions_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatchgenerators_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designer.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designercomponents_private.pri
#%%{_qt6_archdatadir}/mkspecs/modules/qt_lib_help.pri
#%%{_qt6_archdatadir}/mkspecs/modules/qt_lib_help_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_linguist.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_tools_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uiplugin.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uitools.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uitools_private.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc

%files static
%{_qt6_libdir}/libQt6Designer*.prl
#%%{_qt6_libdir}/libQt6Help.prl
%{_qt6_libdir}/libQt6UiTools.prl

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

