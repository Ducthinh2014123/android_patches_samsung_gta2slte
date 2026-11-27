# LineageOS 18.1 for Samsung Galaxy Tab A 8.0 LTE

## Device Information

- Model: Samsung Galaxy Tab A 8.0 (2017)
- Model number: SM-T385
- Codename: gta2slte
- SoC: Qualcomm Snapdragon 425
- Android version: 11
- ROM: LineageOS 18.1
- Status: Unofficial Alpha 2

## Working

- System boot
- Touchscreen
- Wi-Fi
- ADB
- Bluetooth audio
- Built-in speaker
- Camera
- Auto rotation (K2HH accelerometer)
- Hardware H.264 playback (tested at 720p and 1080p)
- SELinux Enforcing
- SIM detection
- LTE registration
- Mobile data (manual APN refresh may be required)

## Known Issues

- Automatic APN initialization
- Full audio routing requires further testing
- GPS and non-accelerometer sensors require testing
- Windows 11 MTP transfers need verification ([issue #1](https://github.com/Ducthinh2014123/android_patches_samsung_gta2slte/issues/1))
- Calls and SMS require testing
- Battery and thermal management require testing

## Alpha 2 (2026-11-27)

- Switched the kernel to the standard AOSP MTP driver.
- Enabled 512 MiB of zRAM and fixed repeated starts from a duplicate Bluetooth service.
- Added Rust device shims, CPU post-boot setup and the Game Mode memory policy and banner.

Download the ROM and matching Lineage Recovery from the
[Releases page](https://github.com/Ducthinh2014123/android_patches_samsung_gta2slte/releases).

## Source Repositories

- Device: https://github.com/Ducthinh2014123/android_device_samsung_gta2slte
- Kernel: https://github.com/Ducthinh2014123/android_kernel_samsung_msm8937
- Vendor: https://github.com/Ducthinh2014123/proprietary_vendor_samsung_gta2slte

## Build Instructions

Initialize and sync the pinned manifest:

    repo init -u https://github.com/Ducthinh2014123/android_patches_samsung_gta2slte.git -b main -m manifest.xml
    repo sync -c -j4

Clone this repository outside the Android source tree and run its script from
the root of the synced Android tree:

    bash /path/to/patch-repository/scripts/apply_patches.sh "$PWD"

The manifest already pins the updated kernel and vendor tree. The script applies
the four remaining patches from the device tree. See the
[Alpha 2 build inputs](https://github.com/Ducthinh2014123/android_device_samsung_gta2slte/blob/5844f9d75a72502f1cf75bdb94d5d89a5abd51f5/patches/alpha2/README.md)
for their base revisions.

Build LineageOS:

    source build/envsetup.sh
    lunch lineage_gta2slte-userdebug
    mka bacon -j4

## Binder ABI Patch

The scripts directory contains a compatibility patch
for the legacy Samsung peripheral client library.

The pinned vendor revision already contains the patched
binary. Do not apply the binary patch twice.

## Disclaimer

This is an experimental unofficial build.
Back up your data before installation.
Only install on the supported SM-T385 model.

## Credits

- LineageOS Team
- Android Open Source Project
- Samsung
- Qualcomm
- Original device tree and kernel contributors
- Community developers and testers

Proprietary binaries remain subject to their respective
owners' licenses and redistribution terms.
