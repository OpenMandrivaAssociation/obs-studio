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
Version:	21.0.3
Release:	1
License:	GPLv2+
Group:		Video
Url:		https://obsproject.com
Source0:	https://github.com/jp9000/obs-studio/archive/%{name}-%{version}.tar.gz
Patch0:		%{name}-20.0.1-linkage.patch
BuildRequires:	cmake
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
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libswresample)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libvlc)
BuildRequires:	pkgconfig(MagickCore)
BuildRequires:	pkgconfig(Qt5Core) >= 5.7
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-randr)
BuildRequires:	pkgconfig(xcb-shm)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcb-xinerama)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xfixes)
# Used via dlopen() so require them, otherwise they don't get installed
Requires:	%{libobsopengl} = %{EVRD}
Requires:	%{libobs} = %{EVRD}

%description
Free and open source software for video recording and live streaming.
This package is in the Restricted repository because it requires x264 codec.

%files
%doc COPYING README.rst
%{_bindir}/%{oname}
%{_datadir}/applications/%{oname}.desktop
%dir %{_datadir}/%{oname}/
%{_datadir}/%{oname}/*
%{_iconsdir}/hicolor/*/apps/%{oname}.png
%dir %{_libdir}/%{oname}-plugins/
%{_libdir}/%{oname}-plugins/*.so

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
%setup -q
%patch0 -p1


%build
%cmake	-DUNIX_STRUCTURE=1 \
%ifarch x86_64
		-DOBS_MULTIARCH_SUFFIX=64
%else
		-DOBS_MULTIARCH_SUFFIX=
%endif
%make


%install
%makeinstall_std -C build

%changelog

* Sun Oct 08 2017 Giovanni Mariani <mc2374@mclink.it> 20.0.1-1
- (287c532) Updated to release 20.0.1, updated BReqs according to the configure output and rediffed P0


