"""Collect system data relevant to energy consumption. 

The SystemDataCollector class is exported to collect system data at a point in
time and format as JSON message for real-time data streaming.

Typical usage:
    collector = SystemDataCollector()
    message = collector.produce_json_message()
"""


from dataclasses import dataclass, asdict
import json
from datetime import datetime

import psutil


@dataclass
class SystemData:
    """Represents system data.

    Attributes:
        cpu_usage: A float representing CPU usage as a percentage.
        cpu_freq: A float representing CPU frequency in MHz.
        memory_usage: A float representing memory usage as a percentage.
        disk_io: An integer representing total bytes read and written to disk.
        net_io: An integer representing total bytes sent and recieved.
        battery_percent: An integer representing remaining battery percentage.
        power_plugged: Indicates if the system is plugged into power.
        time_left: An integer representing estimated remaining battery life in
          seconds.
        timestamp: A string timestamp in ISO format.
    """

    cpu_usage: float
    cpu_freq: float
    memory_usage: float
    disk_io: int
    net_io: int
    battery_percent: int
    power_plugged: bool
    time_left: int
    timestamp: str


class SystemDataCollector:
    """Collects system data and produces JSON message.

    Attributes:
        data: A SystemData instance.
    """

    def __init__(self) -> None:
        self.data = self.collect_data()

    def collect_data(self) -> SystemData:
        """Collects system data using psutils.

        Returns:
            SystemData: System data at a specific point in time.
        """
        # CPU usage as a percentage
        cpu_usage = psutil.cpu_percent()
        # CPU frequency in MHz
        cpu_freq = psutil.cpu_freq().current
        # Memory usage as a percentage
        memory_usage = psutil.virtual_memory().percent
        # Disk I/O in bytes
        disk_io_counters = psutil.disk_io_counters()
        disk_io = disk_io_counters.read_bytes + disk_io_counters.write_bytes
        # Network I/O in bytes
        net_io_counters = psutil.net_io_counters()
        net_io = net_io_counters.bytes_sent + net_io_counters.bytes_recv
        # Battery information
        sensors_battery = psutil.sensors_battery()
        battery_percent = sensors_battery.percent
        power_plugged = sensors_battery.power_plugged
        time_left = sensors_battery.secsleft
        # Timestamp
        timestamp = datetime.now().isoformat()
        # Create and return a SystemData object
        return SystemData(
            cpu_usage=cpu_usage,
            cpu_freq=cpu_freq,
            memory_usage=memory_usage,
            disk_io=disk_io,
            net_io=net_io,
            battery_percent=battery_percent,
            power_plugged=power_plugged,
            time_left=time_left,
            timestamp=timestamp,
        )

    def produce_json_message(self) -> str:
        """Produces JSON message from SystemData object using json and asdict.

        Returns:
            str: JSON message.
        """
        # Convert SystemData object to a JSON string
        return json.dumps(asdict(self.data))
