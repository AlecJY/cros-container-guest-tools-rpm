%global hash c2d2d80

Name: cros-guest-tools		
Version: 117.15572+git.%{hash}
Release: 0
Summary: Chromium OS integration meta package

License: BSD-3-Clause
Group: System/Emulators/PC
URL: https://chromium.googlesource.com/chromiumos/containers/cros-container-guest-tools/
Source0: https://chromium.googlesource.com/chromiumos/containers/cros-container-guest-tools/+archive/%{hash}.tar.gz#/%{name}-%{hash}.tar.gz
Source100: cros-sudo-config.sysusers
Source101: cros-garcon.preset
Source102: cros-sommelier.preset
Source103: cros-vmstat-metrics.preset
Patch0: disable-auto-update.patch
Patch1: fix-paths.patch
Patch2: fix-desktop-file.patch
Patch3: crostini_metric_reporter-force-start.patch
BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: systemd
Recommends: bash-completion
Recommends: bzip2
Recommends: curl
Recommends: dbus-x11
Recommends: file
Recommends: fuse3
Recommends: git
Recommends: gnupg
Recommends: iputils
Recommends: iptables
Recommends: less
Recommends: libXss1
Recommends: man
Recommends: udev
Recommends: unzip
Recommends: usbutils
Recommends: vim
Recommends: wget
Recommends: xz
Requires: cros-garcon = %{version}-%{release}
Requires: cros-host-fonts = %{version}-%{release}
Requires: cros-notificationd = %{version}-%{release}
Requires: cros-sommelier = %{version}-%{release}
Requires: cros-ui-config = %{version}-%{release}
Recommends: cros-logging = %{version}-%{release}
Recommends: cros-sommelier-config = %{version}-%{release}
Recommends: cros-sudo-config = %{version}-%{release}
Recommends: cros-systemd-overrides = %{version}-%{release}
Recommends: cros-vmstat-metrics = %{version}-%{release}
Recommends: cros-wayland = %{version}-%{release}
Recommends: cros-pulse-config = %{version}-%{release}

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
systemctl mask auditd.service
systemctl mask display-manager.service

%postun -n cros-systemd-overrides
if [ $1 -eq 0 ] ; then
systemctl unmask systemd-journald-audit.socket
systemctl unmask auditd.service
systemctl unmask display-manager.service
fi

%package -n cros-logging
Summary: Journald config for Chromium OS integration
Requires: systemd
BuildArch: noarch

%description -n cros-logging
This package installs configuration for logging integration
with Chrome OS so e.g. filing feedback reports can collect
error logs from within the container.

%post -n cros-logging
%tmpfiles_create %{_tmpfilesdir}/cros-logging.conf

%package -n cros-adapta
Summary: Chromium OS GTK Theme
Requires: gtk2-engines
Requires: gtk2-engine-murrine
Requires: gtk2
Requires: gtk3
Requires: libqt5-qtbase-platformtheme-gtk3
Requires: libqt5-qtstyleplugins-platformtheme-gtk2
BuildArch: noarch

%description -n cros-adapta
This package provides symlinks which link the bind-mounted theme into the
correct location in the container.

%package -n cros-garcon
Summary: Chromium OS Garcon Bridge
BuildRequires: ansible
Requires: desktop-file-utils
Requires: PackageKit
Requires: xdg-utils
Requires: ansible
Requires: systemd
Requires: cros-sftp = %{version}-%{release}
BuildArch: noarch

%description -n cros-garcon
This package provides the systemd unit files for Garcon, the bridge to
Chromium OS.

%post -n cros-garcon
%systemd_user_post cros-garcon.service
# FIXME: workaround to make sure the user service symlink creation (bsc#1083473)
if [ ! -f /etc/systemd/user/default.target.wants/cros-garcon.service ]; then
  %{_bindir}/systemctl --user --global enable cros-garcon.service
fi

%preun -n cros-garcon
%systemd_user_preun cros-garcon.service

%package -n cros-host-fonts
Summary: Share fonts from Chromium OS
Requires: systemd
BuildArch: noarch

%description -n cros-host-fonts
This package provides a config file to search for the shared Chromium OS font
directory.

%post -n cros-host-fonts
%systemd_post usr-share-fonts-chromeos.mount

