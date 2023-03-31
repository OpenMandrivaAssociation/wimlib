%define major 15
%define prename wim
%define libname %mklibname %{prename} %{major}
%define devname %mklibname %{prename} -d
%define binname %{prename}tools

Summary: The open source Windows Imaging (WIM) library
Name:    %{prename}lib
Version: 1.13.6
Release: 2
# Most files are licensed under LGPLv3+, a few under MIT.
# According to the author, GPLv3+ kicks in when linking to libntfs-3g.
# In theory that only applies to static linking, but let's play safe.
License: GPLv3+ and MIT
Group:   Development/Other
Url:     https://%{name}.net
Source0: https://github.com/ebiggers/wimlib/archive/refs/tags/v%{version}.tar.gz

BuildRequires: chrpath
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(libntfs-3g)
BuildRequires: pkgconfig(libxml-2.0)

%description
wimlib is a C library for creating, modifying, extracting,
and mounting files in the Windows Imaging Format (WIM files).
wimlib and its command-line frontend 'wimlib-imagex' provide a free
and cross-platform alternative to Microsoft's WIMGAPI, ImageX, and DISM.

%package -n %{libname}
Summary:  %{summary}
Group:    %{group}
Provides: %{name} = %{version}-%{release}

%description -n %{libname}
This package contains the %{name} runtime libraries.

%package -n %{devname}
Summary:  %{summary}
Group:    %{group}
Requires: %{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the %{name} development headers and libraries.

%package -n %{binname}
Summary:  Tools to create, extract, modify, and mount WIM files
Group:    %{group}
Provides: %{binname} = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description -n %{binname}
This package contains the %{name} tools.

%prep
%autosetup -n %{name}-%{version}

%build
./bootstrap

%configure --disable-static \
           --prefix=%{_prefix}

%make_build

%install
%make_install

shopt -s extglob
rm -r examples/!(*.c)

%files -n %{libname}
%{_libdir}/lib%{prename}.so.%{major}*

%files -n %{devname}
%doc NEWS README examples
%license COPYING COPYING.GPLv3
%{_libdir}/lib%{prename}.so
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{binname}
%{_bindir}/*
%{_mandir}/man*/*
