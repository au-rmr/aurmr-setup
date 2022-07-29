#!/bin/bash -eux

echo """
Installs the kernel with RT patch.
For more information see the tutorial 

https://chenna.me/blog/2020/02/23/how-to-setup-preempt-rt-on-ubuntu-18-04/
https://wiki.archlinux.org/title/Realtime_kernel_patchset
"""

# kernel version without -generic flag
KERNEL_VERSION=`uname -r | sed 's/-generic//g'`

if [ "${KERNEL_VERSION}" != "5.15.0-41" ]; then
    echo "Script was written for a different kernel version"
    exit 1
fi

TEMP_DIR=$(mktemp -d -p . rt_patch_XXXXXXXXXX)
cd $TEMP_DIR



# install dependencies
sudo apt install build-essential git libssl-dev libelf-dev flex bison

sudo apt install cpufrequtils
sudo apt install rt-tests

# testing

sudo cyclictest --smp -p98 -m -l 10000 -q | tee `date -I`_test_`uname -r`.log

# download source files
curl -SLO  https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.15.55.tar.gz
curl -SLO https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/5.15/patch-5.15.55-rt48.patch.xz

tar -xzvf linux-5.15.55.tar.gz
cd linux-5.15.55
xzcat ../patch-5.15*.patch.xz | patch -p1


cp /boot/config-`uname -r` .config


#sed -i -e 's/CONFIG_SYSTEM_TRUSTED_KEYS="debian/canonical-certs.pem"/CONFIG_SYSTEM_TRUSTED_KEYS=""/g' .config
make oldconfig

make -j12

# https://stackoverflow.com/questions/56149191/linux-latest-stable-compilation-cannot-represent-change-to-vmlinux-gdb-py
rm vmlinux-gdb.py

make deb-pkg -j12

dpkg -i  <todo>

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



echo """reboot system and run
cyclictest --smp -p98 -m | tee `date -I`_test_`uname -r`.log
"""
