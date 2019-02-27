%global hash 4dc99dd
%global snapshotdate 20190214

Name: cros-guest-tools		
Version: 1.0
Release: 0.8.%{snapshotdate}git%{hash}%{?dist}
Summary: Chromium OS integration meta package

License: BSD	
URL: https://chromium.googlesource.com/chromiumos/containers/cros-container-guest-tools/
Source0: https://chromium.googlesource.com/chromiumos/containers/cros-container-guest-tools/+archive/%{hash}.tar.gz#/%{name}-%{hash}.tar.gz

BuildArch: noarch
BuildRequires: systemd
Requires: cros-adapta = %{version}-%{release}
Requires: cros-garcon = %{version}-%{release}
Requires: cros-notificationd = %{version}-%{release}
Requires: cros-pulse-config = %{version}-%{release}
Requires: cros-sftp = %{version}-%{release}
Requires: cros-sommelier = %{version}-%{release}
Requires: cros-sommelier-config = %{version}-%{release}
Requires: cros-systemd-overrides = %{version}-%{release}
Requires: cros-ui-config = %{version}-%{release}
Requires: cros-wayland = %{version}-%{release}

%description
This package has dependencies on all other packages necessary for Chromium OS
integration.

%package -n cros-systemd-overrides
Summary: Systemd overrides for running under Chromium OS
Requires(post): systemd
Requires(postun): systemd
BuildArch: noarch

%description -n cros-systemd-overrides
This package overrides the default behavior of some core systemd units.

%post -n cros-systemd-overrides
systemctl mask systemd-journald-audit.socket

%postun -n cros-systemd-overrides
if [ $1 -eq 0 ] ; then
systemctl unmask systemd-journald-audit.socket
fi

%package -n cros-adapta
Summary: Chromium OS GTK Theme
Requires: filesystem
Requires: gtk2
Requires: gtk3
Requires: gtk-murrine-engine
Requires: gtk2-engines
Requires: qt5-qtstyleplugins
BuildArch: noarch

%description -n cros-adapta
This package provides symlinks which link the bind-mounted theme into the
correct location in the container.

%package -n cros-garcon
Summary: Chromium OS Garcon Bridge
BuildRequires: desktop-file-utils
Requires: systemd
BuildArch: noarch

%description -n cros-garcon
This package provides the systemd unit files for Garcon, the bridge to
Chromium OS.

%post -n cros-garcon
%systemd_user_post cros-garcon.service

%preun -n cros-garcon
%systemd_user_preun cros-garcon.service

%package -n cros-notificationd
Summary: Chromium OS Notification Bridge
Requires: dbus-common
BuildArch: noarch

%description -n cros-notificationd
This package installs D-Bus on-demand service specification for notificationd.

%package -n cros-pulse-config
Summary: This package installs a helper systemd unit for PulseAudio support
Requires: alsa-plugins-pulseaudio
Requires: pulseaudio-utils
BuildArch: noarch

%description -n cros-pulse-config
This package installs a helper systemd unit for PulseAudio support.
This is required as a workaround for the lack of udev in unprivileged
containers.

%post -n cros-pulse-config
%systemd_user_post cros-pulse-config.service

%preun -n cros-pulse-config
%systemd_user_preun cros-pulse-config.service

%package -n cros-sftp
Summary: SFTP service files for CrOS integration
Requires(post): openssh-server
BuildArch: noarch

%description -n cros-sftp
This package installs unit-files and support scripts for enabling SFTP
integration with Chromium OS.

%post -n cros-sftp
%systemd_user_post cros-sftp.service

%preun -n cros-sftp
%systemd_user_preun cros-sftp.service

%package -n cros-sommelier
Summary: This package installs unit-files and support scripts for sommelier
Requires: xorg-x11-xauth
BuildArch: noarch

%description -n cros-sommelier
%{summary}

%post -n cros-sommelier
%systemd_user_post sommelier@.service
%systemd_user_post sommelier-x@.service

%preun -n cros-sommelier
%systemd_user_preun sommelier@.service
%systemd_user_preun sommelier-x@.service

%package -n cros-sommelier-config
Summary: Sommelier config for Chromium OS integration
Requires: cros-sommelier
BuildArch: noarch

%description -n cros-sommelier-config
This package installs default configuration for sommelier that is ideal for
integration with Chromium OS.

