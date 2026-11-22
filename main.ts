import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point: hand in the front page that is already drawn and committed
// beside this file as entry.png (clean v1-style grid + restrained pseudo-3D
// depth: deep panel shadows, layered Hormuz tankers, document tag — built
// 2026-11-22). Nothing is spawned, nothing reads the clock — the program
// only copies that one file, byte for byte, into the output directory.
const out = process.env.MAKEFUN_OUTPUT_DIR || "out";
mkdirSync(out, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(out, "entry.png"));
