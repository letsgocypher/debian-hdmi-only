# Debian 13 KDE HDMI-only ISO

Builds an amd64 Debian 13 (Trixie) KDE Plasma live ISO with Intel i915 modesetting and HDMI-focused kernel parameters.

## Build the ISO

1. Open **Actions**.
2. Select **Build Debian HDMI KDE ISO**.
3. Press **Run workflow** on the main branch.
4. Wait for the build to finish.
5. Download the `debian-hdmi-kde-iso` artifact from the run's Artifacts section.

The artifact contains the ISO and SHA256 checksum.

## Graphics configuration

The live kernel is started with:

```
i915.modeset=1 video=eDP-1:d video=HDMI-A-1:e
```

The installed system receives the same parameters through `/etc/default/grub.d/99-hdmi-only.cfg`. i915 is included in initramfs modules, and Intel graphics firmware/microcode are included.

**Connector names are provisional.** `eDP-1` and `HDMI-A-1` are common Intel DRM names, but must be verified on this laptop. A wrong HDMI connector name may prevent the forced-enable parameter from having the intended effect.

## Important boot limitation

This only configures Linux after the kernel starts. It cannot change Lenovo BIOS/UEFI video output or choose USB boot. If the firmware boot menu is invisible, the USB must be selected by a separate method (for example, the NOVO button or USB-first boot order).

Do not install until the live desktop is visible on the external HDMI display. Carefully verify the target disk in the installer before formatting.

## Debloated KDE Plasma edition

A separate **Build Debian HDMI KDE Minimal ISO** workflow builds a lighter KDE Plasma edition for older laptops. It keeps Plasma as the desktop environment but avoids the full `task-kde-desktop` package bundle and disables APT recommended packages.

The selected desktop includes Plasma, the X11 window manager/session, SDDM, Dolphin, Konsole, System Settings, NetworkManager integration, audio controls, and essential device/power services. It keeps Calamares, Intel graphics firmware/microcode, Wi-Fi support, and the HDMI boot configuration. It deliberately leaves out a preinstalled browser, office suite, games, and large optional KDE applications.

To build it, open **Actions** → **Build Debian HDMI KDE Minimal ISO** → **Run workflow**. Download the `debian-hdmi-kde-plasma-minimal-iso` artifact. This is separate from the existing standard KDE build.

This reduces the default software selection and avoids optional background components; it does not strip essential Plasma services or promise a specific RAM footprint. Actual performance depends on hardware and the applications running.
