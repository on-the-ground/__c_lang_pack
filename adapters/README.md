# Connect the pack to an Agent

The archive contains `SKILL.md` + modules, `subsea-cable-context.md`, examples,
`pack.json`, `release.json`, and a license. Unpack it into a workspace directory
such as `.agent-context/subsea-cable/`. Verify the file hashes in `release.json`
against the files received; they detect corruption, not publisher authenticity.
Use a trusted distribution channel or verify a publisher-provided archive digest.

For a workspace Agent, add the contents of
[AGENTS.snippet.md](AGENTS.snippet.md) to its applicable instruction file and
adjust the directory path if needed. Codex-style hosts commonly read `AGENTS.md`;
Claude Code uses `CLAUDE.md`. Preserve existing instructions. The snippet loads
only a short entry and selects deeper modules when needed. Merely unpacking a
nested directory does not make an Agent read it.

For a host that supports Agent Skills, install the folder using that host's
actual skill installation mechanism and confirm discovery of `SKILL.md`.
Discoverability does not mean the skill is always loaded. If Subsea Cable is the
workspace's default workflow language, keep an explicit instruction-file entry.

For a retrieval or prompt-context host, attach `subsea-cable-context.md` and
provide the remaining modules/examples on demand. The compact artifact has a
build-enforced byte budget; it is not a measured tokenizer-specific token count.

The production workspace/bootstrap should install the pinned pack and its
instruction-file entry by default, and record `release.json` with the deployment.
This initial pack supplies the artifact and connection instructions; it does not
change any Agent host's defaults or install itself.

Language knowledge and MCP connectivity are independent. Connect an actual
Runtime separately and inspect the tools it exposes. This pack registers no MCP
server and promises no general Plan execution tool. Read the workflow module's
availability section before running a plan. A deployment should verify that the
Agent can discover the entry, explain routing, report real validator diagnostics,
and use supported execution/revision operations before declaring integration ready.
