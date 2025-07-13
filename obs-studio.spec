%define _disable_ld_no_undefined 1
%define _disable_lto 1

# Current status of CEF plugin: It compiles, but crashes when trying
# to use the browser
%bcond_without cef
%define cef_version 6533

%define	libobs %mklibname obs
%define	libobsfrontendapi  %mklibname obs-frontend-api
%define	libobsscripting  %mklibname obs-scripting
%define	devobs %mklibname obs -d

%define	oname	obs

# ffmpeg 6.1 deprecates a slew of things still used by obs
%global optflags %{optflags} -Wno-error=deprecated-declarations

# as of obs 31.0.0 and clang 19.1.2 needed or build failed with: call to '_curl_easy_setopt_err_write_callback' 
# declared with 'warning' attribute: curl_easy_setopt expects a curl_write_callback argument for this option [-Werror,-Wattribute-warning]
%global optflags %{optflags} -Wno-error=attribute-warning

# This package requires x264 codec so we provide it in Restricted repository
%define	distsuffix plf

#define beta rc1

Summary:	Free and open source software for video recording and live streaming
Name:		obs-studio
Version:	31.1.1
Release:	%{?beta:0.%{beta}.}1
License:	GPLv2+
Group:		Video
Url:		https://obsproject.com
Source0:	https://github.com/obsproject/%{name}/archive/%{version}/%{name}-%{version}%{?beta:-%{beta}}.tar.gz
# git submodules that have gone missing in 28.0 tarballs
Source1:	https://github.com/obsproject/obs-browser/archive/obs-browser-bdabf8300ecefeb566b81f4a7ff75f8a8e21f62b.tar.gz
Source2:	https://github.com/obsproject/obs-websocket/archive/obs-websocket-40d26dbf4d29137bf88cd393a3031adb04d68bba.tar.gz
#Source3:	https://github.com/obsproject/obs-amd-encoder/archive/5a1dafeddb4b37ca2ba2415cf88b40bff8aee428.tar.gz
%if %{with cef}
# Keep using it, intil we can provide system cef
Source3:	https://cdn-fastly.obsproject.com/downloads/cef_binary_%{cef_version}_linux_x86_64_v3.tar.xz
Source4:	https://cdn-fastly.obsproject.com/downloads/cef_binary_%{cef_version}_linux_aarch64_v4.tar.xz
%endif

#Patch0:		%{name}-27.1.0-linkage.patch
#Patch1:		obs-studio-29.1.0-clang16.patch
# The cmake dependency generator isn't smart enough
# to see that the w32-pthreads dependency is only
# in a condition that can never be true on a real OS
Patch2:		no-w32-pthreads-dep.patch
# Port the browser plugin to CEF 122.x
#Patch3:		obs-studio-cef-122.patch
#Patch3:		https://patch-diff.githubusercontent.com/raw/obsproject/obs-studio/pull/11618.patch

# Needed because: https://github.com/obsproject/obs-studio/issues/12357
# Compile fine on GCC, for Clang require this patch:
Patch3:		clang.patch

BuildRequires:	cmake ninja
BuildRequires:	cmake(ECM)
BuildRequires:	freetype-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavdevice)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(fdk-aac)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libswresample)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libvlc)
BuildRequires:	pkgconfig(MagickCore)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libvlc)
BuildRequires:	pkgconfig(nlohmann_json)
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	qt6-cmake
BuildRequires:	qmake-qt6
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:	cmake(vulkanheaders)
%ifarch %{x86_64}
BuildRequires:	pkgconfig(vpl)
%endif
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-randr)
BuildRequires:	pkgconfig(xcb-shm)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcb-xinerama)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(luajit)
BuildRequires:	swig
BuildRequires:	mbedtls-devel
BuildRequires:	sndio-devel
BuildRequires:  uthash-devel
%if %{with cef}
#BuildRequires:	cef-devel
%endif

