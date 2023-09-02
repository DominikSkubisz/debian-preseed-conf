#!/bin/bash

IN_ISO=$1
if [[ -z "$IN_ISO" ]]
then
  echo "You must provide ISO file"
else
  OUT_ISO="${IN_ISO/netinst/unattended}"
  echo "Extracting ISO"
  xorriso -osirrox on -indev "$IN_ISO" -extract / isofiles/
  
  echo "Modifing ISO"
  chmod +w -R isofiles/install.amd/
  gunzip isofiles/install.amd/initrd.gz
  echo preseed.cfg | cpio -H newc -o -A -F isofiles/install.amd/initrd
  gzip isofiles/install.amd/initrd
  chmod -w -R isofiles/install.amd/

  echo "Edit boot menu *.cfg files"
  chmod +w ./isofiles/isolinux/isolinux.cfg
  sudo sed -i '$d' ./isofiles/isolinux/isolinux.cfg
  chmod -w ./isofiles/isolinux/isolinux.cfg
  #vim ./isofiles/boot/grub/grub.cfg

  echo "Generate MD5 sum"
  cd isofiles/ || exit
  chmod a+w md5sum.txt
  md5sum $(find ./ -follow -type f) > md5sum.txt
  chmod a-w md5sum.txt

  echo "Create unattended ISO file"
  cd ..
  chmod a+w isofiles/isolinux/isolinux.bin
  genisoimage -r -J -b isolinux/isolinux.bin -c isolinux/boot.cat\
    -no-emul-boot -boot-load-size 4 -boot-info-table -o "$OUT_ISO" isofiles

  echo "Cleaning after install"
  sudo rm -Rf isofiles
fi
