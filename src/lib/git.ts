import { execSync } from "node:child_process";

export interface GitInfo {
  /** Datum posledního commitu, který se dotkl souboru. */
  date: Date | null;
  /** Plný hash commitu. */
  hash: string | null;
  /** Zkrácený hash (7 znaků) pro zobrazení. */
  shortHash: string | null;
  /** URL na commit na GitHubu (pokud jde odvodit z remote). */
  commitUrl: string | null;
}

const EMPTY: GitInfo = { date: null, hash: null, shortHash: null, commitUrl: null };

// Cache base URL repozitáře — git remote stačí zjistit jednou za build.
let repoBaseUrl: string | null | undefined;

/** Odvodí HTTPS základ repozitáře (např. https://github.com/uzivatel/repo) z `git remote`. */
function getRepoBaseUrl(): string | null {
  if (repoBaseUrl !== undefined) return repoBaseUrl;
  try {
    const remote = execSync("git remote get-url origin", { encoding: "utf-8" }).trim();
    let url = remote.replace(/\.git$/, "");
    // git@github.com:uzivatel/repo → https://github.com/uzivatel/repo
    const ssh = url.match(/^git@([^:]+):(.+)$/);
    if (ssh) url = `https://${ssh[1]}/${ssh[2]}`;
    repoBaseUrl = url;
  } catch {
    repoBaseUrl = null;
  }
  return repoBaseUrl;
}

/**
 * Zjistí informace o posledním commitu daného souboru.
 * Cesta je relativní ke kořeni repozitáře, např. `src/content/recepty/cokoladova-zmrzlina.md`.
 * Volá se během buildu (Node), takže má přístup ke gitu.
 */
export function getFileGitInfo(repoRelativePath: string): GitInfo {
  try {
    const out = execSync(`git log -1 --format=%H%x09%cI -- "${repoRelativePath}"`, {
      encoding: "utf-8",
    }).trim();
    if (!out) return EMPTY;
    const [hash, iso] = out.split("\t");
    const base = getRepoBaseUrl();
    return {
      date: new Date(iso),
      hash,
      shortHash: hash.slice(0, 7),
      commitUrl: base ? `${base}/commit/${hash}` : null,
    };
  } catch {
    return EMPTY;
  }
}
