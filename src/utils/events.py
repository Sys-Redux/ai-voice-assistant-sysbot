"""Event bus for inter-module communication"""
import asyncio
from typing import Callable, Any
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Event:
    name: str
    data: Any = None

class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._async_subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable):
        if asyncio.iscoroutinefunction(callback):
            self._async_subscribers[event_name].append(callback)
        else:
            self.subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):
        if callback in self._subscribers[event_name]:
            self.subscribers[event_name].remove(callback)
        if callback in self._async_subscribers[event_name]:
            self._async_subscribers[event_name].remove(callback)

    async def emit(self, event: Event):
        # Sync subscribers
        for callback in self.subscribers[event.name]:
            callback(event)

        # Async subscribers
        tasks = [
            callback(event)
            for callback in self._async_subscribers[event.name]
        ]
        if tasks:
            await asyncio.gather(*tasks)

event_bus = EventBus()