%package -n cros-ui-config
Summary: UI integration for Chromium OS
Requires: dconf
Requires: gtk2
Requires: gtk3
BuildArch: noarch

%description -n cros-ui-config
This package installs default configuration for GTK+ that is ideal for
integration with Chromium OS.

%package -n cros-wayland
Summary: Wayland extras for virtwl in Chromium OS
Requires: systemd-udev
BuildArch: noarch

%description -n cros-wayland
This package provides config files and udev rules to improve the Wayland
experience under CrOS.

%prep
%setup -q -c

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d
mkdir -p %{buildroot}%{_sysconfdir}/gtk-2.0
mkdir -p %{buildroot}%{_sysconfdir}/gtk-3.0
mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
mkdir -p %{buildroot}%{_sysconfdir}/xdg
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{_sysconfdir}/skel/.config
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datarootdir}/applications
mkdir -p %{buildroot}%{_datarootdir}/dbus-1/services
mkdir -p %{buildroot}%{_datarootdir}/themes
mkdir -p %{buildroot}%{_userunitdir}/cros-garcon.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier@0.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier@1.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier-x@0.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier-x@1.service.d

ln -sf /opt/google/cros-containers/bin/sommelier %{buildroot}%{_bindir}/sommelier
ln -sf /opt/google/cros-containers/cros-adapta %{buildroot}%{_datarootdir}/themes/CrosAdapta

install -m 644 cros-sommelier/sommelierrc  %{buildroot}%{_sysconfdir}/sommelierrc
install -m 755 cros-sommelier/sommelier.sh %{buildroot}%{_sysconfdir}/profile.d/sommelier.sh
install -m 644 cros-garcon/skel.cros-garcon.conf %{buildroot}%{_sysconfdir}/skel/.config/cros-garcon.conf
install -m 644 cros-wayland/skel.weston.ini %{buildroot}%{_sysconfdir}/skel/.config/weston.ini
install -m 644 cros-wayland/10-cros-virtwl.rules %{buildroot}%{_udevrulesdir}/10-cros-virtwl.rules
install -m 755 cros-garcon/garcon-terminal-handler %{buildroot}%{_bindir}/garcon-terminal-handler
install -m 755 cros-garcon/garcon-url-handler %{buildroot}%{_bindir}/garcon-url-handler
install -m 644 cros-notificationd/org.freedesktop.Notifications.service %{buildroot}%{_datarootdir}/dbus-1/services/org.freedesktop.Notifications.service
install -m 644 cros-ui-config/gtkrc %{buildroot}%{_sysconfdir}/gtk-2.0/gtkrc
install -m 644 cros-ui-config/settings.ini %{buildroot}%{_sysconfdir}/gtk-3.0/settings.ini
install -m 644 cros-ui-config/Trolltech.conf %{buildroot}%{_sysconfdir}/xdg/Trolltech.conf
install -m 644 cros-ui-config/01-cros-ui %{buildroot}%{_sysconfdir}/dconf/db/local.d/01-cros-ui

install -m 644 cros-garcon/cros-garcon.service %{buildroot}%{_userunitdir}/cros-garcon.service
install -m 644 cros-pulse-config/cros-pulse-config.service %{buildroot}%{_userunitdir}/cros-pulse-config.service
install -m 644 cros-sommelier/sommelier@.service %{buildroot}%{_userunitdir}/sommelier@.service
install -m 644 cros-sommelier/sommelier-x@.service %{buildroot}%{_userunitdir}/sommelier-x@.service
install -m 644 cros-sftp/cros-sftp.service %{buildroot}%{_userunitdir}/cros-sftp.service

install -m 644 cros-garcon/cros-garcon-override.conf %{buildroot}%{_userunitdir}/cros-garcon.service.d/cros-garcon-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-override.conf %{buildroot}%{_userunitdir}/sommelier@0.service.d/cros-sommelier-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-x-override.conf %{buildroot}%{_userunitdir}/sommelier-x@0.service.d/cros-sommelier-x-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-low-density-override.conf %{buildroot}%{_userunitdir}/sommelier@1.service.d/cros-sommelier-low-density-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-low-density-override.conf %{buildroot}%{_userunitdir}/sommelier-x@1.service.d/cros-sommelier-low-density-override.conf

sed -i 's/OnlyShowIn=Never/OnlyShowIn=X-Never/g' cros-garcon/garcon_host_browser.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications cros-garcon/garcon_host_browser.desktop

