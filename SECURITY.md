# Security policy

## Reporting a vulnerability

Use GitHub private vulnerability reporting on this repository (Security tab
> "Report a vulnerability"). Please do not open public issues for
exploitable findings. You will get an acknowledgment within 72 hours.

## Scope

The installers (`install/`), the git hook (`hooks/`), the gates (`gates/`)
and the embodiment adapters (`embodiment/`) run on contributor machines:
anything that lets a crafted agent card, wiki atom, or CSV rule row execute
unintended code or write outside the repository is in scope. The YAML-subset
parser (`gates/_lib.py`) processes untrusted card content and is in scope.

## Hardening notes for users

- The one-line installers clone the `main` branch. For a reproducible,
  auditable install, clone a tagged release and run `install/install.sh`
  (or `.ps1`) from it instead of piping the bootstrap.
- `embodiment.launch` is validated against shell metacharacters by
  `gate_schema` and re-validated by `embody.py`; adapters escape identity
  strings anyway (defense in depth).

## Supported versions

Only the latest release and `main` are supported.
