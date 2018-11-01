#!/usr/bin/python3 -u
import libvirt
import time
import threading
import os

print("vmpower starting..")

# LIBVIRT_ENDPOINT = "qemu+ssh://sk@sk01/system"
LIBVIRT_ENDPOINT = "qemu:///system"
MAIN_VM_NAME = "xubuntu"

# sk@skubu02:~/vmpower$ python main.py
# EVENT: Domain win10x64(2) VIR_DOMAIN_EVENT_SHUTDOWN(6) 0
# EVENT: Domain win10x64(2) VIR_DOMAIN_EVENT_STOPPED(5) 0

# EVENT: Domain win10x64(3) VIR_DOMAIN_EVENT_RESUMED(4) 0
# EVENT: Domain win10x64(3) VIR_DOMAIN_EVENT_STARTED(2) 0

# EVENT: Domain win10x64(3) VIR_DOMAIN_EVENT_SHUTDOWN(6) 0
# EVENT: Domain win10x64(3) VIR_DOMAIN_EVENT_STOPPED(5) 0


# virDomainEventType is emitted during domain lifecycles (see libvirt.h)
VIR_DOMAIN_EVENT_MAPPING = {
    0: "VIR_DOMAIN_EVENT_DEFINED",
    1: "VIR_DOMAIN_EVENT_UNDEFINED",
    2: "VIR_DOMAIN_EVENT_STARTED",
    3: "VIR_DOMAIN_EVENT_SUSPENDED",
    4: "VIR_DOMAIN_EVENT_RESUMED",
    5: "VIR_DOMAIN_EVENT_STOPPED",
    6: "VIR_DOMAIN_EVENT_SHUTDOWN",
    7: "VIR_DOMAIN_EVENT_PMSUSPENDED",
}

VIR_DOMAIN_EVENT_DEFINED = 0
VIR_DOMAIN_EVENT_UNDEFINED = 1
VIR_DOMAIN_EVENT_STARTED = 2
VIR_DOMAIN_EVENT_SUSPENDED = 3
VIR_DOMAIN_EVENT_RESUMED = 4
VIR_DOMAIN_EVENT_STOPPED = 5
VIR_DOMAIN_EVENT_SHUTDOWN = 6
VIR_DOMAIN_EVENT_PMSUSPENDED = 7

# virDomainState
VIR_DOMAIN_STATE_MAPPING = {
    0: "VIR_DOMAIN_NOSTATE",
    1: "VIR_DOMAIN_RUNNING",
    2: "VIR_DOMAIN_BLOCKED",
    3: "VIR_DOMAIN_PAUSED",
    4: "VIR_DOMAIN_SHUTDOWN",
    5: "VIR_DOMAIN_SHUTOFF",
    6: "VIR_DOMAIN_CRASHED",
    7: "VIR_DOMAIN_PMSUSPENDED",
}

def callback(conn, dom, event, detail, opaque):
    print("EVENT: Domain %s(%s) %s(%s) %s" % (dom.name(), dom.ID(), VIR_DOMAIN_EVENT_MAPPING[event], event, detail))

    # check for main vm shutdown
    if dom.name() == MAIN_VM_NAME and event == VIR_DOMAIN_EVENT_STOPPED:
        vmHasStopped()

def who():
    output = os.popen("/usr/bin/who").read() # see who's logged in
    output = output.split("\n") # split lines
    output = filter(None, output) # strip empty lines
    return list(output)

def vmHasStopped():
    print("main vm %s has stopped" % (MAIN_VM_NAME))
    for x in range(10):
        sessions = who()
        if len(sessions) > 0:
            print("num sessions = %d" % (len(sessions)))
            time.sleep(1)
            continue

        hypervisorShutdown()
        return

    print("not shutting down, cuz there's still someone logged in")

def hypervisorShutdown():
    print("shutting down hypervisor...")
    os.system("/usr/bin/sudo /bin/systemctl poweroff")

# event handling setup

eventLoopThread = None

def virEventLoopNativeRun():
    while True:
        libvirt.virEventRunDefaultImpl()

def virEventLoopNativeStart():
    global eventLoopThread
    libvirt.virEventRegisterDefaultImpl()
    eventLoopThread = threading.Thread(target=virEventLoopNativeRun,
                                       name="libvirtEventLoop")
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()

if __name__ == "__main__":
    virEventLoopNativeStart()

    print("connecting to libvirt at %s" % (LIBVIRT_ENDPOINT))
    conn = libvirt.openReadOnly(LIBVIRT_ENDPOINT)

    conn.domainEventRegister(callback, None)
    conn.setKeepAlive(5, 3)

    while conn.isAlive() == 1:
        time.sleep(1)
