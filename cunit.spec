%define name cunit
%define Name CUnit
%define version 2.1.0
%define bad_version 2.1-0
%define release %mkrel 7
%define	major 1
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Summary:	A Unit Testing Framework for C
Group:		System/Libraries
URL:		http://cunit.sourceforge.net
Source:		http://prdownloads.sourceforge.net/cunit/%{Name}-%{bad_version}-src.tar.gz
Patch0:		%{name}-2.1.0.link_against_ncurses.patch
BuildRequires:	ncurses-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

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
aclocal
autoconf
automake

%configure2_5x \
	--enable-curses

%make

%install
rm -rf %{buildroot}
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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_datadir}/doc/%{libname}-devel-%{version}
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/%{Name}
%{_datadir}/%{Name}
%{_mandir}/man3/*
