---
type: imported-note
title: Gallica MCP Evaluation Report
source_path: /Users/ana/Documents/Claude/Projects/PHD/gallica_mcp_evaluation_report.md
status: active
created: 2026-04-15
---

# Gallica MCP Evaluation Report

## Summary

The report documents a mixed result set for the Gallica MCP server:

- some search and URL construction flows pass
- some metadata and IIIF calls are blocked by connectivity or endpoint limits
- compound CQL search is a known implementation bug

## Useful takeaways

- broaden iconography queries beyond a single controlled term when coverage is empty
- document the endpoint limitations explicitly
- do not assume IIIF or OAI access is stable for all ARKs

## Why useful

This is a direct operational reference for archive work and search fallback design.
