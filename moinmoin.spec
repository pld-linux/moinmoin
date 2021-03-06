# TODO
# - for lighttpd: http://permalink.gmane.org/gmane.comp.web.lighttpd/3140
# - http://moinmoin.wikiwikiweb.de/HelpOnInstalling/FastCgi
%define				module	moin
Summary:	Wiki Engine
Summary(pl.UTF-8):	Silnik Wiki
Name:		moinmoin
Version:	1.5.9
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://static.moinmo.in/files/%{module}-%{version}.tar.gz
# Source0-md5:	03025422c5addcbe9ccce3df2dde470c
Source1:	%{name}-apache.conf
Source2:	%{name}-httpd.conf
Patch0:		%{name}-config.patch
URL:		http://www.moinmo.in/
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-modules > 1:2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	pydoc
Requires:	webapps
%pyrequires_eq	python-modules
Conflicts:	apache-base < 2.4.0-1
Conflicts:	docutils < 0.4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
MoinMoin is a nice and easy WikiEngine with advanced features - said
in a few words, it is about collaboration on easily editable web
pages.

%description -l pl.UTF-8
MoinMoin to przyjemny i łatwy silnik Wiki z zaawansowanymi
możliwościami - mówiąc w kilku słowach dotyczy współpracy przy łatwo
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
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

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

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc docs/* config
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
/var/lib/moin/data/meta
#/var/lib/moin/underlay/meta
