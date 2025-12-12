import httpx


class MCPHelloClient:
    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url

    async def call_tool(self, name: str, arguments: dict) -> str:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            },
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                self.mcp_url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=payload,
            )

        r.raise_for_status()
        data = r.json()

        try:
            return data["result"]["content"][0]["text"]
        except Exception:
            return str(data)[:2000]

    async def get_exchange_rate(self, date: str) -> str:
        return await self.call_tool(
            "get_exchange_rate",
            {"date": date},
        )

    async def say_hello(self, name: str) -> str:
        return await self.call_tool(
            "say_hello",
            {"name": name},
        )

    async def say_hello_multiple(self, names: list[str]) -> str:
        return await self.call_tool(
            "say_hello_multiple",
            {"names": names},
        )