%preun -n cros-host-fonts
%systemd_preun usr-share-fonts-chromeos.mount

%package -n cros-notificationd
Summary: Chromium OS Notification Bridge
Requires: dbus-1
Requires: systemd
BuildArch: noarch

%description -n cros-notificationd
This package installs D-Bus on-demand service specification for notificationd.

%package -n cros-pulse-config
Summary: PulseAudio helper for Chromium OS integration
Requires: pulseaudio
Requires: pulseaudio-utils
BuildArch: noarch

%description -n cros-pulse-config
This package installs customized pulseaudio configurations to /etc/skel.
"default.pa" is required as a workaround for the lack of udev in
unprivileged containers.
"daemon.conf" contains low latency configuration.

%package -n cros-sftp
Summary: SFTP link for CrOS integration
Requires(post): openssh-server
BuildArch: noarch

%description -n cros-sftp
This package create a link of sftp-server for enabling SFTP integration with
Chromium OS.

%package -n cros-sommelier
Summary: Sommelier base package
Requires: bash
Requires: xorg-x11
Requires: vim
Requires: systemd
Recommends: xorg-x11-server
Recommends: xauth
Recommends: xorg-x11-fonts
Recommends: xkeyboard-config
BuildArch: noarch

%description -n cros-sommelier
This package installs unitfiles and support scripts for sommelier.

%post -n cros-sommelier
%systemd_user_post sommelier@0.service
%systemd_user_post sommelier@1.service
%systemd_user_post sommelier-x@0.service
%systemd_user_post sommelier-x@1.service
# FIXME: workaround to make sure the user service symlink creation (bsc#1083473)
if [ ! -f /etc/systemd/user/default.target.wants/sommelier@0.service ]; then
  %{_bindir}/systemctl --user --global enable sommelier@0.service
fi
if [ ! -f /etc/systemd/user/default.target.wants/sommelier@1.service ]; then
  %{_bindir}/systemctl --user --global enable sommelier@1.service
fi
if [ ! -f /etc/systemd/user/default.target.wants/sommelier-x@0.service ]; then
  %{_bindir}/systemctl --user --global enable sommelier-x@0.service
fi
if [ ! -f /etc/systemd/user/default.target.wants/sommelier-x@1.service ]; then
  %{_bindir}/systemctl --user --global enable sommelier-x@1.service
fi

%preun -n cros-sommelier
%systemd_user_preun sommelier@0.service
%systemd_user_preun sommelier@1.service
%systemd_user_preun sommelier-x@0.service
%systemd_user_preun sommelier-x@1.service

%package -n cros-sommelier-config
Summary: Sommelier config for Chromium OS integration
Requires: cros-sommelier
BuildArch: noarch

%description -n cros-sommelier-config
This package installs default configuration for sommelier that is ideal for
integration with Chromium OS.

%package -n cros-sudo-config
Summary: Sudo config for Chromium OS integration
BuildRequires: sudo
BuildRequires: sysuser-tools
Requires: sudo
%sysusers_requires
BuildArch: noarch

%description -n cros-sudo-config
This package installs default configuration for sudo to allow passwordless
sudo access for the sudo group, and passwordless pkexec for the sudo group.

%package -n cros-ui-config
%define branding_name cros
%define gtk2_real_package %(rpm -q --qf '%%{name}' --whatprovides gtk2)
%define gtk2_version %(rpm -q --qf '%%{version}' %{gtk2_real_package})
%define gtk3_real_package %(rpm -q --qf '%%{name}' --whatprovides gtk3)
%define gtk3_version %(rpm -q --qf '%%{version}' %{gtk3_real_package})
Summary: UI integration for Chromium OS
BuildRequires: dconf
BuildRequires: gtk2
BuildRequires: gtk3
Requires: cros-adapta = %{version}-%{release}
Requires: dconf
Requires: %{gtk2_real_package} = %{gtk2_version}
Requires: %{gtk3_real_package} = %{gtk3_version}
Requires: gtk2-metatheme-adwaita
Requires: gtk3-metatheme-adwaita
Provides: gtk2-branding = %{gtk2_version}
Provides: gtk3-branding = %{gtk3_version}
Conflicts: gtk2-branding
Conflicts: gtk3-branding
Supplements: packageand(gtk2:branding-%{branding_name})
Supplements: packageand(gtk3:branding-%{branding_name})
BuildArch: noarch

