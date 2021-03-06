%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define	major 0
%define	libobs %mklibname obs %{major}
%define	libobsglad %mklibname obsglad %{major}
%define	libobsopengl %mklibname obs-opengl %{major}
%define	libobsfrontendapi  %mklibname obs-frontend-api %{major}
%define	devobs %mklibname obs -d

%define	oname	obs

# This package requires x264 codec so we provide it in Restricted repository
%define	distsuffix plf

Summary:	Free and open source software for video recording and live streaming
Name:		obs-studio
Version:	27.0.1
Release:	1
License:	GPLv2+
Group:		Video
Url:		https://obsproject.com
Source0:	https://github.com/obsproject/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-26.0.0-rc1-linkage.patch
Patch1:		hevc-vaapi.diff
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
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libswresample)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libvlc)
BuildRequires:	pkgconfig(MagickCore)
BuildRequires:	pkgconfig(Qt5Core) >= 5.7
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Xml)
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
BuildRequires:	pkgconfig(lua)
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
%{_libdir}/libobs.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libobsglad}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libobsglad}
Shared library for %{name}.

%files -n %{libobsglad}
%doc COPYING README.rst
%{_libdir}/libobsglad.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libobsopengl}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{libobsfrontendapi} = %{EVRD}

%description -n %{libobsopengl}
Shared library for %{name}.

%files -n %{libobsopengl}
%doc COPYING README.rst
%{_libdir}/libobs-opengl.so.%{major}*

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
%dir %{_libdir}/cmake/LibObs
%{_libdir}/cmake/LibObs/*.cmake
%{_libdir}/pkgconfig/libobs.pc

#----------------------------------------------------------------------------

%package -n %{libobsfrontendapi}
Summary:	Frontend-api library for %{name}	
Group:		System/Libraries

%description -n %{libobsfrontendapi}
Frontend-api library for %{name}.

%files -n %{libobsfrontendapi}
%doc COPYING README.rst
%{_libdir}/libobs-frontend-api.so.%{major}*

#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-%{version} -p1
%cmake	-DUNIX_STRUCTURE=1 \
	-DOBS_MULTIARCH_SUFFIX=$(echo %{_lib} |sed -e 's,^lib,,') \
	-DOBS_VERSION_OVERRIDE="%{version}" \
	-DBUILD_BROWSER=OFF \
	-DBUILD_VST=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
