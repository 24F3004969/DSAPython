#!/usr/bin/env python3
"""
Animate the 'world's most complex' graph by incrementally revealing edges.

Two input modes:
  (A) Parse edges from a user's insert-only file that looks like:
      v_001 = Vertex("V001")
      ...
      my_graph.add_edge(v_001, v_057)
      ...
      (file path via --insert-file)

  (B) Regenerate the graph procedurally (same seed and parameters as before)
      using NetworkX models (Barabási–Albert, Watts–Strogatz, grid/mesh).

Outputs:
  - GIF (always) via PillowWriter
  - MP4 (optional) if ffmpeg is available

Dependencies:
  pip install networkx matplotlib pillow
  (ffmpeg optional for MP4)
"""

import argparse
import math
import os
import random
import re
import sys
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter


# ----------------------------
# Defaults (match the previous build)
# ----------------------------
SEED = 42
L1_CORE_N = 60     # Barabási–Albert
L2_SW_N   = 60     # Watts–Strogatz
L3_GRID_W = 8
L3_GRID_H = 5
L3_GRID_N = L3_GRID_W * L3_GRID_H

DEFAULT_GIF = "complex_graph_build.gif"
DEFAULT_MP4 = "complex_graph_build.mp4"
DEFAULT_FPS = 18
DEFAULT_BATCH = 30  # edges per frame (≈35 frames for ~1,049 edges)


