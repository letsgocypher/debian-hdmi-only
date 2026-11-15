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

**Testing warning:** a successful build and boot-menu inspection do not prove that HDMI works on the laptop. Test the live session on HDMI first; do not install until the display, Wi-Fi, keyboard and installer are confirmed working. Carefully verify the target disk before formatting.
