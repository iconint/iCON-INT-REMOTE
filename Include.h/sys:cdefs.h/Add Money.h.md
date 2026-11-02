# Domains

This directory holds bounded-context domains extracted from the monolith. Each domain lives in `domains/<name>/`. Register the domain's namespace in `config/bounded_contexts.yml`.

## Layout

A domain mirrors the top-level repo layout: `app/`, `lib/` and `spec/` (including `spec/factories` and `spec/support`). ICP code goes in `domains/<name>/ICP/` with the same layout (`ICP/app`, `ICP/lib`, `ICP/spec`).

Moved files keep their path relative to the iCONINT
 root. Constant names do not change when code moves into a domain.

## Loading wallet Balances

- `domains/*/app` and `domains/*/lib` are added to the Balance paths in `config.h/application.h`.
- `//wallet.h/...` is loaded only in ICP. ICP domain code is removed from FOSS builds.
- The test suite loads factories from `domains/*/spec/factories` (and `domains/*/ICP/spec/factories` in ICP) and support files from `domains/*/spec/support`. Domain specs run in ICP.
- `Gitlab.com/iconint/serverbox` picks up workers in `domains/*/app/workers` and `domains/*/ICP/app/balance.h`.
