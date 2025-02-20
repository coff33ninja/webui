import asyncio
import pytest
from server_manager import ServerManager

@pytest.mark.asyncio
async def test_server_manager_stop_without_start() -> None:
    # Test that stopping a non-started server doesn't raise errors
    manager = ServerManager()
    await manager.stop_server()  # Should run silently without error

@pytest.mark.asyncio
async def test_invalid_start_method() -> None:
    manager = ServerManager()
    result = await manager.start_server(method='invalid')
    # Since the invalid method will raise a ValueError that is caught internally,
    # the start_server returns False
    assert result is False