# Build dependencies from restricted repo. If needed OSB-Studio can be moved to main repo and below deps disabled
# Build with this deps only for OBS-Studio from restricted repo.
BuildRequires:	pkgconfig(x264)
BuildRequires:  pkgconfig(x265)
BuildRequires:	pkgconfig(fdk-aac)

#Libva is needed for enable hardware encoding via vaapi.(penguin).
%ifnarch %{ix86}
Requires:	lib64va2
%endif
%ifarch %{ix86}
Requires:	libva2
%endif
Requires: x264
Requires: x265
Requires: %{_lib}Qt6WlShellIntegration

# Used via dlopen() so require them, otherwise they don't get installed
Requires:	%{libobs} = %{EVRD}

# Libraries that existed in previous versions
%define	libobsglad %mklibname obsglad
%define	libobsopengl %mklibname obs-opengl
Obsoletes:	%{libobsglad} < %{EVRD}
Obsoletes:	%{libobsopengl} < %{EVRD}

%description
Free and open source software for video recording and live streaming.
This package is in the Restricted repository because it requires x264 codec.

%files
%{_bindir}/%{oname}
%{_bindir}/%{oname}-ffmpeg-mux
%ifarch %{x86_64}
%{_bindir}/obs-nvenc-test
%endif
%{_datadir}/applications/com.obsproject.Studio.desktop
%{_datadir}/metainfo/com.obsproject.Studio.metainfo.xml
%dir %{_datadir}/%{oname}/
%{_datadir}/%{oname}/*
%{_iconsdir}/hicolor/*/apps/*
%dir %{_libdir}/%{oname}-plugins/
%{_libdir}/%{oname}-plugins/frontend-tools.so
%{_libdir}/%{oname}-plugins/image-source.so
%{_libdir}/%{oname}-plugins/linux-*.so
%{_libdir}/%{oname}-plugins/obs-*.so
%exclude %{_libdir}/%{oname}-plugins/obs-browser.so
%{_libdir}/%{oname}-plugins/rtmp-services.so
%{_libdir}/%{oname}-plugins/text-freetype2.so
%{_libdir}/obs-scripting
%{_libdir}/libobs-opengl.so*

#----------------------------------------------------------------------------

%package plugin-vlc
Summary:	VLC player support plugin for OBS Studio
Group:		Video
Requires:	%{name} = %{EVRD}

%description plugin-vlc
VLC player support plugin for OBS Studio

%files plugin-vlc
%{_libdir}/%{oname}-plugins/vlc-video.so

#----------------------------------------------------------------------------

%package plugin-decklink
Summary:	DeckLink hardware support plugin for OBS Studio
Group:		Video
Requires:	%{name} = %{EVRD}

%description plugin-decklink
DeckLink hardware support plugin for OBS Studio

%files plugin-decklink
%{_libdir}/%{oname}-plugins/decklink*.so

#----------------------------------------------------------------------------
%if %{with cef}
%package plugin-browser
Summary:	Web browser plugin for OBS Studio
Group:		Video
Requires:	%{name} = %{EVRD}

%description plugin-browser
Web browser plugin for OBS Studio

%files plugin-browser -f browser.lang
%{_libdir}/obs-plugins/obs-browser.so
%{_libdir}/obs-plugins/chrome-sandbox
%{_libdir}/obs-plugins/chrome_100_percent.pak
%{_libdir}/obs-plugins/chrome_200_percent.pak
%{_libdir}/obs-plugins/icudtl.dat
%{_libdir}/obs-plugins/libEGL.so
%{_libdir}/obs-plugins/libGLESv2.so
%{_libdir}/obs-plugins/libcef.so
%{_libdir}/obs-plugins/libvk_swiftshader.so
%{_libdir}/obs-plugins/libvulkan.so.1
%{_libdir}/obs-plugins/obs-browser-page
%{_libdir}/obs-plugins/resources.pak
%{_libdir}/obs-plugins/v8_context_snapshot.bin
%{_libdir}/obs-plugins/vk_swiftshader_icd.json
%endif
#----------------------------------------------------------------------------

%package -n %{libobs}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libobs}
Shared library for %{name}.

%files -n %{libobs}
%{_libdir}/libobs.so.*

#----------------------------------------------------------------------------

%package -n %{devobs}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libobs} = %{EVRD}
Requires:	%{libobsfrontendapi} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{oname}-devel = %{EVRD}

%description -n %{devobs}
Development files for %{name}

%files -n %{devobs}
%dir %{_includedir}/%{oname}
%{_includedir}/%{oname}/*
%{_libdir}/libobs.so
%{_libdir}/libobs-frontend-api.so
%{_libdir}/cmake/libobs
%{_libdir}/cmake/obs-frontend-api
%{_libdir}/cmake/obs-websocket-api/
%{_libdir}/pkgconfig/libobs.pc
%{_libdir}/pkgconfig/obs-frontend-api.pc

#----------------------------------------------------------------------------

%package -n %{libobsfrontendapi}
Summary:	Frontend-api library for %{name}	
Group:		System/Libraries

%description -n %{libobsfrontendapi}
Frontend-api library for %{name}.

%files -n %{libobsfrontendapi}
%{_libdir}/libobs-frontend-api.so.*

#----------------------------------------------------------------------------

%package -n %{libobsscripting}
Summary:	Scripting library for %{name}	
Group:		System/Libraries

%description -n %{libobsscripting}
Scripting library for %{name}.

%files -n %{libobsscripting}
%{_libdir}/libobs-scripting.so.*
%{_libdir}/libobs-scripting.so

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}%{?beta:-%{beta}}

cd plugins
rmdir obs-browser obs-websocket
tar xf %{S:1}
tar xf %{S:2}
mv obs-browser-* obs-browser
mv obs-websocket-* obs-websocket
cd ..
%if %{with cef}
%ifarch %{x86_64}
tar -xf %{SOURCE3}
%endif
%ifarch %{aarch64}
tar -xf %{SOURCE4}
%endif
%endif

%autopatch -p1
export CC=gcc
export CXX=g++
%cmake	-DUNIX_STRUCTURE=1 \
	-DOBS_MULTIARCH_SUFFIX=$(echo %{_lib} |sed -e 's,^lib,,') \
	-DOBS_VERSION_OVERRIDE="%{version}" \
	-DENABLE_LIBFDK=ON \
  	-DENABLE_JACK=ON \
%if %{with cef}
 	-DENABLE_BROWSER=ON \
%ifarch %{x86_64}  
 	-DCEF_ROOT_DIR="../cef_binary_%{cef_version}_linux_x86_64" \
%endif
%ifarch %{aarch64}
	-DCEF_ROOT_DIR="../cef_binary_%{cef_version}_linux_aarch64" \
%endif
%else
	-DBUILD_BROWSER=OFF \
%endif
	-DENABLE_WEBSOCKET=OFF \
	-DBUILD_VST=OFF \
	-DENABLE_NEW_MPEGTS_OUTPUT=OFF \
	-DENABLE_AJA=OFF \
 	-DENABLE_WEBRTC=OFF \
  	-DENABLE_NATIVE_NVENC:BOOL=ON \
%ifnarch %{x86_64}
	-DENABLE_QSV11=OFF \
%endif
	-G Ninja
# Use it in case of system cef and not external/ 
# -DCEF_ROOT_DIR=%{_libdir}/cef \

%build
export CC=gcc
export CXX=g++
%ninja_build -C build

%install
%ninja_install -C build

echo '%%dir %{_libdir}/obs-plugins/locales' >browser.lang
for i in %{buildroot}%{_libdir}/obs-plugins/locales/*.pak; do
	L="`basename $i .pak`"
	echo "%%lang($L) %{_libdir}/obs-plugins/locales/$L.pak*" >>browser.lang
done
