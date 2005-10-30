%define		_modname	mailparse
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%{_libdir}/php4

Summary:	Email message manipulation
Summary(pl):	Obrabianie wiadomo¶ci E-mail
Name:		php4-pecl-%{_modname}
Version:	2.1.1
Release:	2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	14c058d79f1f6c01aa53273565bd4a54
URL:		http://pecl.php.net/package/mailparse/
BuildRequires:	php4-devel
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.

In PECL status of this package is: %{_status}.

%description -l pl
Mailparse to rozszerzenie do analizy i pracy z wiadomo¶ciami poczty
elektronicznej. Radzi sobie z wiadomo¶ciami zgodnymi z RFC822 oraz
RFC2024 (MIME).

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
