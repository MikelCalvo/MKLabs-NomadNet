#!/usr/bin/env python3

from __future__ import annotations

import filecmp
import os
import shutil
import sys
from typing import Iterable, Tuple


def prompt_yes_no(question: str, default: bool = True) -> bool:
    yes_options = {"y", "yes"}
    no_options = {"n", "no"}
    prompt = "[Y/n]" if default else "[y/N]"

    while True:
        answer = input(f"{question} {prompt} ").strip().lower()
        if not answer:
            return default
        if answer in yes_options:
            return True
        if answer in no_options:
            return False
        print("Please answer with 'y' or 'n'.")


def prompt_path(question: str, default: str) -> str:
    answer = input(f"{question} [{default}] ").strip()
    if not answer:
        return default
    return os.path.expanduser(answer)


def prompt_collision(src: str, dst: str) -> bool:
    rel_dst = os.path.relpath(dst, os.path.expanduser("~"))
    while True:
        print()
        print(f"Collision detected for '{rel_dst}':")
        print(f"- Current file : {dst}")
        print(f"- Project file: {src}")
        choice = input("Keep (c)urrent or use (p)roject file? [c/p] ").strip().lower()
        if choice in {"c", "current"}:
            return False
        if choice in {"p", "project"}:
            return True
        print("Please answer with 'c' or 'p'.")


def iter_files(src_dir: str) -> Iterable[Tuple[str, str]]:
    for root, _, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)
        yield rel_root, root, files


def copy_tree(src_dir: str, dst_dir: str) -> None:
    for rel_root, root, files in iter_files(src_dir):
        target_root = dst_dir if rel_root == "." else os.path.join(dst_dir, rel_root)
        os.makedirs(target_root, exist_ok=True)

        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(target_root, filename)

            if os.path.exists(dst_path):
                try:
                    same = filecmp.cmp(src_path, dst_path, shallow=False)
                except OSError:
                    same = False
                if same:
                    continue
                if not prompt_collision(src_path, dst_path):
                    continue

            shutil.copy2(src_path, dst_path)
            print(f"Copied {src_path} -> {dst_path}")


def chmod_tree(target_dir: str, mode: int = 0o755) -> None:
    if not os.path.isdir(target_dir):
        return

    warnings = []
    for root, dirs, files in os.walk(target_dir):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                os.chmod(path, mode)
            except OSError as exc:
                warnings.append((path, exc))

    if warnings:
        print()
        print("Some files could not be chmodded automatically:")
        for path, exc in warnings:
            print(f"- {path}: {exc}")
        print(
            "You can run this command manually to fix permissions:\n"
            f"  chmod -R {oct(mode)} {target_dir}"
        )


def main() -> int:
    project_root = os.path.dirname(os.path.abspath(__file__))

    default_storage = os.path.expanduser("~/.nomadnetwork/storage")
    storage_root = os.path.abspath(prompt_path("NomadNet storage path", default_storage))
    os.makedirs(storage_root, exist_ok=True)

    pages_src = os.path.join(project_root, "pages")
    scripts_src = os.path.join(project_root, "scritps")

    pages_dst = os.path.join(storage_root, "pages")
    scripts_dst = os.path.join(storage_root, "scripts")

    print()
    print("Setup options:")
    print(f"- Pages source : {pages_src}")
    print(f"- Pages target : {pages_dst}")
    print(f"- Scripts source: {scripts_src}")
    print(f"- Scripts target: {scripts_dst}")
    print()

    if os.path.isdir(pages_src):
        if prompt_yes_no(f"Copy website pages to {pages_dst}?"):
            copy_tree(pages_src, pages_dst)
            chmod_tree(pages_dst, 0o755)
        else:
            print("Skipping pages.")
    else:
        print("Pages directory not found; skipping pages.")

    if os.path.isdir(scripts_src):
        if prompt_yes_no(f"Copy helper scripts to {scripts_dst}?"):
            copy_tree(scripts_src, scripts_dst)
        else:
            print("Skipping scripts.")
    else:
        print("Scripts directory not found; skipping scripts.")

    print()
    print("Setup completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


