# Remote CLI Requirements

## Goal

Provide Crawl4AI CLI access to a remote Crawl4AI HTTP API without requiring
Playwright, browsers, or other local crawling dependencies.

## Change discipline

- Change only files required to implement, test, or document this feature.
- Preserve unrelated files byte-for-byte, including formatting and trailing
  newlines, to keep reviews and pull requests focused.

## Command compatibility

- Preserve the existing local `crwl` behavior.
- Provide the standalone `crwl-remote ...`.
- Support aliasing `crwl` to `crwl-remote` for backend-agnostic scripts and
  agent workflows.
- Do not provide Docker-specific command names; the API may be hosted anywhere.

## Lightweight installation

- Support `pip install --no-deps 'crawl4ai[crwl-remote]'`.
- The remote command must use only the Python standard library before
  dispatching a request.
- Remote operation must not import or install local browser/crawler libraries.

## Credentials

- Provide `crwl-remote config` to save credentials globally in
  `~/.crawl4ai/remote.json`.
- Store the credential file with user-only (`0600`) permissions.
- Resolve credentials in this order:
  1. `--api-url` / `--api-token`
  2. `CRAWL4AI_API_URL` / `CRAWL4AI_API_TOKEN`
  3. The global credential file
- Never print, log, or commit API or proxy credentials.

## Crawl configuration

- Support browser and crawler configuration files and inline scalar overrides.
- Support existing output formats and output files.
- Support deep-crawl options.
- Support authenticated browser proxy configuration, including proxy server,
  username, and password.

## Proxy authorization and safety

- Treat the static `CRAWL4AI_API_TOKEN` as an admin/operator credential.
- Trust browser and crawler configuration supplied by callers authenticated
  with the admin token, including proxy configuration.

## Agent skill

- Include a repository skill that invokes only `crwl`.
- Keep the skill compatible with local `crwl` and a shell alias to
  `crwl-remote`.

## Upstream synchronization workflow

- Include a GitHub Actions workflow that runs weekly and supports manual
  dispatch.
- Synchronize the fork's `crwl-remote` branch with
  `https://github.com/unclecode/crawl4ai.git` branch `main`.
- Push a clean upstream merge directly to the fork's `crwl-remote` branch,
  then merge `crwl-remote` into the default `auto-fix-workflow` branch.
- Keep `auto-fix-workflow` a strict superset of `crwl-remote` containing only
  workflow-specific changes beyond the maintained Crawl4AI branch.
- Treat upstream fetch failures, merge conflicts, and push failures as sync
  problems that require repair by LangChain Deep Agents.
- Run the workflow in the `actions-env` GitHub Environment so it can access
  environment-scoped model-provider secrets.
- Allow the model to be selected with the `DEEP_AGENT_MODEL` repository
  variable and default to `openai:gpt-5.6-sol`.
- Before changing a failed sync, the Deep Agent must read this document in full
  and treat every requirement in it as an acceptance criterion.
- When upstream changes conflict with these requirements, preserve the
  fork-specific remote CLI behavior required by this document.
- Require the Deep Agent to run focused validation and verify its completed
  repair against this document.
- Do not allow the Deep Agent to push, create pull requests, rewrite history,
  or force-push itself.
- Publish a resolved agent repair on a dedicated branch as a pull request
  against the branch whose synchronization failed for human review; never let
  an agent repair write directly to either maintained branch.
- Grant the workflow only the GitHub permissions it needs to update repository
  contents and create pull requests, prevent overlapping sync runs, and pin
  third-party actions to commit SHAs.

## Acceptance criteria

- Unit and security suites pass without weakening existing security posture.
- Build the modified backend as a Docker/OCI container.
- Run the API with an admin credential.
- Send two `crwl-remote` requests to `https://ipv4.webshare.io` through a
  rotating proxy.
- Both requests must succeed and return different public IP addresses.
- Browser execution for acceptance testing must occur only inside the
  container; no local Playwright or browser installation is permitted.
