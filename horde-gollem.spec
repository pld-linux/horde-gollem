
%define	_beta	rc1
%define	_rel	1

%include	/usr/lib/rpm/macros.php
Summary:	Gollem - the Horde File Manager
Summary(pl):	Gollem - zarz±dca plików Horde
Name:		gollem
Version:	1.0
Release:	0.%{_beta}.1
License:	GPL
Group:		Applications/WWW
Source0:	http://ftp.horde.org/pub/gollem/%{name}-%{version}-%{_beta}.tar.gz
# Source0-md5:	a60aa2a22ab33ef118beafa57cb1b927
Source1:	%{name}.conf
Patch0:		%{name}-prefs.patch
URL:		http://www.horde.org/gollem/
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc	CREDITS
%define		_noautoreq		'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org

%description
Gollem is the Horde File Manager, and works through any Horde_VFS
driver. It is currently in development, but all basic functionality is
available and works well. It uses Horde's MIME_Viewer framework to
identify file types, associate icons, etc.

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Gollem) please visit <http://www.horde.org/>.

%description -l pl
Gollem to zarz±dca plików Horde dzia³aj±cy poprzez sterownik
Horde_VFS. Aktualnie jest rozwijany, ale ca³a podstawowa
funkcjonalno¶æ jest ju¿ dostêpna i dzia³a dobrze. U¿ywa szkieletu
Horde MIME_Viewer do identyfikowania typów plików, wi±zania z nimi
ikon itp.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
Genral Public License. Wiêcej informacji (w³±cznie z pomoc± dla
Gollema) mo¿na znale¼æ na stronie <http://www.horde.org/>.

%prep
%setup -q -n %{name}-%{version}-%{_beta}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -p config/conf.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR locale/*			$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR themes/*			$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/credentials.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
