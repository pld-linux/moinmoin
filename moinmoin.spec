
%define	module	moin
%define _rc	beta4

Summary:	Wiki Engine
Summary(pl.UTF-8):   Silnik Wiki
Name:		moinmoin
Version:	1.5.0
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/moin/%{module}-%{version}%{_rc}.tar.gz
# Source0-md5:	ce48757dff4bcc273fa43403f52454cb
Patch0:		%{name}-userform_customization.patch
Patch1:		%{name}-quickhelp.patch
URL:		http://moinmoin.wikiwikiweb.de/
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-modules
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MoinMoin is a nice and easy WikiEngine with advanced features - said
in a few words, it is about collaboration on easily editable web
pages.

%description -l pl.UTF-8
MoinMoin to przyjemny i łatwy silnik Wiki z zaawansowanymi
możliwościami - mówiąc w kilku słowach dotyczy współpracy przy łatwo
modyfikowalnych stronach WWW.

%prep
%setup -q -n %{module}-%{version}%{_rc}
%patch0 -p1
%patch1 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT
rm -rf docs/licenses

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog docs/*
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/MoinMoin
%{_datadir}/moin
