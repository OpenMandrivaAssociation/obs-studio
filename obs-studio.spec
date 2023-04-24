%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define	libobs %mklibname obs
%define	libobsglad %mklibname obsglad
%define	libobsopengl %mklibname obs-opengl
%define	libobsfrontendapi  %mklibname obs-frontend-api
%define	libobsscripting  %mklibname obs-scripting
%define	devobs %mklibname obs -d

%define	oname	obs

# This package requires x264 codec so we provide it in Restricted repository
%define	distsuffix plf

Summary:	Free and open source software for video recording and live streaming
Name:		obs-studio
Version:	29.0.2
Release:	2
License:	GPLv2+
Group:		Video
Url:		https://obsproject.com
Source0:	https://github.com/obsproject/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# git submodules that have gone missing in 28.0 tarballs
Source1:	https://github.com/obsproject/obs-browser/archive/b6e0888084ab623f0a73e8cb7ee5dc341e56fda1.tar.gz
Source2:	https://github.com/obsproject/obs-websocket/archive/5716577019b1ccda01a12db2cba35a023082b7ad.tar.gz
#Source3:	https://github.com/obsproject/obs-amd-encoder/archive/5a1dafeddb4b37ca2ba2415cf88b40bff8aee428.tar.gz

#Patch0:		%{name}-27.1.0-linkage.patch
Patch1:		hevc-vaapi.diff
# The cmake dependency generator isn't smart enough
# to see that the w32-pthreads dependency is only
# in a condition that can never be true on a real OS
Patch2:		no-w32-pthreads-dep.patch
BuildRequires:	cmake ninja
BuildRequires:	qmake5
BuildRequires:	freetype-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
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
BuildRequires:	qt6-cmake
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

# Used via dlopen() so require them, otherwise they don't get installed
Requires:	%{libobsopengl} = %{EVRD}
Requires:	%{libobs} = %{EVRD}

%description
Free and open source software for video recording and live streaming.
This package is in the Restricted repository because it requires x264 codec.

%files
%doc COPYING README.rst
%{_bindir}/%{oname}
%{_bindir}/%{oname}-ffmpeg-mux
%{_datadir}/applications/com.obsproject.Studio.desktop
%{_datadir}/metainfo/com.obsproject.Studio.appdata.xml
%dir %{_datadir}/%{oname}/
%{_datadir}/%{oname}/*
%{_iconsdir}/hicolor/*/apps/*
%dir %{_libdir}/%{oname}-plugins/
%{_libdir}/%{oname}-plugins/*.so
%{_libdir}/libobs-scripting.so
%{_libdir}/obs-scripting

#----------------------------------------------------------------------------

%package -n %{libobs}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libobs}
Shared library for %{name}.

%files -n %{libobs}
%doc COPYING README.rst
%{_libdir}/libobs.so.*

#----------------------------------------------------------------------------

%package -n %{libobsglad}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libobsglad}
Shared library for %{name}.

%files -n %{libobsglad}
%doc COPYING README.rst
%{_libdir}/libobsglad.so.*

#----------------------------------------------------------------------------

%package -n %{libobsopengl}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{libobsfrontendapi} = %{EVRD}

%description -n %{libobsopengl}
Shared library for %{name}.

%files -n %{libobsopengl}
%doc COPYING README.rst
%{_libdir}/libobs-opengl.so.*

#----------------------------------------------------------------------------

%package -n %{devobs}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libobs} = %{EVRD}
Requires:	%{libobsglad} = %{EVRD}
Requires:	%{libobsopengl} = %{EVRD}
Requires:	%{libobsfrontendapi} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{oname}-devel = %{EVRD}

%description -n %{devobs}
Development files for %{name}

%files -n %{devobs}
%doc COPYING README.rst
%dir %{_includedir}/%{oname}
%{_includedir}/%{oname}/*
%{_libdir}/libobs.so
%{_libdir}/libobsglad.so
%{_libdir}/libobs-opengl.so
%{_libdir}/libobs-frontend-api.so
%{_libdir}/cmake/libobs
%{_libdir}/cmake/obs-frontend-api
%{_libdir}/pkgconfig/libobs.pc

#----------------------------------------------------------------------------

%package -n %{libobsfrontendapi}
Summary:	Frontend-api library for %{name}	
Group:		System/Libraries

%description -n %{libobsfrontendapi}
Frontend-api library for %{name}.

%files -n %{libobsfrontendapi}
%doc COPYING README.rst
%{_libdir}/libobs-frontend-api.so.*

#----------------------------------------------------------------------------

%package -n %{libobsscripting}
Summary:	Scripting library for %{name}	
Group:		System/Libraries

%description -n %{libobsscripting}
Scripting library for %{name}.

%files -n %{libobsscripting}
%{_libdir}/libobs-scripting.so.*

#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-%{version} -p1

cd plugins
rmdir obs-browser obs-websocket enc-amf
tar xf %{S:1}
tar xf %{S:2}
mv obs-browser-* obs-browser
mv obs-websocket-* obs-websocket
cd ..

%cmake	-DUNIX_STRUCTURE=1 \
	-DOBS_MULTIARCH_SUFFIX=$(echo %{_lib} |sed -e 's,^lib,,') \
	-DOBS_VERSION_OVERRIDE="%{version}" \
	-DENABLE_LIBFDK=ON \
  	-DENABLE_JACK=ON \
	-DBUILD_BROWSER=OFF \
	-DENABLE_WEBSOCKET=OFF \
	-DBUILD_VST=OFF \
	-DENABLE_NEW_MPEGTS_OUTPUT=OFF \
	-DENABLE_AJA=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
