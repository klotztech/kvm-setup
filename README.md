# KVM Setup
My personal QEMU KVM setup and configuration.

I currently mainly use the Xubuntu guest, which is configured for GPU passthrough for daily tasks and some Linux gaming. Only occasionally I fire up the Windows 10 guest and remote into it using either [Remmina](https://remmina.org/) or [FreeRDP](http://www.freerdp.com/) on the Linux guest.

## Table of contents

```
├── guest                   // Everything concerning the virtualized guest systems
│   ├── windows-10          // Windows 10 Pro configs + scripts
│   │   └── msi             // Registry patches for Message-Signaled Interrupts (MSI)
│   └── xubuntu-18.04       // Xubuntu 18.04 LTS configs + scripts
│       └── pulseaudio      // PulseAudio configuration
│
└── host                    // Everything concerning the host system
    ├── grub                // GRUB configuration
    ├── libvirt             // LibVirt configuration
    └── misc                // Miscellaneous configs + scripts
```
###### Thanks `tree(1)` 😉 <!-- $ tree -d -->
## Hardware specifications

**CPU:** Intel® Core™ i7-5820K @4.4GHz \
**RAM:** 32GB Corsair Vengeance LED DDR4-3000 CL15 Quad Kit (CMU32GX4M4C3000C15) \
**MoBo:** MSI X99A SLI Krait Edition \
**Primary GPU:** Gigabyte GeForce GTX 770 4GB Windforce 3X (GV-N770OC-4GD) \
**Secondary GPU:** ASUS Radeon HD 5450 Silent (90-C1CP20-L0UANABZ/90-C1CP2U-L0UANAYZ) \
**Storage:** Samsung 960 EVO 1TB NVMe SDD (MZ-V6E1T0BW)

### Peripherals

**Sound:** Focusrite Scarlett 2i2 USB (2nd Gen) \
**Display 1:** ASUS ROG Swift PG279Q 27" with G-Sync (90LM0230-B01370) \
**Display 2&3:** ASUS VE248H, 24" (90LMC3101Q01041C) \
**Additional:** Two mice and keyboards

🍻 *cheers!*