%description -n cros-ui-config
This package installs default configuration for GTK+ that is ideal for
integration with Chromium OS.

%package -n cros-vmstat-metrics
Summary: Chromium OS VMStat Metrics Reporting Daemon
Requires: systemd
BuildArch: noarch

%description -n cros-vmstat-metrics
This package installs a systemd service which monitors /proc/vmstat and
reports metrics via garcon

%post -n cros-vmstat-metrics
%systemd_user_post cros-vmstat-metrics.service
# FIXME: workaround to make sure the user service symlink creation (bsc#1083473)
if [ ! -f /etc/systemd/user/default.target.wants/cros-vmstat-metrics.service ]; then
  %{_bindir}/systemctl --user --global enable cros-vmstat-metrics.service
fi

%preun -n cros-vmstat-metrics
%systemd_user_preun cros-vmstat-metrics.service

%package -n cros-wayland
Summary: Wayland extras for virtwl in Chromium OS
BuildArch: noarch

%description -n cros-wayland
This package provides config files and udev rules to improve the Wayland
experience under CrOS.

%package -n cros-xdg-desktop-portal
Summary: ChromeOS FileChooser backend for xdg-desktop-portal
Requires: xdg-desktop-portal
BuildArch: noarch

%description -n cros-xdg-desktop-portal
cros-xdg-desktop-portal provides a ChromeOS system FileChooser implementation
for the xdg-desktop-portal service. This allows linux apps to use the system
FileChooser. This implementation is currently experimental.

%prep
%setup -q -c

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%sysusers_generate_pre %{SOURCE100} sudo cros-sudo-config.conf

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d
mkdir -p %{buildroot}%{_sysconfdir}/gtk-2.0
mkdir -p %{buildroot}%{_sysconfdir}/gtk-3.0
mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
mkdir -p %{buildroot}%{_sysconfdir}/xdg
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{_sysconfdir}/skel/.config/pulse
mkdir -p %{buildroot}%{_sysusersdir}
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datarootdir}/ansible/plugins/callback
mkdir -p %{buildroot}%{_datarootdir}/applications
mkdir -p %{buildroot}%{_datarootdir}/dbus-1/services
mkdir -p %{buildroot}%{_datarootdir}/themes
mkdir -p %{buildroot}%{_datarootdir}/xdg-desktop-portal/portals
mkdir -p %{buildroot}%{_userunitdir}/sommelier@0.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier@1.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier-x@0.service.d
mkdir -p %{buildroot}%{_userunitdir}/sommelier-x@1.service.d
mkdir -p %{buildroot}%{_userunitdir}/pulseaudio.service.wants
mkdir -p %{buildroot}%{_userunitdir}/default.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
mkdir -p %{buildroot}%{_sysconfdir}/fonts/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/systemd/user/default.target.wants
mkdir -p %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/10-vendor.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset
mkdir -p %{buildroot}/usr/lib/openssh

export NO_BRP_STALE_LINK_ERROR=yes
ln -sf /opt/google/cros-containers/bin/sommelier %{buildroot}%{_bindir}/sommelier
ln -sf /opt/google/cros-containers/cros-adapta %{buildroot}%{_datarootdir}/themes/CrosAdapta
ln -sf /usr/lib/ssh/sftp-server %{buildroot}/usr/lib/openssh/sftp-server

install -m 644 %{SOURCE100} %{buildroot}%{_sysusersdir}/cros-sudo-config.conf
install -m 644 %{SOURCE101} %{buildroot}%{_prefix}/lib/systemd/user-preset/80-cros-garcon.preset
install -m 644 %{SOURCE102} %{buildroot}%{_prefix}/lib/systemd/user-preset/80-cros-sommelier.preset
install -m 644 %{SOURCE103} %{buildroot}%{_prefix}/lib/systemd/user-preset/80-cros-vmstat-metrics.preset

