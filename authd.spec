Summary:	A RFC 1413 ident protocol daemon
Summary(pl):	Demon protoko³u ident (RFC 1413)
Name:		authd
Version:	1.4.1
Release:	1.4
License:	GPL
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
Provides:	pidentd = 3.2
Obsoletes:	pidentd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
authd is a small and fast RFC 1413 ident protocol daemon with both
xinetd server and interactive modes that supports IPv6 and IPv4 as
well as the more popular features of pidentd.

%description -l pl
authd to ma³y i szybki protoko³u demon protoko³u ident (RFC 1413) z
trybami xinetd i interaktywnym obs³uguj±cy IPv6 i IPv4, a tak¿e
bardziej popularne mo¿liwo¶ci pidentd.

%prep
%setup -q
sed -i -e "s|/etc|%{_sysconfdir}|" config.h

%build
# TODO: optflags
%{__make} \
	prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# TODO: use rc-inetd
#install -m 644 xinetd.conf.auth $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/auth
#sed -i -e 's|/usr/local|/usr|' $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/auth

touch $RPM_BUILD_ROOT%{_sysconfdir}/ident.key

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# TODO: standard useradd sequence
#/usr/sbin/adduser -s /sbin/nologin -r ident 2>/dev/null || true
/usr/bin/openssl rand -base64 -out %{_sysconfdir}/ident.key 32
echo CHANGE THE LINE ABOVE TO A PASSPHRASE >> %{_sysconfdir}/ident.key
/bin/chown ident:ident %{_sysconfdir}/ident.key
chmod o-rw %{_sysconfdir}/ident.key

%files -f authd.lang
%defattr(644,root,root,755)
%doc COPYING README.html rfc1413.txt
#%config(noreplace) %{_sysconfdir}/xinetd.d/auth
%config %{_sysconfdir}/ident.key
%attr(755,root,root) %{_sbindir}/in.authd
