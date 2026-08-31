import logging

import pytest


@pytest.fixture
def unique_tag(request):
    """A logger tag unique to each test.

    ``logging.getLogger`` returns a process-wide singleton per name, so tests
    that share a tag would leak handlers and level config into each other.
    Handing every test its own tag keeps them isolated; the fixture also tears
    the logger down afterwards.
    """
    tag = f"klogs_test_{request.node.name}"
    yield tag
    logger = logging.getLogger(tag)
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    logging.Logger.manager.loggerDict.pop(tag, None)