install -m 644 cros-garcon/third_party/garcon.py %{buildroot}%{_datarootdir}/ansible/plugins/callback/garcon.py
install -m 440 cros-sudo-config/10-cros-nopasswd %{buildroot}%{_sysconfdir}/sudoers.d/10-cros-nopasswd
install -m 440 cros-sudo-config/10-cros-nopasswd.pkla %{buildroot}%{_sharedstatedir}/polkit-1/localauthority/10-vendor.d/10-cros-nopasswd.pkla
install -m 644 cros-sommelier/sommelierrc  %{buildroot}%{_sysconfdir}/sommelierrc
install -m 644 cros-sommelier/sommelier.sh %{buildroot}%{_sysconfdir}/profile.d/sommelier.sh
install -m 644 cros-sommelier/skel.sommelierrc %{buildroot}%{_sysconfdir}/skel/.sommelierrc
install -m 644 cros-garcon/skel.cros-garcon.conf %{buildroot}%{_sysconfdir}/skel/.config/cros-garcon.conf
install -m 644 cros-wayland/skel.weston.ini %{buildroot}%{_sysconfdir}/skel/.config/weston.ini
install -m 644 cros-wayland/10-cros-virtwl.rules %{buildroot}%{_udevrulesdir}/10-cros-virtwl.rules
install -m 644 cros-pulse-config/default.pa %{buildroot}%{_sysconfdir}/skel/.config/pulse/default.pa
install -m 644 cros-pulse-config/daemon.conf %{buildroot}%{_sysconfdir}/skel/.config/pulse/daemon.conf
install -m 755 cros-garcon/garcon-terminal-handler %{buildroot}%{_bindir}/garcon-terminal-handler
install -m 755 cros-garcon/garcon-url-handler %{buildroot}%{_bindir}/garcon-url-handler
install -m 644 cros-notificationd/org.freedesktop.Notifications.service %{buildroot}%{_datarootdir}/dbus-1/services/org.freedesktop.Notifications.service
install -m 644 cros-ui-config/gtkrc %{buildroot}%{_sysconfdir}/gtk-2.0/gtkrc
install -m 644 cros-ui-config/settings.ini %{buildroot}%{_sysconfdir}/gtk-3.0/settings.ini
install -m 644 cros-ui-config/Trolltech.conf %{buildroot}%{_sysconfdir}/xdg/Trolltech.conf
install -m 644 cros-ui-config/01-cros-ui %{buildroot}%{_sysconfdir}/dconf/db/local.d/01-cros-ui

install -m 644 cros-host-fonts/usr-share-fonts-chromeos.mount %{buildroot}%{_unitdir}/usr-share-fonts-chromeos.mount
install -m 644 cros-garcon/cros-garcon.service %{buildroot}%{_userunitdir}/cros-garcon.service
install -m 644 cros-sommelier/sommelier@.service %{buildroot}%{_userunitdir}/sommelier@.service
install -m 644 cros-sommelier/sommelier-x@.service %{buildroot}%{_userunitdir}/sommelier-x@.service
install -m 644 cros-vmstat-metrics/cros-vmstat-metrics.service %{buildroot}%{_userunitdir}/cros-vmstat-metrics.service
install -m 644 cros-sommelier-config/cros-sommelier-override.conf %{buildroot}%{_userunitdir}/sommelier@0.service.d/cros-sommelier-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-x-override.conf %{buildroot}%{_userunitdir}/sommelier-x@0.service.d/cros-sommelier-x-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-low-density-override.conf %{buildroot}%{_userunitdir}/sommelier@1.service.d/cros-sommelier-low-density-override.conf
install -m 644 cros-sommelier-config/cros-sommelier-low-density-override.conf %{buildroot}%{_userunitdir}/sommelier-x@1.service.d/cros-sommelier-low-density-override.conf
install -m 644 cros-notificationd/cros-notificationd.service %{buildroot}%{_userunitdir}/cros-notificationd.service
install -m 644 cros-logging/00-create-logs-dir.conf %{buildroot}%{_tmpfilesdir}/cros-logging.conf
install -m 644 cros-xdg-desktop-portal/cros.portal %{buildroot}%{_datarootdir}/xdg-desktop-portal/portals/cros.portal
desktop-file-install --dir=%{buildroot}%{_datadir}/applications cros-garcon/garcon_host_browser.desktop

%pre -n cros-sudo-config -f sudo.pre

%files
%dir %{_sysconfdir}/skel/.config
%license LICENSE
%doc README.md

