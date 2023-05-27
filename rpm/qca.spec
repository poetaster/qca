Name:           qca
Summary:        QCA provides a straightforward and cross-platform crypto API
Version:        2.3.4
Release:        1
License:        Lesser GNU General Public License
URL:            https://github.com/KDE/qca
Source0:        %{name}-%{version}.tar.xz
#Patch0:         001-version.patch

Requires:  ca-certificates
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  cmake
BuildRequires:  ca-certificates

%description
The Qt Cryptographic Architecture (QCA) provides a straightforward and cross-
platform API for a range of cryptographic features, including SSL/TLS,
X.509 certificates, SASL, OpenPGP, S/MIME CMS, and smart cards.

%package devel
Summary:    Development package of %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-devel

%description devel
Contains files needed to development with %{name}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
touch .git                           
mkdir -p build                       
pushd build                 

%cmake .. \
  -D QCA_INSTALL_IN_QT_PREFIX=OFF \
  -D LIB_INSTALL_DIR=%{_libdir} \
  -D BUILD_PLUGINS=AUTO \
  -D BUILD_TESTS=OFF 

%make_build 
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc README TODO
%license COPYING
%{_bindir}/qcatool-qt5
%{_bindir}/mozcerts-qt5
%{_libdir}/libqca-qt5.so
%{_libdir}/libqca-qt5.so.*
%{_libdir}/qca-qt5/crypto/libqca-*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/cmake/*/*
%{_libdir}/pkgconfig/qca2-qt5.pc
%{_includedir}/Qca-qt5/QtCrypto/*
%{_usr}/mkspecs/features/crypto.prf
%{_mandir}/man1/*

