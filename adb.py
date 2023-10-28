from ppadb.client import Client as PPADBClient
from utils import resource_path
from utils import build_command
from filepath.file_relative_paths import FilePaths
import subprocess
import traceback

bridge = None


class Adb:
    def __init__(self, host="127.0.0.1", port=5037):
        self.client = PPADBClient(host, port)

    def connect_to_device(self, host="127.0.0.1", port=5555):
        adb_path = resource_path(FilePaths.ADB_EXE_PATH.value)
        cmd = build_command(adb_path, "connect", "{}:{}".format(host, port))
        ret = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.PIPE, encoding="utf-8", timeout=2
        )
        return self.get_device(host)

    def get_client_devices(self):
        return self.client.devices()

    def get_device(self, host="127.0.0.1"):
        device = self.client.device("{}".format(host))
        return device


def enable_adb(host="127.0.0.1", port=5037):
    adb = None
    try:
        adb = Adb(host, port)

        version = adb.client.version()

    except RuntimeError as err:
        adb_path = resource_path(FilePaths.ADB_EXE_PATH.value)

        ret = subprocess.run(
            build_command(adb_path, "-P", str(port), "kill-server", host),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )

        ret = subprocess.run(
            build_command(adb_path, "-P", str(port), "connect", host),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        print("ret: ", ret)
        if ret.returncode != 0:
            raise RuntimeError("Error: fail to start adb server. \n({})".format(ret))

    return adb


def initAdb():
    client = PPADBClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    return devices
