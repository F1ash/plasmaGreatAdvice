Name: kde-plasma-motivator
Version: 1.2
Release: 1%{?dist}
Summary: Funny plasmoid for joke or motivation to work activities and keeping a good mood. 21 + .
Summary(ru): Плазмоид-шутка для мотивации трудовой деятельности и просто хорошего настроения.
Group: Applications/Network
License: GPL
Source0: http://cloud.github.com/downloads/F1ash/plasmaGreatAdvice/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/plasmaGreatAdvice
BuildArch: noarch

Requires: python, PyQt4, PyKDE4

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
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/kde4/apps/plasma/plasmoids/%{name}
cp -r * $RPM_BUILD_ROOT/%{_datadir}/kde4/apps/plasma/plasmoids/%{name}/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/kde4/services
cp -r metadata.desktop $RPM_BUILD_ROOT/%{_datadir}/kde4/services/%{name}.desktop

%files
%defattr(-,root,root)
%{_datadir}/kde4/services/%{name}.desktop
%{_datadir}/kde4/apps/plasma/plasmoids/%{name}/*
%dir %{_datadir}/kde4/apps/plasma/plasmoids/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Mon Aug 22 2011 Fl@sh <kaperang07@gmail.com> - 1.2-1
- Initial build