%files -n cros-adapta
%{_datarootdir}/themes/CrosAdapta
%license LICENSE
%doc README.md

%files -n cros-logging
%license LICENSE
%doc README.md
%{_tmpfilesdir}/cros-logging.conf
%attr(0755,root,root) %dir %ghost %{_localstatedir}/log/journal

%files -n cros-garcon
%dir %{_sysconfdir}/systemd/user/default.target.wants
%{_bindir}/garcon-terminal-handler
%{_bindir}/garcon-url-handler
%{_datarootdir}/ansible/plugins/callback/garcon.py
%{_datarootdir}/applications/garcon_host_browser.desktop
%{_userunitdir}/cros-garcon.service
%{_prefix}/lib/systemd/user-preset/80-cros-garcon.preset
%config %{_sysconfdir}/skel/.config/cros-garcon.conf
%license LICENSE
%doc README.md

%files -n cros-host-fonts
%{_unitdir}/usr-share-fonts-chromeos.mount
%license LICENSE
%doc README.md

%files -n cros-notificationd
%{_datarootdir}/dbus-1/services/org.freedesktop.Notifications.service
%{_userunitdir}/cros-notificationd.service
%license LICENSE
%doc README.md

%files -n cros-sudo-config
%dir %{_sharedstatedir}/polkit-1
%dir %{_sharedstatedir}/polkit-1/localauthority
%dir %{_sharedstatedir}/polkit-1/localauthority/10-vendor.d
%{_sharedstatedir}/polkit-1/localauthority/10-vendor.d/10-cros-nopasswd.pkla
%{_sysusersdir}/cros-sudo-config.conf
%config(noreplace) %{_sysconfdir}/sudoers.d/10-cros-nopasswd
%license LICENSE
%doc README.md

%files -n cros-systemd-overrides
%license LICENSE
%doc README.md

%files -n cros-pulse-config
%dir %{_sysconfdir}/skel/.config/pulse
%config %{_sysconfdir}/skel/.config/pulse/daemon.conf
%config %{_sysconfdir}/skel/.config/pulse/default.pa
%license LICENSE
%doc README.md

%files -n cros-sftp
%dir /usr/lib/openssh
/usr/lib/openssh/sftp-server
%license LICENSE
%doc README.md

%files -n cros-sommelier
%dir %{_sysconfdir}/systemd/user/default.target.wants
%{_bindir}/sommelier
%config %{_sysconfdir}/skel/.sommelierrc
%config(noreplace) %{_sysconfdir}/sommelierrc
%config(noreplace) %{_sysconfdir}/profile.d/sommelier.sh
%{_userunitdir}/sommelier@.service
%{_userunitdir}/sommelier-x@.service
%{_prefix}/lib/systemd/user-preset/80-cros-sommelier.preset
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
%dir %{_sysconfdir}/dconf/db/local.d
%config(noreplace) %{_sysconfdir}/gtk-2.0/gtkrc
%{_sysconfdir}/gtk-3.0
%config(noreplace) %{_sysconfdir}/gtk-3.0/settings.ini
%config(noreplace) %{_sysconfdir}/xdg/Trolltech.conf
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/01-cros-ui
%license LICENSE
%doc README.md

%files -n cros-vmstat-metrics
%dir %{_sysconfdir}/systemd/user/default.target.wants
%{_userunitdir}/cros-vmstat-metrics.service
%{_prefix}/lib/systemd/user-preset/80-cros-vmstat-metrics.preset
%license LICENSE
%doc README.md

%files -n cros-wayland
%config(noreplace) %{_sysconfdir}/skel/.config/weston.ini
%{_udevrulesdir}/10-cros-virtwl.rules
%license LICENSE
%doc README.md

%files -n cros-xdg-desktop-portal
%dir %{_datarootdir}/xdg-desktop-portal/
%dir %{_datarootdir}/xdg-desktop-portal/portals
%{_datarootdir}/xdg-desktop-portal/portals/cros.portal
%license LICENSE
%doc README.md

%changelog
* Sat Aug 12 2023 Alec Su ae40515@yahoo.com.tw - 117.15572+git.c2d2d80-0
- Update to release-R117-15572.B c2d2d80
- Support OpenSUSE
- Add cros-vmstat-metrics package 
- Add cros-xdg-desktop-portal package

