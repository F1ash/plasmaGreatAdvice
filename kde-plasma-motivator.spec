Name: kde-plasma-motivator
Version: 1.0
Release: %(date +%Y%m%d_%H%M)%{?dist}
Summary: Funny plasmoid for joke or motivation to work activities and keeping a good mood. 21 + .
Summary(ru): Плазмоид-шутка для мотивации трудовой деятельности и просто хорошего настроения.
#Group: Applications/Network
License: GPL
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/plasmaGreatAdvice
BuildArch: noarch

%if %{defined fedora}
Requires: python >= 2.6, PyQt4 >= 4.7, PyKDE4 >= 4.6
Conflicts: python >= 3.0
BuildRequires: desktop-file-utils
%endif

%description
kde-plasma-motivator
Funny plasmoid for joke or motivation to work activities and keeping
a good mood. 21 + . On russian.

%description -l ru
kde-plasma-motivator
Плазмоид-шутка для мотивации трудовой деятельности и
просто хорошего настроения. Детям 21+ разрешается.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_kde4_appsdir}/plasma/plasmoids/%{name}
cp -r * $RPM_BUILD_ROOT/%{_kde4_appsdir}/plasma/plasmoids/%{name}/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/kde4/services
cp -r metadata.desktop $RPM_BUILD_ROOT/%{_datadir}/kde4/services/%{name}.desktop


%files
%defattr(-,root,root)
%{_datadir}/kde4/services/%{name}.desktop
%{_kde4_appsdir}/plasma/plasmoids/%{name}/*
%dir %{_kde4_appsdir}/plasma/plasmoids/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Sat Aug 13 2011 Fl@sh <no@mail.me>	-	1.0
-- Build began ;)

