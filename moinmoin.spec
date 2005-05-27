
%define	module	moin

Summary:	Wiki Engine
Summary(pl):	Silnik Wiki
Name:		moinmoin
Version:	1.3.4
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/moin/%{module}-%{version}.tar.gz
# Source0-md5:	9d72e2cc6382d6dc8408bf0f9ccb1398
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

%description -l pl
MoinMoin to przyjemny i ³atwy silnik Wiki z zaawansowanymi
mo¿liwo¶ciami - mówi±c w kilku s³owach dotyczy wspó³pracy przy ³atwo
modyfikowalnych stronach WWW.

%prep
%setup -q -n %{module}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README INSTALL.html UPDATE.html
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/MoinMoin
%{_datadir}/moin
