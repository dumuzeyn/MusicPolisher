import argparse
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

import music2picture
import music_metadata


SCRIPT_DIR = Path(__file__).resolve().parent

# PyCharm / direct Python run settings.
# Set RUN_FROM_CODE = True, edit the paths below, then press Run.
RUN_FROM_CODE = False
CODE_SOURCE = r"C:\Path\To\MusicFolder"
CODE_OUTPUT = r"C:\Path\To\ProcessedMusic"
CODE_GENRE = None
CODE_COLOR_MODE = "plasma"
CODE_INTEGRATED_LUFS = -14.0
CODE_TRUE_PEAK = -1.5
CODE_LRA = 11.0
CODE_FINAL_GAIN = 1.15
CODE_DENOISE = True
CODE_DENOISE_STRENGTH = 4.0
CODE_LIMITER = True
CODE_OVERWRITE_GENRE = False
CODE_EXTRA_METADATA = {}
CODE_COVER_SEED = None
CODE_COVER_SIZE = 1000
CODE_COVER_PATTERNS = 2
CODE_CENTER_TITLE = True
CODE_EMBED_COVER = True
CODE_CHANGE_COVER = True


def load_python_file(name, filename):
    module_path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


normalize_music_file = load_python_file("normalize_music_file", "Normalize-Music.py")


def ask_path(prompt):
    while True:
        value = input(prompt).strip().strip('"')
        if value:
            return value
        print("Please enter a path.")


def ask_settings():
    source = ask_path("Source folder or audio file: ")
    output = ask_path("Output folder: ")
    genre = input("Genre for songs without genre, or Enter for auto-detect: ").strip()
    return source, output, genre or None


def publish_processed_tree(staging_path, output_path):
    output_path.mkdir(parents=True, exist_ok=True)
    for source_item in staging_path.rglob("*"):
        relative = source_item.relative_to(staging_path)
        target_item = output_path / relative
        if source_item.is_dir():
            target_item.mkdir(parents=True, exist_ok=True)
            continue

        target_item.parent.mkdir(parents=True, exist_ok=True)
        if target_item.exists():
            target_item.unlink()
        shutil.move(str(source_item), str(target_item))