* Thu Aug 06 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.39.20200806git19eab9e
- Fix changelog error

* Thu Aug 06 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.38.20200806git19eab9e
- Update to master 19eab9e

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.37.20200716git74ea274
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.36.20200716git74ea274
- Update to master 74ea274

* Thu Jun 11 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.35.20200611git5ab8724
- Update to master 5ab8724

* Mon Jun 08 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.34.20200608git0767a9f
- Update to master 0767a9f
- Removes cros-pulse-config service. Adds /etc/skel/.config/pulse config files

* Sun May 24 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.33.20200524gitc91e2b4
- Update to master c91e2b4
- Add xdg-utils to the recommended packages

* Sat May 09 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.32.20200509gitfce526e
- Update to master fce526e

* Mon Apr 27 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.31.20200427git6968d7b
- Update to master 6968d7b

* Fri Mar 13 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.30.20200330git61d9c12
- Update to master 61d9c12

* Fri Mar 13 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.29.20200313git1d204a4
- Update to master 1d204a4

* Wed Mar 04 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.28.20200304gitd2e19d8
- Update to master d2e19d8

* Wed Feb 19 2020 Jason Montleon jmontleo@redhat.com - 1.0-0.27.20200219git28f04a1
- Update to master 28f04a1

* Mon Feb 03 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.26.20200203git41d4d31
- Update to master 41d4d31

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.25.20200115git88d1189
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Jason Montleon jmontleo@redhat.com 1.0-0.24.20200115git88d1189
- Update to master 88d1189

* Tue Dec 17 2019 Jason Montleon jmontleo@redhat.com 1.0-0.23.20191217gitce9fd9f
- Update to master ce9fd9f

* Mon Dec 02 2019 Jason Montleon jmontleo@redhat.com 1.0-0.22.20191105git526b9cd
- Update to master 526b9cd

* Tue Nov 05 2019 Jason Montleon jmontleo@redhat.com 1.0-0.21.20191105git37b5c2c
- Update to master 37b5c2c

* Sat Nov 02 2019 Jason Montleon jmontleo@redhat.com 1.0-0.20.20191102gite218618
- Update to master e218618

* Fri Oct 18 2019 Jason Montleon jmontleo@redhat.com 1.0-0.19.20191015gita93ea04
- Add recommends for mesa-dri-drivers

* Tue Oct 15 2019 Jason Montleon jmontleo@redhat.com 1.0-0.18.20191015gita93ea04
- Update to upstream master
- Removed cros-adapta theme for CentOS 8 due to missing dependencies

* Fri Sep 13 2019 Jason Montleon jmontleo@redhat.com 1.0.0.17.20190913git939ae3e
- Update to master 939ae3e
- Add missing cros-sudo-config

* Thu Aug 15 2019 Jason Montleon jmontleo@redhat.com 1.0.0.16.20190815git4e1b573
- Update to master 4e1b573

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.15.20190703gita30bd3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Jason Montleon jmontleo@redhat.com 1.0-0.14.20190703gita30bd3e
- Removed cros-gpu and workaround services.
- Added an Environment setting to sommelier-x service to get it working instead

* Sun Jul 07 2019 Jason Montleon jmontleo@redhat.com 1.0-0.13.20190703gita30bd3e
- Added cros-gpu package with service to work around 3d acceleration issues.

* Wed Jul 03 2019 Jason Montleon jmontleo@redhat.com 1.0-0.12.20190703gita30bd3e
- Updated to master a30bd3e
- Removed tsched=0 fix. This is now default upstream

* Tue May 07 2019 Jason Montleon jmontleo@redhat.com 1.0-0.11.20190324git8f20e06
- Update cros-pulse-config to load with tsched=0 to fix sound skipping

* Wed Apr 24 2019 Jason Montleon jmontleo@redhat.com 1.0-0.10.20190324git8f20e06
- Update to 8f20e06

* Fri Mar 29 2019 Jason Montleon jmontleo@redhat.com 1.0-0.9.20190214git4dc99dd
- make cros-sftp a system service
- add missing dependencies
- fix distro specific sommelier-x issues

* Tue Feb 26 2019 Jason Montleon jmontleo@redhat.com 1.0-0.8.20190214git4dc99dd
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
