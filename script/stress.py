
import argparse
#import random
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXTENSIONS = ["py", "out", "exe"]


def find(path: Path, name: str):
    for e in EXTENSIONS:
        file_path = (path / f"{name}.{e}")
        if file_path.is_file():
            return file_path
    raise FileNotFoundError(f'"{name}" in {path} not found')

def run(cmd, input_data=None, timeout=2):
    return subprocess.run(
        cmd,
        input=input_data,
        text=True,
        capture_output=True,
        timeout=timeout,
        cwd=BASE_DIR,
        check=False,
    )


def save_failure(seed, input_data=None, ac=None, wa=None):
    prob_dir = BASE_DIR / "WA" / f"{seed:04d}"
    prob_dir.mkdir(parents=True, exist_ok=True)

    if input_data is not None:
        (prob_dir / "fail.in").write_text(input_data, encoding="utf-8")

    #(prob_dir / "fail.seed").write_text(str(seed), encoding="utf-8")

    if ac is not None:
        (prob_dir / "ac.out").write_text(
            ac.stdout, encoding="utf-8"
        )
        (prob_dir / "ac.err").write_text(
            ac.stderr, encoding="utf-8"
        )

    if wa is not None:
        (prob_dir / "wa.out").write_text(
            wa.stdout, encoding="utf-8"
        )
        (prob_dir / "wa.err").write_text(
            wa.stderr, encoding="utf-8"
        )
    return prob_dir

def is_continue():
    try:
        ans = input("continue? [Y/n] ")
    except KeyboardInterrupt:
        print(flush=True)
        return False
    if ans.lower() in ["n", "no"]:
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--tests", type=int, default=1000)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    PROBMEL_PATH = BASE_DIR / "problem"
    GEN_PATH = find(PROBMEL_PATH, "gen")
    AC_PATH = find(PROBMEL_PATH, "ac")
    WA_PATH = find(PROBMEL_PATH, "wa")


    for i in range(args.tests):
        seed = args.seed + i
        input_data = None
        ac = None
        wa = None
        stage = "generator"

        try:
            # 1. 入力生成
            gen = run(
                [sys.executable, GEN_PATH, str(seed)] if GEN_PATH.suffix == ".py" else [GEN_PATH, str(seed)],
                timeout=args.timeout,
            )

            if gen.returncode != 0:
                print(f"Generator error! seed={seed}")
                print(gen.stderr)
                save_failure(seed)
                if not is_continue():
                    return

            input_data = gen.stdout

            # 2. 正解コード
            stage = "ac"
            ac = run(
                [sys.executable, AC_PATH] if AC_PATH.suffix == ".py" else [AC_PATH],
                input_data=input_data,
                timeout=args.timeout,
            )

            if ac.returncode != 0:
                print(f"ac error! seed={seed}")
                print(ac.stderr)
                save_failure(seed, input_data, ac, wa)
                if not is_continue():
                    return

            # 3. 検証対象コード
            stage = "wa"
            wa = run(
                [sys.executable, WA_PATH] if WA_PATH.suffix == ".py" else [WA_PATH],
                input_data=input_data,
                timeout=args.timeout,
            )

            if wa.returncode != 0:
                print(f"wa error! seed={seed}")
                print(wa.stderr)
                save_failure(seed, input_data, ac, wa)
                if not is_continue():
                    return

            # 4. 出力比較（空白・改行の差は無視）
            if ac.stdout.split() != wa.stdout.split():
                print(f"Diff found! seed={seed}")
                prob_dir = save_failure(seed, input_data, ac, wa)

                print("\n--- Input ---")
                print(input_data, end="")
                print("\n--- Expected output ---")
                print(ac.stdout, end="")
                print("\n--- Actual output ---")
                print(wa.stdout, end="")
                print(f"\n\nSaved to {prob_dir}")
                if not is_continue():
                    return

        except subprocess.TimeoutExpired:
            print(f"Timeout! stage={stage}, seed={seed}")
            save_failure(seed, input_data, ac, wa)
            if input_data is not None:
                print("\n--- Input ---")
                print(input_data, end="")
            if not is_continue():
                return

        except OSError as e:
            print(f"Execution error! stage={stage}, seed={seed}")
            print(e)
            save_failure(seed, input_data, ac, wa)
            if not is_continue():
                return

        if (i + 1) % 50 == 0:
            print(f"Passed: {i + 1} last_seed={seed}")

    print(f"All {args.tests} tests passed.")
    print(f"Seeds tested: {args.seed} ... {args.seed + args.tests - 1}")


if __name__ == "__main__":
    main()
