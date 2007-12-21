%define name		cunit
%define Name		CUnit
%define version		2.1.0
%define bad_version	2.1-0
%define release		%mkrel 3
%define	major		1
%define	libname		%mklibname %{name} %{major}

Name:		    %{name}
Version:	    %{version}
Release:	    %{release}
License:	    GPL
Summary:	    A Unit Testing Framework for C
Group:		    System/Libraries
URL:		    http://cunit.sourceforge.net
Source:		    http://prdownloads.sourceforge.net/cunit/%{Name}-%{bad_version}-src.tar.gz
Patch0:         %{name}-2.1.0.link_against_ncurses.patch
BuildRequires:  ncurses-devel
BuildRequires:  automake1.9
BuildRequires:  autoconf2.5
Buildroot:	    %{_tmppath}/%{name}-%{version}

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

%package -n	%{libname}
Summary:	C testing framework
Group:		System/Libraries

%description -n	%{libname}
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

%package -n	%{libname}-devel 
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
This package contains development files for %{name}.

%prep
%setup -q -n %{Name}-%{bad_version}
%patch0 -p 0
chmod 644 AUTHORS COPYING NEWS ChangeLog README TODO INSTALL VERSION

%build
automake-1.9
autoconf
%configure --enable-curses
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
install -m 644 AUTHORS COPYING NEWS ChangeLog README TODO INSTALL VERSION \
    %{buildroot}%{_datadir}/doc/%{libname}-devel-%{version} 
rm -rf %{buildroot}%{_prefix}/doc

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_datadir}/doc/%{libname}-devel-%{version}
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/%{Name}
%{_datadir}/%{Name}
%{_mandir}/man3/*


