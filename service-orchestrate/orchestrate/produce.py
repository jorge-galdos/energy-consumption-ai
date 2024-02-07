"""Send commands to the Produce service.
"""

from datetime import datetime

import pytz
from faust import App
from faust.cli import option
import orchestrate.command_models.produce as cmd_mods  # pylint: disable=E0401


app = App(
    id="orch-produce",
    version=1,
    broker="aiokafka://localhost:29092",  # todo: Must modify for container    # os.environ.get("KAFKA_BROKER")
    serializer="json",
)

produce_commands_topic = app.topic("commands.produce")


@app.command(
    option(
        "--interval",
        type=int,
        default=5,
        help="Add delay of N seconds between messages.",
    ),
    option(
        "--max-messages",
        type=int,
        default=0,
        help="Send at most N messages or 0 for infinity.",
    ),
)
async def start(self, interval: int, max_messages: int) -> None:
    """Command Produce service to begin producing to `data.raw` topic."""
    # Initialize command from command models
    command = cmd_mods.StartProducingCommand(
        name=self.__name__, interval=interval, max_messages=max_messages
    )
    # Produce command to Kafka topic as JSON message
    timestamp = datetime.now(pytz.UTC).isoformat()
    await produce_commands_topic.send(
        value=command.model_dump(),
        headers=[
            ("source", bytes(app.conf.id, encoding="utf-8")),
            ("timestamp", bytes(timestamp, encoding="utf-8")),
        ],
    )
    app.logger.info(
        "<%s> command sent to <%s> topic successfully!",
        self.__name__,
        produce_commands_topic.get_topic_name(),
    )
