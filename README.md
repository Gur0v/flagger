# flagger

`flagger` is a harder-edged fork of upstream `flaggie`.

Same basic job:

- edit Gentoo `package.*` config entries from command line

Main fork changes from upstream:

- project/package name is now `flagger`
- installed command is now `flagger`
- `--version` prints `flagger <version>`
- when config lives in directory form such as `package.use/`, writes go only to
  `99local.conf`
- sibling config files in `package.use/`, `package.accept_keywords/`, and other
  `package.*` dirs are left alone
- if local Python package-manager integration fails, `flagger` falls back to
  system `python3` + system `gentoopm` when possible
- this makes auto type guessing work better for `uv tool install` setups on
  Gentoo

Why this fork exists:

- keep machine-managed changes in one predictable file
- stop touching hand-maintained config fragments
- work better with isolated tool installs

What did not change:

- internal Python module path is still `flaggie`
- direct single-file configs like `/etc/portage/package.use` still work
- normal flag editing behavior stays same

## Install on Gentoo

1. Install `uv`:

```bash
sudo emerge -av dev-python/uv app-portage/gentoopm
```

2. Install this repo as a tool:

```bash
cd ~/flaggie
uv tool install --with gentoopm .
```

3. If command is not found, add local bin dir to `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

4. Verify:

```bash
flagger --version
flagger --help
```

## Update after local changes

```bash
cd ~/flaggie
uv tool install --force --with gentoopm .
```

## Examples

Explicit namespace:

```bash
flagger media-video/pipewire +use::sound-server
```

Auto type guessing:

```bash
flagger pipewire +sound-server
```

If package-manager integration inside local tool env breaks, `flagger` tries to
query the system Gentoo Python environment instead.

## Behavior in config dirs

Given a directory like:

```text
/etc/portage/package.use/
```

`flagger` will:

- create `99local.conf` if missing
- read and write `99local.conf`
- not pick some other existing file
- not modify sibling files in that directory

This is deliberate.

## Upstream

Original project:

- <https://github.com/gentoo/flaggie>
