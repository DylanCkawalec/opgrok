"""Parallel DAG scheduling — run ready SuperGroks concurrently."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable


def topo_layers(nodes: list[dict], edges: list[dict]) -> list[list[str]]:
    """Return layers of node ids that can run in parallel."""
    ids = [n["id"] for n in nodes]
    preds: dict[str, set[str]] = {i: set() for i in ids}
    for e in edges:
        frm, to = e.get("from"), e.get("to")
        if frm in preds and to in preds:
            preds[to].add(frm)
    remaining = set(ids)
    done: set[str] = set()
    layers: list[list[str]] = []
    # preserve declared order as tie-break
    order_index = {i: idx for idx, i in enumerate(ids)}
    while remaining:
        ready = [i for i in remaining if preds[i].issubset(done)]
        if not ready:
            # cycle or bad edge — fall back to remaining serial
            ready = sorted(remaining, key=lambda x: order_index[x])
            layers.append(ready)
            break
        ready.sort(key=lambda x: order_index[x])
        layers.append(ready)
        for i in ready:
            remaining.remove(i)
            done.add(i)
    return layers


def ready_wave(
    layer_ids: list[str],
    run_one: Callable[[str], Any],
    parallel: bool,
    max_workers: int = 4,
) -> dict[str, Any]:
    """Execute a layer; returns {node_id: result}."""
    if not parallel or len(layer_ids) == 1:
        return {nid: run_one(nid) for nid in layer_ids}
    out: dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=min(max_workers, len(layer_ids))) as ex:
        futs = {ex.submit(run_one, nid): nid for nid in layer_ids}
        for fut in as_completed(futs):
            nid = futs[fut]
            out[nid] = fut.result()
    # stable order
    return {nid: out[nid] for nid in layer_ids}
