import { walk } from "https://deno.land/std/fs/mod.ts";
import { join, dirname } from "https://deno.land/std/path/mod.ts";
import { entropyToStratum, getRepoRoot } from "./TS/m32/sigma.ts";

async function migrate() {
  const root = getRepoRoot();
  const mdDir = join(root, "MD");

  console.log(`🐌 Starting Raukuška Migration in ${mdDir}...`);

  for await (const entry of walk(mdDir, { includeDirs: false })) {
    if (!entry.path.endsWith(".md")) continue;

    const folderName = dirname(entry.path).split("/").pop();
    let entropy = 0;
    if (folderName?.startsWith("p")) {
        const bucket = parseInt(folderName.substring(1));
        entropy = bucket * 1024;
    } else if (folderName?.startsWith("m")) {
        const bucket = parseInt(folderName.substring(1));
        entropy = -bucket * 1024;
    }

    if (entropy === 0 && folderName !== "z00") continue;

    const newStratum = entropyToStratum(entropy);
    const newPath = join(root, "MD", newStratum, entry.name);

    if (entry.path === newPath) continue;

    console.log(`   Migration: ${folderName} -> ${newStratum} | ${entry.name}`);
  }

  console.log("\n✅ Raukuška Migration Dry-Run Complete.");
}

if (import.meta.main) {
  migrate();
}
