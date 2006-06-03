# TODO
# - for lighttpd: http://permalink.gmane.org/gmane.comp.web.lighttpd/3140
# - http://moinmoin.wikiwikiweb.de/HelpOnInstalling/FastCgi
%define	module	moin
Summary:	Wiki Engine
Summary(pl):	Silnik Wiki
Name:		moinmoin
Version:	1.5.3
Release:	0.7
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/moin/%{module}-%{version}.tar.gz
# Source0-md5:	e95ec46ee8de9527a39793108de22f7d
Source1:	%{name}-apache.conf
Patch0:		%{name}-config.patch
URL:		http://moinmoin.wikiwikiweb.de/
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-modules > 1:2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	pydoc
Requires:	webapps
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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
%patch0 -p1

rm -rf docs/licenses
rm -f wiki/data/user/README
rm -f wiki/server/mointwisted.cmd
rm -rf wiki/data/cache

# omit /usr/bin/env dep and let rpm autogenerate python binary dep
%{__sed} -i -e  '1s,^#!.*python,#!%{__python},' wiki/server/*
mv wiki/server/moinmodpy.htaccess .

# prepare inclusion into %doc
mkdir -p config
mv wiki/config/{more_samples,wikifarm} config

# dos, windows,.. blah
%{__sed} -i -e 's,\r$,,' wiki/data/intermap.txt

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/{cache,lib}/moin}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{%{_datadir}/moin/config/*.py,%{_sysconfdir}}
rm -f $RPM_BUILD_ROOT%{_datadir}/moin/config/*.py[co]

# FHS friendly
mv $RPM_BUILD_ROOT{%{_datadir}/moin/data,/var/lib/moin/data}
# it needs rw on underlay, so move it also to /var
mv $RPM_BUILD_ROOT{%{_datadir}/moin/underlay,/var/lib/moin/underlay}

# create dirs / files it creates by on it's own
install -d $RPM_BUILD_ROOT/var/lib/moin/data/cache/{i18n,surgeprotect,wikidicts}/__lock__
touch $RPM_BUILD_ROOT/var/lib/moin/data/{event-log,error.log}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc ChangeLog docs/* config
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.py
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/MoinMoin
%dir %{_datadir}/moin
%{_datadir}/moin/config
%{_datadir}/moin/htdocs
%dir %{_datadir}/moin/server
%attr(755,root,root) %{_datadir}/moin/server/*

%dir /var/lib/moin
%dir /var/lib/moin/underlay
%defattr(660,root,http,770)
/var/lib/moin/underlay/pages
%dir /var/lib/moin/data
/var/lib/moin/data/plugin
%config(missingok,noreplace) %verify(not md5 mtime size) /var/lib/moin/data/pages
%config(missingok,noreplace) %verify(not md5 mtime size) /var/lib/moin/data/user
%config(missingok,noreplace) %verify(not md5 mtime size) /var/lib/moin/data/dict
%config(missingok,noreplace) %verify(not md5 mtime size) /var/lib/moin/data/cache
%ghost /var/lib/moin/data/edit-log
%ghost /var/lib/moin/data/event-log
%ghost /var/lib/moin/data/error.log
/var/lib/moin/data/intermap.txt
