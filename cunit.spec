%define Name CUnit
%define bad_version 2.1-3
%define	major 1
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		cunit
Version:	2.1.3
Release:	1
License:	GPLv2+
Summary:	A Unit Testing Framework for C
Group:		System/Libraries
URL:		http://cunit.sourceforge.net
Source0:	http://sourceforge.net/projects/cunit/files/CUnit/%{bad_version}/%{Name}-%{bad_version}.tar.bz2
Patch0:		%{name}-2.1.0.link_against_ncurses.patch
BuildRequires:	pkgconfig(ncurses)

%description
CUnit is a lightweight system for writing, administering, and running unit
tests in C.  It provides C programmers a basic testing functionality with a
flexible variety of user interfaces.

CUnit is built as a static library which is linked with the user's testing
code.  It uses a simple framework for building test structures, and provides a
rich set of assertions for testing common data types. In addition, several
different interfaces are provided for running tests and reporting results.
These interfaces currently include:

- Automated: Non-interactive output to xml file
- Basic: Non-interactive flexible programming interface
- Console: Interactive console interface (ansi C)
- Curses: Interactive graphical interface (Unix)

%package -n %{libname}
Summary:	C testing framework
Group:		System/Libraries

%description -n %{libname}
CUnit is a lightweight system for writing, administering, and running unit
tests in C.  It provides C programmers a basic testing functionality with a
flexible variety of user interfaces.

CUnit is built as a static library which is linked with the user's testing
code.  It uses a simple framework for building test structures, and provides a
rich set of assertions for testing common data types. In addition, several
different interfaces are provided for running tests and reporting results.
These interfaces currently include:

- Automated: Non-interactive output to xml file
- Basic: Non-interactive flexible programming interface
- Console: Interactive console interface (ansi C)
- Curses: Interactive graphical interface (Unix)

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n	%{develname}
This package contains development files for %{name}.

%prep
%setup -q -n %{Name}-%{bad_version}
%patch0 -p 0
chmod 644 AUTHORS NEWS ChangeLog README TODO

%build
autoreconf -f -i
%configure2_5x \
	--enable-curses
%make

%install
%makeinstall_std

# fix la file
perl -pi -e 's| -L\S+ ||'  %{buildroot}%{_libdir}/libcunit.la

# ugly, but needed to deal with installed and non-installed documentation
install -d -m 755 %{buildroot}%{_datadir}/doc/%{libname}-devel-%{version}
mv %{buildroot}%{_prefix}/doc/%{Name} \
    %{buildroot}%{_datadir}/doc/%{libname}-devel-%{version}/html
install -m 644 AUTHORS NEWS ChangeLog README TODO \
    %{buildroot}%{_datadir}/doc/%{libname}-devel-%{version} 
rm -rf %{buildroot}%{_prefix}/doc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_datadir}/doc/%{libname}-devel-%{version}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{Name}
%{_datadir}/%{Name}
%{_mandir}/man3/*
