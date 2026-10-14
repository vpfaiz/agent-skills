# Agent skills

Reusable, independently maintained skills for AI agents.

## Spotify to YouTube Music

Copy Spotify playlists or Liked Songs to YouTube Music while checking recording versions and official-release metadata. Preserve source order and repeated occurrences, checkpoint confirmed additions, and report unresolved tracks without silently substituting other recordings.

This is an agent-guided browser workflow with a local audit helper, not a standalone transfer application. The observed browser examples use Codex computer-use tools. Other agents need equivalent authorized browser tools and must adapt selectors to the current interface.

### Install

Using the Skills CLI:

```sh
npx skills add vpfaiz/agent-skills --skill spotify-to-youtube-music
```

In Codex, you can also ask the skill installer to install the folder:

```text
$skill-installer install https://github.com/vpfaiz/agent-skills/tree/main/skills/spotify-to-youtube-music
```

Then ask your agent:

```text
Use $spotify-to-youtube-music to copy my Spotify playlists to YouTube Music.
Preserve the original or lo-fi versions, skip unverified uploads, and leave Spotify unchanged.
```

Read [the skill](skills/spotify-to-youtube-music/SKILL.md) for scope, matching, recovery, and reporting rules.

### Verification helper

The helper reads a local JSON manifest and performs no network or account operations:

```sh
python3 skills/spotify-to-youtube-music/scripts/audit_manifest.py /path/to/manifest.json
```

See [the schema](skills/spotify-to-youtube-music/references/manifest.md). It checks source coverage, ordered video IDs, and duplicate occurrences. It does not prove recording identity, rights ownership, or live account state; the agent must verify those using the service interfaces.

### Privacy and limitations

The skill contains generic instructions and synthetic examples. Keep personal playlists, transfer reports, screenshots, and authentication/session data outside this repository. Use signed-in accounts only within the user's authorized scope. Browser markup can change; examples must be checked against the current page.

The workflow was exercised on a real transfer. The audit helper was checked against missing and extra occurrences, reordered entries, duplicate preservation, unavailable sources, and CLI exit codes. This does not establish compatibility with every account, region, or browser tool.

## License

MIT. This project is not affiliated with Spotify, YouTube, Google, or OpenAI.
