"""Pydantic command models for Produce service. 
"""

from pydantic import BaseModel, PositiveInt


class StartProducingCommand(BaseModel):
    """Command model for `start_producing` command.

    Attributes:
        name (str): Command name.
        interval (PositiveInt): Optional flag to set the interval at which to
          produce system data.
        max_messages (PositiveInt): Optional flag to limit the total number of
          messages produced.
    """

    name: str
    interval: PositiveInt
    max_messages: PositiveInt
