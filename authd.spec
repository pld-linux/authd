Summary:	a RFC 1413 ident protocol daemon
Name:		authd
Version:	1.4.1
Release:	1.fc3
License:	GPL
Group:		System Environment/Daemons
######		Unknown group!
Obsoletes:	pidentd
Provides:	pidentd = 3.2
Requires:	openssl
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	openssl-devel

%description
authd is a small and fast RFC 1413 ident protocol daemon with both
xinetd server and interactive modes that supports IPv6 and IPv4 as
well as the more popular features of pidentd.

%prep
%setup -q
sed -i -e "s|/etc|%{_sysconfdir}|" config.h

%build
%{__make} prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d

install -m 644 xinetd.conf.auth ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d/auth
sed -i -e 's|/usr/local|/usr|' ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d/auth

touch ${RPM_BUILD_ROOT}%{_sysconfdir}/ident.key

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/adduser -s /sbin/nologin -r ident 2>/dev/null || true
/usr/bin/openssl rand -base64 -out %{_sysconfdir}/ident.key 32
echo CHANGE THE LINE ABOVE TO A PASSPHRASE >> %{_sysconfdir}/ident.key
/bin/chown ident:ident %{_sysconfdir}/ident.key
chmod o-rw %{_sysconfdir}/ident.key

%files -f authd.lang
%defattr(644,root,root,755)
%doc COPYING README.html rfc1413.txt
%config(noreplace) %{_sysconfdir}/xinetd.d/auth
%config %{_sysconfdir}/ident.key
%attr(755,root,root) %{_sbindir}/in.authd