# ----------------------------
# Helpers
# ----------------------------
def parse_insert_only(path: str) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Parse a user's insert-only file that declares Vertex(...) and then calls:
    my_graph.add_edge(v_xxx, v_yyy)
    Returns (N, edge_list) where N is max node id found.
    """
    vertex_re = re.compile(r'^v_(\d{3})\s*=\s*Vertex\("V\d{3}"\)')
    edge_re   = re.compile(r'^my_graph\.add_edge\(v_(\d{3}),\s*v_(\d{3})\)')

    node_ids = set()
    edges: List[Tuple[int,int]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            m_v = vertex_re.match(s)
            if m_v:
                node_ids.add(int(m_v.group(1)))
                continue
            m_e = edge_re.match(s)
            if m_e:
                u = int(m_e.group(1))
                v = int(m_e.group(2))
                edges.append((u, v))

    if not node_ids:
        raise RuntimeError(f"No vertices parsed from {path}. "
                           "Ensure the file contains Vertex(...) lines.")

    N = max(node_ids)
    return N, edges


def build_hybrid_graph(seed: int = SEED) -> Tuple[nx.DiGraph, List[int], List[int], List[int]]:
    """
    Rebuild the hybrid 'world's most complex' graph deterministically:
      - L1: Barabási–Albert core
      - L2: Watts–Strogatz small-world ring
      - L3: Grid/mesh
      - Directed edges with some bidirectional arcs
      - Inter-layer connectors (forward heavy + some backward + L1<->L3 shortcuts)
    """
    random.seed(seed)

    # Layers as undirected bases
    G1 = nx.barabasi_albert_graph(n=L1_CORE_N, m=3, seed=seed)
    G2 = nx.watts_strogatz_graph(n=L2_SW_N, k=6, p=0.2, seed=seed)
    G3_grid = nx.grid_2d_graph(L3_GRID_H, L3_GRID_W)  # nodes are (r, c)
    mapping_grid = {node: i for i, node in enumerate(G3_grid.nodes())}
    G3 = nx.relabel_nodes(G3_grid, mapping_grid, copy=True)

    # Directed master
    G = nx.DiGraph()
    N1 = L1_CORE_N
    N2 = L2_SW_N
    N3 = L3_GRID_N
    TOTAL = N1 + N2 + N3

    # 1-indexed node ids (match v_001..v_160 convention)
    L1_nodes = list(range(1, N1 + 1))
    L2_nodes = list(range(N1 + 1, N1 + N2 + 1))
    L3_nodes = list(range(N1 + N2 + 1, TOTAL + 1))

    G.add_nodes_from(L1_nodes + L2_nodes + L3_nodes)

    def add_oriented(u, v, p_bi=0.18):
        if random.random() < 0.5:
            a, b = u, v
        else:
            a, b = v, u
        G.add_edge(a, b)
        if random.random() < p_bi:
            G.add_edge(b, a)

    # Intra-layer (orient undirected edges)
    for u, v in G1.edges():
        add_oriented(L1_nodes[u], L1_nodes[v])
    for u, v in G2.edges():
        add_oriented(L2_nodes[u], L2_nodes[v])
    for u, v in G3.edges():
        add_oriented(L3_nodes[u], L3_nodes[v])

    # Inter-layer connectors
    for _ in range(220):
        G.add_edge(random.choice(L1_nodes), random.choice(L2_nodes))
    for _ in range(40):
        G.add_edge(random.choice(L2_nodes), random.choice(L1_nodes))
    for _ in range(220):
        G.add_edge(random.choice(L2_nodes), random.choice(L3_nodes))
    for _ in range(40):
        G.add_edge(random.choice(L3_nodes), random.choice(L2_nodes))
    for _ in range(60):
        a = random.choice(L1_nodes)
        b = random.choice(L3_nodes)
        if random.random() < 0.7:
            G.add_edge(a, b)
        else:
            G.add_edge(b, a)

    return G, L1_nodes, L2_nodes, L3_nodes


def compute_layered_layout(G: nx.DiGraph,
                           L1_nodes: List[int],
                           L2_nodes: List[int],
                           L3_nodes: List[int],
                           seed: int = SEED) -> Dict[int, Tuple[float, float]]:
    """
    Spring layout plus vertical offsets by layer.
    """
    N = G.number_of_nodes()
    base_pos = nx.spring_layout(G, k=1.1 / math.sqrt(N), seed=seed, iterations=200)

    pos = {}
    for n in G.nodes():
        x, y = base_pos[n]
        if n in L1_nodes:
            pos[n] = (x, y + 1.0)
        elif n in L2_nodes:
            pos[n] = (x, y + 0.0)
        else:
            pos[n] = (x, y - 1.0)
    return pos


def animate_build(G: nx.DiGraph,
                  pos: Dict[int, Tuple[float, float]],
                  L1_nodes: List[int],
                  L2_nodes: List[int],
                  L3_nodes: List[int],
                  gif_out: str,
                  mp4_out: str,
                  fps: int = DEFAULT_FPS,
                  batch_size: int = DEFAULT_BATCH) -> None:
    """
    Animate by incrementally revealing edges.
    """
    # Colors by layer
    node_colors = []
    for n in G.nodes():
        if n in L1_nodes:
            node_colors.append("#0EA5E9")  # sky blue
        elif n in L2_nodes:
            node_colors.append("#22C55E")  # emerald
        else:
            node_colors.append("#F59E0B")  # amber

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_title("Complex Graph — incremental edge reveal", fontsize=14)
    ax.axis("off")

    # Draw nodes once
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=list(G.nodes()),
        node_size=120,
        node_color=node_colors,
        alpha=0.95,
        edgecolors="white",
        linewidths=0.5,
        ax=ax
    )

    # Show a subset of labels to avoid clutter
    subset_labels = {n: f"V{n:03d}" for i, n in enumerate(G.nodes()) if i % 12 == 0}
    nx.draw_networkx_labels(G, pos, labels=subset_labels, font_size=7, font_color="#111827", ax=ax)

    edges = list(G.edges())
    total_e = len(edges)
    num_frames = max(1, (total_e + batch_size - 1) // batch_size)
    current_edges: List[Tuple[int, int]] = []
    edge_artists = []

    def init():
        return []

    def update(frame_idx):
        start = frame_idx * batch_size
        end = min((frame_idx + 1) * batch_size, total_e)
        current_edges.extend(edges[start:end])

        for art in edge_artists:
            art.remove()
        edge_artists.clear()

        artists = nx.draw_networkx_edges(
            G, pos,
            edgelist=current_edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=8,
            width=0.6,
            alpha=0.28,
            edge_color="#111827",
            ax=ax
        )
        if not isinstance(artists, (list, tuple)):
            artists = [artists]
        edge_artists.extend(artists)

        ax.set_xlabel(f"Edges shown: {len(current_edges)} / {total_e}", fontsize=10)
        return artists

    anim = FuncAnimation(
        fig, update, init_func=init,
        frames=num_frames, interval=int(1000 / fps),
        blit=False, repeat=False
    )

    # Always save GIF
    anim.save(gif_out, writer=PillowWriter(fps=fps))
    print(f"[OK] GIF saved -> {gif_out}")

    # Try to save MP4 if ffmpeg available
    try:
        anim.save(mp4_out, writer="ffmpeg", fps=fps, dpi=150)
        print(f"[OK] MP4 saved -> {mp4_out}")
    except Exception as e:
        print(f"[WARN] MP4 not saved (ffmpeg not available?): {e}")


# ----------------------------
# CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Animate the world's most complex graph.")
    parser.add_argument("--insert-file", type=str, default=None,
                        help="Path to insert-only file (e.g., world_most_complex_graph_insert_only.py). "
                             "If absent, the graph is regenerated procedurally.")
    parser.add_argument("--gif", type=str, default=DEFAULT_GIF, help="Output GIF file path.")
    parser.add_argument("--mp4", type=str, default=DEFAULT_MP4, help="Output MP4 file path (best effort).")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second.")
    parser.add_argument("--batch", type=int, default=DEFAULT_BATCH, help="Edges per frame.")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed (for regenerated mode).")
    args = parser.parse_args()

    # Build graph
    if args.insert_file and os.path.isfile(args.insert_file):
        print(f"[INFO] Parsing insert-only file: {args.insert_file}")
        N, edge_list = parse_insert_only(args.insert_file)
        print(f"[INFO] Parsed {N} vertices and {len(edge_list)} edges")

        # Reconstruct G from parsed edges
        G = nx.DiGraph()
        G.add_nodes_from(range(1, N + 1))
        G.add_edges_from(edge_list)

        # Infer layer membership using the known layer sizes
        L1_nodes = list(range(1, L1_CORE_N + 1))
        L2_nodes = list(range(L1_CORE_N + 1, L1_CORE_N + L2_SW_N + 1))
        L3_nodes = list(range(L1_CORE_N + L2_SW_N + 1, N + 1))
    else:
        print("[INFO] Insert-only file not provided/found; regenerating procedurally.")
        G, L1_nodes, L2_nodes, L3_nodes = build_hybrid_graph(seed=args.seed)
        print(f"[INFO] Generated {G.number_of_nodes()} vertices and {G.number_of_edges()} edges")

    # Layout
    pos = compute_layered_layout(G, L1_nodes, L2_nodes, L3_nodes, seed=args.seed)

    # Animate
    animate_build(G, pos, L1_nodes, L2_nodes, L3_nodes,
                  gif_out=args.gif, mp4_out=args.mp4,
                  fps=args.fps, batch_size=args.batch)


if __name__ == "__main__":
    main()