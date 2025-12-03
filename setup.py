#!/usr/bin/env python3

from __future__ import annotations

import filecmp
import os
import shutil
import sys
from typing import Iterable, Tuple

from utils.config_loader import get_config


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


def should_skip_file(filename: str, dirpath: str) -> bool:
    if filename.endswith('.pyc'):
        return True
    if '__pycache__' in dirpath:
        return True
    return False


def iter_files(src_dir: str) -> Iterable[Tuple[str, str, list]]:
    for root, _, files in os.walk(src_dir):
        if '__pycache__' in root:
            continue
        rel_root = os.path.relpath(root, src_dir)
        filtered_files = [f for f in files if not should_skip_file(f, root)]
        if filtered_files:
            yield rel_root, root, filtered_files


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


def copy_file(src_file: str, dst_file: str) -> None:
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    
    if os.path.exists(dst_file):
        try:
            same = filecmp.cmp(src_file, dst_file, shallow=False)
        except OSError:
            same = False
        
        if same:
            return
        
        if not prompt_collision(src_file, dst_file):
            return

    shutil.copy2(src_file, dst_file)
    print(f"Copied {src_file} -> {dst_file}")


def chmod_tree(target_dir: str, mode: int = 0o755) -> None:
    if not os.path.isdir(target_dir):
        return

    print()
    print(f"Setting permissions to {oct(mode)} for {target_dir}")
    
    warnings = []
    success_count = 0
    
    for root, dirs, files in os.walk(target_dir):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                os.chmod(path, mode)
                success_count += 1
            except OSError as exc:
                warnings.append((path, exc))

    if warnings:
        print(f"Successfully changed permissions for {success_count} files/directories")
        print("Some files could not be chmodded automatically:")
        for path, exc in warnings:
            print(f"- {path}: {exc}")
        print(
            "You can run this command manually to fix permissions:\n"
            f"  chmod -R {oct(mode)} {target_dir}"
        )
    else:
        print(f"Successfully changed permissions for {success_count} files/directories")


def main() -> int:
    config = get_config()
    default_storage = config.get("nomadnet", "storage_path", default="~/.nomadnetwork/storage")
    
    project_root = os.path.dirname(os.path.abspath(__file__))

    storage_root = os.path.expanduser(
        prompt_path("NomadNet storage path", default_storage)
    )
    storage_root = os.path.abspath(storage_root)
    os.makedirs(storage_root, exist_ok=True)

    pages_src = os.path.join(project_root, "pages")
    scripts_src = os.path.join(project_root, "scripts")
    utils_src = os.path.join(project_root, "utils")
    config_src = os.path.join(project_root, "config.json")

    pages_dst = os.path.join(storage_root, "pages")
    scripts_dst = os.path.join(storage_root, "scripts")
    utils_dst = os.path.join(pages_dst, "utils")
    config_dst = os.path.join(pages_dst, "config.json")

    print()
    print("Setup options:")
    print(f"- Pages source  : {pages_src}")
    print(f"- Pages target  : {pages_dst}")
    print(f"- Scripts source: {scripts_src}")
    print(f"- Scripts target: {scripts_dst}")
    print(f"- Utils source  : {utils_src}")
    print(f"- Utils target  : {utils_dst}")
    print(f"- Config source : {config_src}")
    print(f"- Config target : {config_dst}")
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

    if os.path.isdir(utils_src):
        if prompt_yes_no(f"Copy utils module to {utils_dst}?"):
            copy_tree(utils_src, utils_dst)
        else:
            print("Skipping utils.")
    else:
        print("Utils directory not found; skipping utils.")

    if os.path.isfile(config_src):
        if prompt_yes_no(f"Copy config.json to {config_dst}?"):
            copy_file(config_src, config_dst)
        else:
            print("Skipping config.json.")
    else:
        print("config.json not found; skipping config.")

    print()
    print("Setup completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
