#!/bin/bash -eux

echo """
Installs the kernel with RT patch.
For more information see the tutorial 

https://chenna.me/blog/2020/02/23/how-to-setup-preempt-rt-on-ubuntu-18-04/
https://wiki.archlinux.org/title/Realtime_kernel_patchset
"""

# kernel version without -generic flag
KERNEL_VERSION=`uname -r | sed 's/-generic//g'`

if [[ ${KERNEL_VERSION} -ne "5.15.0-41" ]]; then
    echo "Script was written for a different kernel version"
    return
fi

mkdir kernel-${KERNEL_VERSION}-rt
cd kernel-${KERNEL_VERSION}-rt


# install dependencies
sudo apt install build-essential git libssl-dev libelf-dev flex bison

sudo apt install cpufrequtils
sudo apt install rt-tests

# testing

TEMP_DIR=$(mktemp -d -p .)
cd $TEMP_DIR

cyclictest --smp -p98 -m | tee `date -I`_test_`uname -r`.log



# download source files
curl -SLO https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.15.1.tar.xz
curl -SLO https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/5.15/patches-5.15.55-rt48.tar.xz


tar -xf linux-5.15.1.tar.xz
cd linux-5.15.1
xzcat ../patch-5.15*.patch.xz | patch -p1


exit 0

cp /boot/config-`uname -r`.config


sed -i -e 's/CONFIG_SYSTEM_TRUSTED_KEYS="debian/canonical-certs.pem"/CONFIG_SYSTEM_TRUSTED_KEYS=""/g' .config
make oldconfig
#make menuconfig

make -j8 deb-pkg

dpkg -i ..


# configure system
sudo groupadd realtime
sudo usermod -aG realtime $USER

sudo tee /etc/security/limits.d/99-realtime.conf <<EOF
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
EOF


# disable frequency scaling

sudo systemctl disable ondemand
sudo systemctl enable cpufrequtils
echo "GOVERNOR=performance"  | sudo tee /etc/default/cpufrequtils
sudo systemctl daemon-reload && sudo systemctl restart cpufrequtils

