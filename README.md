# flagger

`flagger` is a Gentoo-focused fork of upstream `flaggie`.

It still edits Portage `package.*` config from the command line, but this fork
is stricter, more predictable, and much nicer to use on a real Gentoo system.

## What changed from upstream

- user-facing project name is `flagger`
- installed command is `flagger`
- `--version` prints `flagger <version>`
- when a `package.*` config is a directory, `flagger` writes only to
  `99local.conf`
- sibling config files are never edited
- when installed with `uv`, `flagger` can still use system `gentoopm` for auto
  type guessing
- on real `/etc/portage` runs, `flagger` auto-reexecs itself through `doas` or
  `sudo` if needed

## Why this fork exists

- keep machine-managed changes in one predictable file
- avoid touching hand-maintained config fragments
- make isolated installs work well on Gentoo
- remove extra friction from normal day-to-day use

## Install on Gentoo

Install dependencies:

```bash
sudo emerge -av dev-python/uv app-portage/gentoopm
```

Install `flagger` from this checkout:

```bash
cd ~/flagger
uv tool install --with gentoopm .
```

If `flagger` is not in `PATH` yet:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Verify:

```bash
flagger --version
flagger --help
```

## Update after local changes

```bash
cd ~/flagger
uv tool install --force --with gentoopm .
```

## Normal usage

You can usually just run it directly:

```bash
flagger pipewire +sound-server
flagger pipewire +~amd64
```

If you are operating on the real `/etc/portage`, `flagger` will invoke
`doas` or `sudo` itself when needed. You do not need to start it with
`sudo flagger ...`.

If you are working against another root, pass `--config-root` explicitly:

```bash
flagger --config-root /tmp/testroot pipewire +sound-server
```

## Directory behavior

If Portage config uses directory layout, for example:

```text
/etc/portage/package.use/
```

`flagger` will:

- create `99local.conf` if missing
- read and write `99local.conf`
- leave every sibling file alone

This applies to other `package.*` directories too, such as:

- `package.accept_keywords/`
- `package.license/`
- `package.properties/`
- `package.accept_restrict/`
- `package.env/`

## Notes

- internal Python module name is still `flaggie`
- direct single-file configs like `/etc/portage/package.use` still work
- if auto type guessing cannot determine a namespace, you can still force one
  with forms like `+use::sound-server` or `+kw::~amd64`

## Upstream

Original project:

- <https://github.com/gentoo/flaggie>
