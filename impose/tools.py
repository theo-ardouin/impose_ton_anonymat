import asyncio

from typing import Any, Callable


def loop(index: int, min: int, max: int) -> int:
    if index < min:
        return max
    if index >= max:
        return min
    return index


def runner(coroutine: Callable, *args: Any, **kwargs: Any) -> None:
    async def wrapper(coroutine: Callable, *args: Any, **kwargs: Any) -> Any:
        await coroutine(*args, **kwargs)

    asyncio.create_task(wrapper(coroutine, *args, **kwargs))