sed -i '/x-auth=\${HOME}\/.Xauthority/d' %{buildroot}%{_userunitdir}/sommelier-x@.service
sed -i 's/false/true/g' %{buildroot}%{_sysconfdir}/skel/.config/cros-garcon.conf
sed -i '1i if [ "$UID" -ne "0" ]; then' %{buildroot}%{_sysconfdir}/profile.d/sommelier.sh
sed -i '1i export XDG_RUNTIME_DIR=/run/user/$UID' %{buildroot}%{_sysconfdir}/profile.d/sommelier.sh
echo "fi" >> %{buildroot}%{_sysconfdir}/profile.d/sommelier.sh

%files
%dir %{_sysconfdir}/skel/.config
%license LICENSE
%doc README.md

%files -n cros-adapta
%{_datarootdir}/themes/CrosAdapta
%license LICENSE
%doc README.md

%files -n cros-garcon
%{_bindir}/garcon-terminal-handler
%{_bindir}/garcon-url-handler
%{_datarootdir}/applications/garcon_host_browser.desktop
%config(noreplace) %{_sysconfdir}/skel/.config/cros-garcon.conf
%{_userunitdir}/cros-garcon.service
%{_userunitdir}/cros-garcon.service.d
%license LICENSE
%doc README.md

%files -n cros-notificationd
%{_datarootdir}/dbus-1/services/org.freedesktop.Notifications.service
%license LICENSE
%doc README.md

%files -n cros-systemd-overrides
%license LICENSE
%doc README.md

%files -n cros-pulse-config
%{_userunitdir}/cros-pulse-config.service
%license LICENSE
%doc README.md

%files -n cros-sftp
%{_userunitdir}/cros-sftp.service
%license LICENSE
%doc README.md

%files -n cros-sommelier
%{_bindir}/sommelier
%config(noreplace) %{_sysconfdir}/sommelierrc
%config(noreplace) %{_sysconfdir}/profile.d/sommelier.sh
%{_userunitdir}/sommelier@.service
%{_userunitdir}/sommelier-x@.service
%license LICENSE
%doc README.md

%files -n cros-sommelier-config
%{_userunitdir}/sommelier@0.service.d
%{_userunitdir}/sommelier@1.service.d
%{_userunitdir}/sommelier-x@0.service.d
%{_userunitdir}/sommelier-x@1.service.d
%license LICENSE
%doc README.md

%files -n cros-ui-config
%config(noreplace) %{_sysconfdir}/gtk-2.0/gtkrc
%{_sysconfdir}/gtk-3.0
%config(noreplace) %{_sysconfdir}/gtk-3.0/settings.ini
%config(noreplace) %{_sysconfdir}/xdg/Trolltech.conf
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/01-cros-ui
%license LICENSE
%doc README.md

%files -n cros-wayland
%config(noreplace) %{_sysconfdir}/skel/.config/weston.ini
%{_udevrulesdir}/10-cros-virtwl.rules
%license LICENSE
%doc README.md

%changelog
* Thu Feb 26 2019 Jason Montleon jmontleo@redhat.com 1.0-0.8.20190214git4dc99dd
- Update to master 4dc99dd

* Thu Feb 21 2019 Jason Montleon jmontleo@redhat.com 1.0-0.7.20190213gitbf01129
- Stop upgrade from unmasking systemd-journald-audit.socket

* Sun Feb 17 2019 Jason Montleon jmontleo@redhat.com 1.0-0.6.20190213gitbf01129
- Limit script to running as user

* Sun Feb 17 2019 Jason Montleon jmontleo@redhat.com 1.0-0.5.20190213gitbf01129
- Clean up rpmlint warnings

* Sun Feb 17 2019 Jason Montleon jmontleo@redhat.com 1.0-0.4.20190213gitbf01129
- Packaging corrections

* Wed Feb 13 2019 Jason Montleon jmontleo@redhat.com 1.0-3.bf01129
- Remove garcon files no relevant to Fedora
- export XDG_RUNTIME_DIR at beginning of script

* Wed Feb 13 2019 Jason Montleon jmontleo@redhat.com 1.0-2.bf01129
- Add missing pulseaudio-utils dep
- Change dist tag

* Wed Feb 13 2019 Jason Montleon jmontleo@redhat.com 1.0-bf01129.1
- Initial package
