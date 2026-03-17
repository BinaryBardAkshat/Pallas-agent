# Sandbox Backends

## What it does

Sandbox backends control where terminal commands are executed. By default Pallas runs commands locally via `subprocess`, but you can redirect execution to a Docker container, a remote SSH host, or Modal serverless infrastructure — without changing any tool code.

## How to configure it

Set the `PALLAS_SANDBOX` environment variable in `.env`:

```env
PALLAS_SANDBOX=local    # default — runs commands on the host machine
PALLAS_SANDBOX=docker   # runs commands in an ephemeral Docker container
PALLAS_SANDBOX=ssh      # runs commands on a remote SSH host
PALLAS_SANDBOX=modal    # runs commands on Modal serverless
```

The `TerminalTool` automatically picks up the configured backend on startup via `get_backend()` in `tools/sandbox_backends/__init__.py`.

## Backends

### Local (default)

No setup required. Uses `subprocess.run(command, shell=True, timeout=120)`.

**Pros**: Zero setup, full host access.
**Cons**: No isolation — destructive commands affect the host.

### Docker

Runs each command in a fresh ephemeral container (`--rm`). The workspace directory is mounted as a volume.

```env
PALLAS_SANDBOX=docker
DOCKER_IMAGE=python:3.11-slim
DOCKER_WORKSPACE=/path/to/project
```

**Requires**: Docker installed and running.
**Pros**: Strong isolation, reproducible environment.
**Cons**: ~1-2s startup per command.

### SSH

Executes commands on a remote host via SSH. Uses paramiko if installed, otherwise falls back to the ssh subprocess.

```env
PALLAS_SANDBOX=ssh
SSH_HOST=dev.example.com
SSH_PORT=22
SSH_USER=ubuntu
SSH_KEY_PATH=~/.ssh/id_rsa
```

### Modal

Runs on Modal serverless infrastructure.

```env
PALLAS_SANDBOX=modal
MODAL_TOKEN_ID=ak-...
MODAL_TOKEN_SECRET=as-...
```

## Tradeoffs

| Backend | Isolation | Speed   | Setup         | Cost         |
|---------|-----------|---------|---------------|--------------|
| Local   | None      | Fastest | None          | Free         |
| Docker  | Container | Fast    | Docker install| Free         |
| SSH     | Remote    | Medium  | SSH keys      | Server cost  |
| Modal   | Serverless| Slowest | Modal account | Pay-per-use  |

All backends enforce a 120-second timeout and return (stdout, stderr, exit_code). The backend name is logged in the trajectory for debugging.

## Adding a new backend

Create `tools/sandbox_backends/mybackend.py` implementing `SandboxBackend`, then register it in `get_backend()` in `tools/sandbox_backends/__init__.py`.
