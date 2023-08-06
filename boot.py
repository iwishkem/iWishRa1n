#!/usr/bin/env python3
#
#  Copyright (C) 2019-2023 checkra1n team
#  This file is part of pongoOS.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
import sys
import time
import usb.core
import struct

kpf = open("payloads/checkra1n-kpf-ploosh.bin", "rb").read()
rdsk = open("payloads/ramdisk.bin", "rb").read()
overlay = open("payloads/overlay.bin", "rb").read()
dev = usb.core.find(idVendor=0x05ac, idProduct=0x4141)
if dev is None:
    raise ValueError('Cihaz Bulunamadı')
dev.set_configuration()

#fuse lock / sep auto
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "fuse lock\n")
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "sep auto\n")

#Send kpf / modload
dev.ctrl_transfer(0x21, 2, 0, 0, 0)
dev.ctrl_transfer(0x21, 1, 0, 0, struct.pack('I', len(kpf)))
dev.write(2,kpf,1000000)
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "modload\n")

#kpf_flags 0x1 / checkra1n_flags 0x0 / palera1n_flags 0x0
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "kpf_flags 0x1\n")
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "checkra1n_flags 0x0\n")
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "palera1n_flags 0x0\n")

#Send ramdisk / ramdisk
dev.ctrl_transfer(0x21, 2, 0, 0, 0)
dev.ctrl_transfer(0x21, 1, 0, 0, struct.pack('I', len(rdsk)))
dev.write(2,rdsk,1000000)
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "ramdisk\n")

#Send overlay / overlay
dev.ctrl_transfer(0x21, 2, 0, 0, 0)
dev.ctrl_transfer(0x21, 1, 0, 0, struct.pack('I', len(overlay)))
dev.write(2,overlay,1000000)
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "overlay\n")

#xargs  rootdev=md0 / bootx
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "xargs  rootdev=md0\n")
dev.ctrl_transfer(0x21, 4, 0, 0, 0)
dev.ctrl_transfer(0x21, 3, 0, 0, "bootx\n")