def process_music(
    source,
    output,
    genre=None,
    color_mode="plasma",
    integrated_lufs=-14.0,
    true_peak=-1.5,
    lra=11.0,
    final_gain=1.15,
    denoise=True,
    denoise_strength=4.0,
    limiter=True,
    overwrite_genre=False,
    extra_metadata=None,
    cover_seed=None,
    cover_size=1000,
    cover_patterns=2,
    center_title=True,
    embed_cover=True,
    change_cover=True,
):
    source_path = Path(source).expanduser()
    output_path = Path(output).expanduser()
    output_parent = output_path.resolve().parent
    output_parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="musicpolisher_", dir=output_parent) as temp_dir:
        staging_path = Path(temp_dir) / "processed"
        covers_path = staging_path / "covers"

        print("\nStep 1/4: normalize, gently denoise, and safely boost audio")
        normalize_music_file.normalize_music(
            source_path,
            staging_path,
            integrated_lufs=integrated_lufs,
            true_peak=true_peak,
            lra=lra,
            final_gain=final_gain,
            denoise=denoise,
            denoise_strength=denoise_strength,
            limiter=limiter,
        )

        print("\nStep 2/4: write clean title/genre metadata")
        music_metadata.require_ffmpeg()
        music_metadata.update_music_metadata(
            staging_path,
            genre_override=genre,
            overwrite_genre=overwrite_genre,
            extra_metadata=extra_metadata,
        )

        if change_cover:
            print("\nStep 3/4: create and embed covers")
            music2picture.require_ffmpeg()
            music2picture.make_covers(
                staging_path,
                covers_path,
                size=cover_size,
                patterns=cover_patterns,
                center_title=center_title,
                embed=embed_cover,
                color_mode=color_mode,
                seed=cover_seed,
            )
        else:
            print("\nStep 3/4: skip cover changes")

        print("\nStep 4/4: publish processed files to output folder")
        publish_processed_tree(staging_path, output_path)

    print(f"\nDone. Songs are saved in: {output_path.resolve()}")
    if change_cover:
        print(f"Covers are saved in: {(output_path / 'covers').resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="All-in-one music processor: normalize audio, clean metadata, create and embed covers."
    )
    parser.add_argument("--source", help="Folder with source songs or one audio file.")
    parser.add_argument("--output", help="Folder where processed songs and covers will be saved.")
    parser.add_argument("--genre", help="Set genre for songs that do not already have genre. Omit for auto-detect.")
    parser.add_argument("--artist", help="Set artist metadata.")
    parser.add_argument("--album", help="Set album metadata.")
    parser.add_argument("--album-artist", help="Set album artist metadata.")
    parser.add_argument("--composer", help="Set composer metadata.")
    parser.add_argument("--date", help="Set date/year metadata.")
    parser.add_argument("--track", help="Set track metadata.")
    parser.add_argument("--comment", help="Set comment metadata.")
    parser.add_argument("--color-mode", choices=sorted(music2picture.COLOR_MODES), default="plasma", help="Cover color mode.")
    parser.add_argument("--integrated-lufs", type=float, default=-14.0, help="Target integrated loudness.")
    parser.add_argument("--true-peak", type=float, default=-1.5, help="Target true peak.")
    parser.add_argument("--lra", type=float, default=11.0, help="Target loudness range.")
    parser.add_argument("--final-gain", type=float, default=1.15, help="Extra gain after loudnorm. Lower than old 1.30 to avoid artifacts.")
    parser.add_argument("--denoise", dest="denoise", action="store_true", default=True, help="Use gentle denoise. Enabled by default.")
    parser.add_argument("--no-denoise", dest="denoise", action="store_false", help="Disable denoise.")
    parser.add_argument("--denoise-strength", type=float, default=4.0, help="Gentle denoise amount in dB.")
    parser.add_argument("--limiter", dest="limiter", action="store_true", default=True, help="Use final limiter. Enabled by default.")
    parser.add_argument("--no-limiter", dest="limiter", action="store_false", help="Disable final limiter.")
    parser.add_argument("--overwrite-genre", action="store_true", help="Replace existing genre tags. Default keeps them.")
    parser.add_argument("--cover-seed", type=int, help="Use an integer for repeatable generated covers.")
    parser.add_argument("--cover-size", type=int, default=1000, help="Generated cover size in pixels.")
    parser.add_argument("--cover-patterns", type=int, choices=[1, 2], default=2, help="Cover pattern detail level.")
    parser.add_argument("--center-title", dest="center_title", action="store_true", default=True, help="Draw title in the center of the cover. Enabled by default.")
    parser.add_argument("--no-center-title", dest="center_title", action="store_false", help="Do not draw title in the center.")
    parser.add_argument("--embed-cover", dest="embed_cover", action="store_true", default=True, help="Embed generated cover into MP3. Enabled by default.")
    parser.add_argument("--no-embed-cover", dest="embed_cover", action="store_false", help="Do not embed generated cover.")
    parser.add_argument("--change-cover", dest="change_cover", action="store_true", default=True, help="Generate and embed a new cover. Enabled by default.")
    parser.add_argument("--no-change-cover", dest="change_cover", action="store_false", help="Do not generate or embed a new cover.")
    args = parser.parse_args()

    if args.source and args.output:
        source, output, genre = args.source, args.output, args.genre
    else:
        source, output, genre = ask_settings()

    process_music(
        source,
        output,
        genre=genre,
        color_mode=args.color_mode,
        integrated_lufs=args.integrated_lufs,
        true_peak=args.true_peak,
        lra=args.lra,
        final_gain=args.final_gain,
        denoise=args.denoise,
        denoise_strength=args.denoise_strength,
        limiter=args.limiter,
        overwrite_genre=args.overwrite_genre,
        extra_metadata={
            "artist": args.artist,
            "album": args.album,
            "album_artist": args.album_artist,
            "composer": args.composer,
            "date": args.date,
            "track": args.track,
            "comment": args.comment,
        },
        cover_seed=args.cover_seed,
        cover_size=args.cover_size,
        cover_patterns=args.cover_patterns,
        center_title=args.center_title,
        embed_cover=args.embed_cover,
        change_cover=args.change_cover,
    )


def run_from_code_settings():
    process_music(
        CODE_SOURCE,
        CODE_OUTPUT,
        genre=CODE_GENRE,
        color_mode=CODE_COLOR_MODE,
        integrated_lufs=CODE_INTEGRATED_LUFS,
        true_peak=CODE_TRUE_PEAK,
        lra=CODE_LRA,
        final_gain=CODE_FINAL_GAIN,
        denoise=CODE_DENOISE,
        denoise_strength=CODE_DENOISE_STRENGTH,
        limiter=CODE_LIMITER,
        overwrite_genre=CODE_OVERWRITE_GENRE,
        extra_metadata=CODE_EXTRA_METADATA,
        cover_seed=CODE_COVER_SEED,
        cover_size=CODE_COVER_SIZE,
        cover_patterns=CODE_COVER_PATTERNS,
        center_title=CODE_CENTER_TITLE,
        embed_cover=CODE_EMBED_COVER,
        change_cover=CODE_CHANGE_COVER,
    )


if __name__ == "__main__":
    try:
        if RUN_FROM_CODE:
            run_from_code_settings()
        else:
            main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
