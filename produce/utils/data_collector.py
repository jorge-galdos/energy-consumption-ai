"""Collect system data relevant to energy consumption. 

The SystemData class is exported to facilitate serialization and deserialization
of system data for producing and consuming messages via Kafka. The collect_data
function collects the data with psutil.
"""


from datetime import datetime

from pydantic import BaseModel
import psutil


class SystemData(BaseModel):
    """Represents system data relevant to energy consumption.

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
        timestamp: A datetime object representing the date and time the data
          was instantiated.
    """

    cpu_usage: float
    cpu_freq: float
    memory_usage: float
    disk_io: int
    net_io: int
    battery_percent: int
    power_plugged: bool
    time_left: int
    timestamp: datetime


def collect_data() -> SystemData:
    """Collects system data using psutil.

    Returns:
        SystemData: System data instance.
    """
    # Instantiate psutil data
    disk_io_counters = psutil.disk_io_counters()
    net_io_counters = psutil.net_io_counters()
    sensors_battery = psutil.sensors_battery()
    # Create and return SystemData object
    return SystemData(
        cpu_usage=psutil.cpu_percent(),
        cpu_freq=psutil.cpu_freq().current,
        memory_usage=psutil.virtual_memory().percent,
        disk_io=disk_io_counters.read_bytes + disk_io_counters.write_bytes,
        net_io=net_io_counters.bytes_sent + net_io_counters.bytes_recv,
        battery_percent=sensors_battery.percent,
        power_plugged=sensors_battery.power_plugged,
        time_left=sensors_battery.secsleft,
        timestamp=datetime.now(),
    )
