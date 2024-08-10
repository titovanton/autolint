import subprocess


def get_stdout_with() -> int:
    result = subprocess.run(
        "stty size | cut -d' ' -f2",
        shell=True,
        capture_output=True,
        text=True
    )

    return int(result.stdout.strip())


def run_linter(command: list[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
