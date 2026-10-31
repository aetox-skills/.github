<div align="center">
  <img src="https://avatars.githubusercontent.com/u/290514512?v=4" width="96" alt="Aetox Skills logo">

  <h2>Aetox Skills</h2>

  <p><strong>AI agent skills from Aetox — one behaviour package per moment where a fast agent gets it wrong.</strong></p>

  <p>Writing code and checking code are two different skills here, and both were measured.</p>
</div>

---

> **93.3% / 97.8% secure code on CWEval** with [`aetox-security`](https://github.com/aetox-skills/aetox-security) switched on, against **68.9% / 77.8%** for the next-best harness without it — 11 tasks × 2 OpenAI models × 3 rounds, hidden tests, the same model both ways.
> Method, reports and raw runs: [Mikedev115/Aetox-Harness](https://github.com/Mikedev115/Aetox-Harness).

## The pair

| Skill | When | What it does |
|:--|:--|:--|
| [`aetox-security`](https://github.com/aetox-skills/aetox-security) | the code is being written | Names the weakness each unit takes in (CWE id and name), takes the standard defense, keeps the contract the code promised, then runs the attack and an input the contract accepts. |
| [`aetox-security-audit`](https://github.com/aetox-skills/aetox-security-audit) | the code already exists | A threat model first, then read-only hunters per unit, a critic that names the units nobody covered, and fresh verifiers that try to refute every finding. Two sizes: a diff answered in the chat, or a whole project with a run folder. |

<sub>Split at the verb on purpose, so the review rules never leak into the writing pass.</sub>

## The rest of the family

| Skill | When |
|:--|:--|
| [`senior-architect-agent`](https://github.com/aetox-skills/senior-architect-agent) | An agent is about to work in a system it did not write: boundaries, risks, handoff notes. |
| [`idea-to-architecture-agent`](https://github.com/aetox-skills/idea-to-architecture-agent) | There is a raw idea and no code: questions first, then a reviewable architecture proposal. |
| [`docstruct`](https://github.com/aetox-skills/docstruct) | Documentation has started duplicating itself: one source of truth, less of it. |
| [`deep-study`](https://github.com/aetox-skills/deep-study) | Something has to be understood properly, not skimmed: a textbook-depth pass over a repo, concept, paper or system. |
| [`create-agent`](https://github.com/aetox-skills/create-agent) | An agent is about to be built: the scope is decided before anything else. |

## Install

```bash
plugin_install("https://github.com/aetox-skills/aetox-security")
```

Or copy `SKILL.md` and `references/` beside it into your agent's skill folder. Every repository carries `README.md`, `INSTALL.md` and `CHANGELOG.md`, and the agents that read these files are not one vendor's — the steps that need a specific tool name say so in the skill itself.

## One name, one skill

A skill's name is its repository name: `aetox-security` lives at `aetox-skills/aetox-security`. There is no second name for anything on this page — if you are told a skill here is called something this page and the [catalog](https://github.com/aetox-skills/aetox-skills) do not list, that name is a guess. The catalog is the one index; it carries what each skill is for, when not to use it, and its current status.

## Numbers

Every figure stated in this organization names the model it was measured on and the test that produced it, and links the report. A skill with no such figure says so instead of implying one — a measured claim you cannot check is worse than no claim.

## Built By

Mike at Aetox, an independent AI systems lab in Thailand.
[Website](https://aetox.vercel.app/th) · [Catalog](https://github.com/aetox-skills/aetox-skills) · [Skill template](https://github.com/aetox-skills/skill-template)
