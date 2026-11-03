"""Command-line interface for retail vision inference."""

from __future__ import annotations

import argparse
from pathlib import Path

from retail_vision.config import Settings
from retail_vision.runner import run_stock_image, run_video


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="retail-vision",
        description="Retail shelf and activity inference using Roboflow.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    stock = commands.add_parser("stock-image", help="Run shelf detection on an image.")
    stock.add_argument("--image", required=True, help="Path to a shelf image.")
    stock.add_argument(
        "--output", default="outputs/stock-result.jpg",
        help="Annotated image output path.",
    )

    video = commands.add_parser("video", help="Run activity detection on video.")
    video.add_argument("--source", default="0", help="Video path or webcam index.")
    video.add_argument(
        "--output", default="outputs/activity-result.mp4",
        help="Annotated MP4 output path.",
    )
    video.add_argument(
        "--log", default="outputs/activity-events.csv",
        help="CSV detection log path.",
    )
    video.add_argument(
        "--preview", action="store_true",
        help="Show preview; press q to stop.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        settings = Settings.from_env()
        if args.command == "stock-image":
            counts = run_stock_image(
                Path(args.image), Path(args.output), settings
            )
            print("Detection counts:")
            for label, count in counts.items():
                print(f"  {label}: {count}")
            print(f"Annotated image saved to: {args.output}")
            return 0

        if args.command == "video":
            frames = run_video(
                source=args.source,
                output_path=Path(args.output),
                log_path=Path(args.log),
                settings=settings,
                preview=args.preview,
            )
            print(f"Processed {frames} frames.")
            print(f"Annotated video saved to: {args.output}")
            print(f"Detection log saved to: {args.log}")
            return 0
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
