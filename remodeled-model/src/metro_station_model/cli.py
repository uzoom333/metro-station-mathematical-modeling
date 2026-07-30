"""Command-line interface for Version 2."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .optimization import run_optimization, save_optimization
from .results import save_result
from .scenarios import run_all_scenarios
from .sensitivity import run_latin_hypercube, run_oat, save_sensitivity
from .solver import simulate


def build_parser() -> argparse.ArgumentParser:
    """Build the public command-line parser."""
    parser = argparse.ArgumentParser(prog="metro-station")
    commands = parser.add_subparsers(dest="command", required=True)
    simulate_parser = commands.add_parser("simulate")
    simulate_parser.add_argument("--config", required=True)
    simulate_parser.add_argument("--output", default="results/baseline")
    scenarios_parser = commands.add_parser("scenarios")
    scenarios_parser.add_argument("--config-dir", default="configs")
    scenarios_parser.add_argument("--output", default="results/scenarios")
    sensitivity_parser = commands.add_parser("sensitivity")
    sensitivity_parser.add_argument("--config", required=True)
    sensitivity_parser.add_argument("--samples", type=int, default=500)
    sensitivity_parser.add_argument("--output", default="results/sensitivity")
    optimize_parser = commands.add_parser("optimize")
    optimize_parser.add_argument("--config", required=True)
    optimize_parser.add_argument("--output", default="results/optimization")
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the requested simulation workflow."""
    args = build_parser().parse_args(argv)
    if args.command == "simulate":
        result = simulate(load_config(args.config))
        save_result(result, args.output)
        print(f"Saved {result.config.name} results to {Path(args.output)}")
    elif args.command == "scenarios":
        results, _ = run_all_scenarios(args.config_dir, args.output)
        print(f"Completed {len(results)} scenarios")
    elif args.command == "sensitivity":
        config = load_config(args.config)
        ranks = save_sensitivity(
            run_oat(config),
            run_latin_hypercube(config, args.samples),
            args.output,
        )
        print(f"Completed sensitivity analysis ({len(ranks)} parameters)")
    elif args.command == "optimize":
        config = load_config(args.config)
        frame = run_optimization(config)
        best = save_optimization(frame, args.output)
        print(f"Evaluated {len(frame)} combinations; {len(best)} best records saved")
