#!/usr/bin/env bash
set -euo pipefail

source_tree=${1:-"$PWD"}
patch_dir="$source_tree/device/samsung/gta2slte/patches/alpha2"
projects=(
    hardware/interfaces
    hardware/qcom-caf/msm8996/media
    prebuilts/rust
    frameworks/base
)
patches=(
    hardware-interfaces.patch
    qualcomm-media.patch
    rust-prebuilts.patch
    frameworks-base.patch
)

# Verify all four before changing any project.
pending=()
for i in "${!projects[@]}"; do
    project="$source_tree/${projects[i]}"
    patch="$patch_dir/${patches[i]}"
    if git -C "$project" apply --reverse --check "$patch" 2>/dev/null; then
        printf 'Already applied: %s\n' "${patches[i]}"
    else
        git -C "$project" apply --check "$patch"
        pending+=("$i")
    fi
done

for i in "${pending[@]}"; do
    git -C "$source_tree/${projects[i]}" apply "$patch_dir/${patches[i]}"
    printf 'Applied: %s\n' "${patches[i]}"
done
