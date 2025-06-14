import asyncio
import logging
from typing import Optional
from asyncio.subprocess import Process
import aiohttp

async def wait_for_server(url: str, timeout: int = 60, interval: int = 5) -> bool:
    """Waits asynchronously until the server responds with HTTP 200."""
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return True
        except Exception:
            # Server isn't ready yet
            await asyncio.sleep(interval)
    return False

class ServerManager:
    def __init__(self, cwd: Optional[str] = None) -> None:
        # The working directory (if needed) to locate your server's executable
        self.cwd = cwd
        self.process: Optional[Process] = None
        self._port = 8080
        self._host = '127.0.0.1'
        self._monitor_task: Optional[asyncio.Task] = None
        self._connection_callback = None
        self._last_state = None

    def set_connection_callback(self, callback):
        """Set a callback to be called when connection state changes."""
        self._connection_callback = callback

    async def monitor_port(self, interval: float = 2.0):
        """Monitor the server port and call the callback on state change."""
        while True:
            is_up = await self.check_port()
            if is_up != self._last_state:
                self._last_state = is_up
                if self._connection_callback:
                    cb = self._connection_callback
                    if asyncio.iscoroutinefunction(cb):
                        await cb(is_up)
                    else:
                        cb(is_up)
            await asyncio.sleep(interval)

    def start_monitoring(self, interval: float = 2.0):
        if self._monitor_task is None or self._monitor_task.done():
            self._monitor_task = asyncio.create_task(self.monitor_port(interval))

    async def start_server(self, method: str = 'direct') -> bool:
        """
        Start the server using the given method.
        Supported methods: 'direct' (or 'piped' – which logs output).
        """
        cmd = ['open-webui', 'serve']

        try:
            if method == 'direct':
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=self.cwd
                )
            elif method == 'piped':
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=self.cwd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                if self.process.stdout:
                    asyncio.create_task(self._log_stream(self.process.stdout, "STDOUT"))
                if self.process.stderr:
                    asyncio.create_task(self._log_stream(self.process.stderr, "STDERR"))
            else:
                raise ValueError(f"Invalid startup method: {method}")

            # Wait a short time for the process to launch
            await asyncio.sleep(2)
            if await wait_for_server('http://127.0.0.1:8080/'):
                logging.info("Server is ready and accepting connections")
                return True
            else:
                logging.error("Server did not become ready within the timeout period")
                return False

        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            return False

    async def _log_stream(self, stream: asyncio.StreamReader, prefix: str) -> None:
        """Asynchronously log output from the given stream."""
        while True:
            line = await stream.readline()
            if line:
                logging.info(f"[Server {prefix}] {line.decode().strip()}")
            else:
                break

    async def check_port(self, timeout: float = 1.0) -> bool:
        """Check if the server port is open and accepting connections"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (ConnectionRefusedError, asyncio.TimeoutError):
            return False

    async def stop_server(self) -> None:
        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5)
                logging.info("Server terminated successfully")
            except asyncio.TimeoutError:
                logging.error("Server did not terminate in time")
            self.process = None
