Python script to power off the host system when the main VM shuts down and there's noone logged into the host system (interactively or via SSH).

## Files

| Repository file | System path                         |
| --------------- | ----------------------------------- |
| main.py         | /opt/vmpower/main.py                |
| sudoers         | /etc/sudoers                        |
| vmpower.service | /etc/systemd/system/vmpower.service |

## Configuration

In `main.py` set `MAIN_VM_NAME` to the name of the libvirt domain to be watched for shutdown events (i.e. your main VM).

For the automatic shutdown to work, the `/etc/sudoers` file needs to be extended by the above files contents. By that the script will be able to execute `systemctl poweroff` as root without authenticating and/or a real tty (as daemon).

To run the python script as a systemd service, add the above unit definition file to `/etc/systemd/system`. In this file, setup the correct user/group with whose privileges the script shall be executed. This user has to be able to execute `main.py` and be affected by the afore-mentioned sudo rule.

To pull in the newly added unit run the following command:

``systemctl daemon-reload``

To run auto-start the service on boot run the following command:

``systemctl enable vmpower.service``