# LineageOS 18.1 for Samsung Galaxy Tab A 8.0 LTE

## Device Information

- Model: Samsung Galaxy Tab A 8.0 (2017)
- Model number: SM-T385
- Codename: gta2slte
- SoC: Qualcomm Snapdragon 425
- Android version: 11
- ROM: LineageOS 18.1
- Status: Unofficial Alpha

## Working

- System boot
- Touchscreen
- Wi-Fi
- ADB
- Bluetooth audio
- Built-in speaker
- Camera
- SIM detection
- LTE registration
- Mobile data (manual APN refresh may be required)

## Known Issues

- Automatic APN initialization
- Full audio routing requires further testing
- GPS and sensors require testing
- Calls and SMS require testing
- Battery and thermal management require testing

## Source Repositories

- Device: https://github.com/Ducthinh2014123/android_device_samsung_gta2slte
- Kernel: https://github.com/Ducthinh2014123/android_kernel_samsung_msm8937
- Vendor: https://github.com/Ducthinh2014123/proprietary_vendor_samsung_gta2slte

## Build Instructions

Initialize and sync the pinned manifest:

    repo init -u https://github.com/Ducthinh2014123/android_patches_samsung_gta2slte.git -b main -m manifest.xml
    repo sync -c -j4

Clone this patch repository outside the Android source tree.

Apply the compatibility patches:

    bash /path/to/patch-repository/scripts/apply_patches.sh "$PWD"

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
