%global commit0 3a6dff883eca34a20d76f82cf4bb87e2d4111a97
%global date 20151228
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%define debug_package %{nil}

Name:    winconn
Version: 0.2.14
Release: 2%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary: RemoteApp manager

License: GPLv3
URL: http://stanev.org/winconn/
Source0: https://github.com/RealEnder/winconn/archive/%{commit0}/winconn-%{commit0}.tar.gz#/winconn-%{shortcommit0}.tar.gz
BuildArch: noarch

BuildRequires: python2-devel
%if 0%{?el} <= 7
BuildRequires: python-distutils-extra
%else
BuildRequires: python2-distutils-extra
%endif
BuildRequires: glib2
BuildRequires: intltool

# Reference: https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=winconn&id=b5556af521c63aabe34c4911a6dfaa3b9cec270f
Requires: gtk3
Requires: gobject-introspection
Requires: libappindicator-gtk3
Requires: yelp
Requires: freerdp
Requires: xdg-utils
Requires: dbus-python
# It seems odd that this requires gtk3 but pygobject2, but it does, both
# emperically and according to the ubuntu control file that upstream ships.
Requires: pygobject2

%description
WinConn simplifies creation, management and desktop integration of remote windows applications in Linux. It uses RemoteApp technology, implemented by FreeRDP project to provide seamless user experience. The applications run in their own window and can be used like any other locally installed Linux application, without bringing the full windows desktop to the user.

%prep
%autosetup -n %{name}-%{commit0}

%build
%py2_build

%install
# Workaround winconn.desktop never being installed
install -D ./build/share/applications/winconn.desktop %{buildroot}/usr/share/applications/winconn.desktop

%py2_install

# remove /etc/apport/crashdb.conf.d/winconn-crashdb.conf
# this is the only file created under /etc and Apport is Ubuntu-specific
rm -rf %{buildroot}/etc
# Also remove the Apport files under /usr/share/apport/package-hooks/
rm -rf %{buildroot}/usr/share/apport/

%files
%{_bindir}/winconn
%{python2_sitelib}/winconn-0.2.14-py2.7.egg-info
%{python2_sitelib}/winconn/*
%{python2_sitelib}/winconn_lib/*
%{_datadir}/applications/winconn.desktop
%{_datadir}/winconn/media/*
%{_datadir}/winconn/ui/*

%changelog
* Sat Dec 03 2016 Mike DePaulo <mikedep333@gmail.com> - 0.2.14-2.20151228git3a6dff8
- Fix gobject dependency

* Sun Nov 27 2016 Mike DePaulo <mikedep333@gmail.com> - 0.2.14-1.20151228git3a6dff8
- Initial version
