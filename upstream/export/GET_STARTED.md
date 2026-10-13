# Get Started: run a Subsea Cable example through your Agent

> **Checked:** 2026-10-11 (Asia/Seoul) with Claude Code on Windows.
> This is a demo of one reference example, not an installable Runtime release.

Connect your Agent to a small Docker image. Then ask in plain words. The Agent
runs a real Voyage Plan that finds the prime numbers up to a limit. It shows you
the actual result and explains the plan from its code.

You do not need to learn a command set, build anything, or start a server. You
add one MCP server entry, and the Agent does the rest.

## What you need

- **Docker**, running. On Windows and macOS, start Docker Desktop.
- **An Agent that can use a local MCP server over stdio.** This page shows
  Claude Code and Codex; any MCP client that can run a command works.
- **Internet access once**, to download the image (about 50 MB).

The image is built for `linux/amd64`. On Arm machines such as Apple silicon,
Docker runs it through emulation. That path has not been checked yet and may
start more slowly.

## 1. Download the image

```sh
docker pull ghcr.io/on-the-ground/subsea-cable-mcp:latest
```

Downloading first keeps the Agent's first start short. Otherwise the download
happens while the Agent waits for the server, and it can run out of time. If
you downloaded the image before, run the same command again to get the current
version.

## 2. Connect your Agent

The server needs a few seconds to start its bundled Host. The settings below
allow up to two minutes.

### Claude Code

Add the server for your user, so it is available in every folder:

```sh
claude mcp add --scope user subsea-cable -- docker run -i --rm ghcr.io/on-the-ground/subsea-cable-mcp:latest
```

Start Claude Code with a longer MCP startup timeout. In macOS or Linux shells:

```sh
MCP_TIMEOUT=120000 claude
```

In Windows PowerShell:

```powershell
$env:MCP_TIMEOUT = "120000"
claude
```

Type `/mcp` in Claude Code to confirm that `subsea-cable` is connected.

### Codex

Add this to your user configuration file, `~/.codex/config.toml`. On Windows,
the default path is `%USERPROFILE%\.codex\config.toml`:

```toml
[mcp_servers.subsea-cable]
command = "docker"
args = ["run", "-i", "--rm", "ghcr.io/on-the-ground/subsea-cable-mcp:latest"]
startup_timeout_sec = 120
```

Save the file, then restart Codex. If you use the IDE extension, restart the
extension.

If you have the Codex CLI installed, check that the server is registered:

```sh
codex mcp list
```

This command lists configured servers. To confirm an active connection, start
Codex CLI and type `/mcp`. Check that `subsea-cable` is connected before asking
for the example.

### Other Agents

Register a stdio server that runs `docker` with the arguments
`run -i --rm ghcr.io/on-the-ground/subsea-cable-mcp:latest`, and allow about two
minutes for startup.

## 3. Ask your Agent

Start with:

> Run the Subsea Cable primes example up to 30.

The Agent runs the example and answers with the actual result:
`2, 3, 5, 7, 11, 13, 17, 19, 23, 29`.

Then keep asking, in any language:

| Ask | What happens |
|---|---|
| "How did it solve that?" | The Agent reads the Voyage Plan used for the run and explains it with the result |
| "What does `Divides` do?" | The Agent explains one part of the plan |
| "Now try 50." | The Agent sends a new input to the same run and shows that result |
| "Close it." | The Agent stops accepting inputs and confirms that everything finished |

## What you are looking at

The [Voyage Plan](conformance/valid/primes-up-to-by-trial-division.vyg) is the
whole program. Two Goals carry most of the idea:

```subsea
CheckPrime = [n, divisor] -1> [
    PastSquareRoot[n, divisor],
    [finished] -> [
        finished,
        { true: Keep[n], false: CheckDivisibility[n, divisor] },
    ],
]

Gather = [limit, candidate] -1> {
    head: CheckPrime[candidate, 2],
    rest: NextCandidate[limit, candidate],
}
```

`CheckPrime` chooses one branch from a condition and recurses through
`CheckDivisibility` until the divisor passes the square root. `Gather` names two
independent pieces of work: test the current candidate, and continue with the
next candidate. Small functions such as `Divides` and `Next` are leaves that
the bundled Host evaluates.

When you ask for a run, the Agent opens a **Cable** for the plan's root Goal
and sends your limit as an input. It reads the result, and the input's
completion signal tells it that the input is finished. The Cable stays open for
more inputs until you ask the Agent to close it. Accepted inputs still finish
after closing. Ending the Agent session instead also closes the Cable, but an
input still running at that moment may not finish.

The result is one completed map, not a stream of separate numbers. Each
candidate has a `head`, either `{prime: n}` or `{}`, and a `rest` holding the
next candidate. The Agent reads the primes by walking that map.
[Primes Up To](conformance/PRIMES_UP_TO.md) describes the result shape, and
[The Subsea Cable World](METAPHORS.md) explains the terms.

## What this demo covers

- It runs only this example, with integer limits from 1 to 100. The limit is a
  demo restriction, not a language rule.
- You cannot run your own Voyage Plan with it yet. The Agent can help you draft
  one, but not run it.
- Explanations come from the plan code and the actual result. The demo shows
  no step-by-step execution trace.
- The container needs no network and keeps nothing. Cables and results end
  with the Agent session.
- It runs a prototype implementation. [Runtime availability](RUNTIME_STATUS.md)
  records what is and is not supported.

## If something goes wrong

| Symptom | What to do |
|---|---|
| The Agent reports that the server failed to start or timed out | Download the image first (step 1) and allow two minutes for startup |
| PowerShell says `MCP_TIMEOUT=120000` is not recognized | Use the PowerShell form `$env:MCP_TIMEOUT = "120000"` |
| Docker reports that it cannot connect to the daemon | Start Docker Desktop and try again |
| `subsea-cable` is missing in another folder | Add it with `--scope user`, as shown above |

To remove the demo later, run `claude mcp remove subsea-cable` (or delete the
Codex entry), then `docker rmi ghcr.io/on-the-ground/subsea-cable-mcp:latest`.

## Next steps

- Sketch one of your own workflows with the [adoption guide](ADOPTION.md) and
  [For Agents](FOR_AGENTS.md).
- Read the [Language Reference](LANGUAGE_REFERENCE.md) for the constructs used
  in this plan.
- Tell us where you got stuck, or what felt useful, through
  [Contributing](CONTRIBUTING.md).
