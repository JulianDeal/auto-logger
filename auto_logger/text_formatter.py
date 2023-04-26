from typing import Any, Callable, Dict, List, Optional


def formatText(
    args: List[Any],
    kwargs: Dict[str, Any],
    ret: Any,
    *,
    objStr: str = "",
    method: Optional[Callable] = None,
    func: Optional[Callable] = None,
    time: Optional[float] = None,
):
    time_str = ""
    if time:
        time_str = f" TOOK {time}"
    if objStr:
        return (
            f"CALL METHOD <{method.__name__ if method else 'Unknown'}>"
            f" OF {objStr} WITH ARGS {args} KWARGS {kwargs} RETURNS  {ret}"
            f"{time_str}"
        )
    return (
        f"CALL FUNCTION <{func.__name__ if func else 'Unknown'}>"
        f" WITH ARGS {args} KWARGS {kwargs} RETURNS {ret}"
        f"{time_str}"
    )
