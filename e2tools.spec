Name:           e2tools
Version:        0.0.16
Release:        %mkrel 9
Summary:        Manipulate files in unmounted ext2/ext3 filesystems

Group:          System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPL
URL:            http://home.earthlink.net/~k_sheff/sw/e2tools/
Source0:        http://home.earthlink.net/~k_sheff/sw/e2tools/%{name}-%{version}.tar.lzma
Source1:        e2tools-test.sh
# Thank you very much for the man pages from Debian package.
Source2:        e2cp.1
Source3:        e2ln.1
Source4:        e2ls.1
Source5:        e2mkdir.1
Source6:        e2mv.1
Source7:        e2rm.1
Source8:        e2tail.1
Source9:        e2tools.7
Patch1:         e2tools-fedora-fixes.patch

BuildRequires:  e2fsprogs-devel >= 1.27

# For e2tools-test.sh
BuildRequires:  e2fsprogs, diffutils


%description
A simple set of utilities to read, write, and manipulate files in an
ext2/ext3 filesystem directly using the ext2fs library. This works

  - without root access
  - without the filesystem being mounted
  - without kernel ext2/ext3 support

The utilities are: e2cp e2ln e2ls e2mkdir e2mv e2rm e2tail

%prep
%setup -q
%patch1 -p1

%build
%configure
%make  CPPFLAGS="-Wall -Werror"


%check
# Run tests
for e in e2ln e2ls e2mkdir e2mv e2rm e2tail; do
    ln -s e2cp $e
done
sh %{SOURCE1}


%install
rm -rf %{buildroot}
%makeinstall_std
%{__install} -d $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} \
    %{SOURCE2} \
    %{SOURCE3} \
    %{SOURCE4} \
    %{SOURCE5} \
    %{SOURCE6} \
    %{SOURCE7} \
    %{SOURCE8} \
    $RPM_BUILD_ROOT%{_mandir}/man1/
%{__install} -D %{SOURCE9} $RPM_BUILD_ROOT%{_mandir}/man7/e2tools.7


%files
%defattr(-,root,root,-)
%doc README ChangeLog TODO AUTHORS
%{_bindir}/e2cp
%{_bindir}/e2ln
%{_bindir}/e2ls
%{_bindir}/e2mkdir
%{_bindir}/e2mv
%{_bindir}/e2rm
%{_bindir}/e2tail
%doc %{_mandir}/man1/e2cp.1*
%doc %{_mandir}/man1/e2ln.1*
%doc %{_mandir}/man1/e2ls.1*
%doc %{_mandir}/man1/e2mkdir.1*
%doc %{_mandir}/man1/e2mv.1*
%doc %{_mandir}/man1/e2rm.1*
%doc %{_mandir}/man1/e2tail.1*
%doc %{_mandir}/man7/e2tools.7*
