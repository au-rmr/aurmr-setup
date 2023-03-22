import sys
import logging

import rich_click as click

from rich.logging import RichHandler
from rich.console import Console

logger = logging.getLogger(__name__)

console = Console()

@click.group()
@click.option("--verbose", "-v", default=False, count=True,
              help="Increase verbosity of the logging output. Can base used multiple times")
@click.option("--quiet", "-q", default=False, is_flag=True,
              help="Suppress all logging output except critical messages")
def cli(**kwargs):
    """
    aurmr command line interface

    Manages conda environments with ROS from robostack
    """
    log_config = {'handlers': [RichHandler(console=console, markup=True, rich_tracebacks=True)]}
    if kwargs['verbose'] and kwargs['quiet']:
        logger.error('verbose and quiet must be mutually exclusive')
        sys.exit(-1)
    elif kwargs['verbose'] == 1:
        logging.basicConfig(level=logging.INFO, **log_config)
    elif kwargs['verbose'] == 2:
        logging.basicConfig(level=logging.DEBUG, **log_config)
    elif kwargs['verbose'] >= 3:
        logging.basicConfig(level=logging.NOTSET, **log_config)
    elif kwargs['quiet']:
        logging.basicConfig(level=logging.CRITICAL, **log_config)
    else:
        logging.basicConfig(level=logging.INFO, **log_config)


