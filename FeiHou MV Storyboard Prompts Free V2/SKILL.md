---
name: feihou-mv-storyboard-prompts-free
description: Build a reference-driven MiniMax H3 storyboard for music videos, interviews, and scripted digital presenters from supplied audio/scripts and existing images. Use for H3 prompts and production pages when timing and references are sufficient.
---

# FeiHou MV Storyboard Prompts Free

Create a practical, reference-driven AI video production package from the user's existing audio, timing evidence, locked script or lyrics, and supplied visual references. This edition creates visual plans and H3 prompts only. It does not write lyrics or create missing reference images.

## Scope and Free-Edition Boundaries

Use this edition for MiniMax H3 Ref2VA planning when the supplied images already cover the required performers, vehicles, locations, props, creatures, and visual states.

- Use user-provided lyric/script timings as the timing source. When no reliable audio timing is supplied, inspect available audio/manual evidence and label unverified cuts as provisional.
- Build a global `P#` reference register from supplied files only. New user-supplied images may be added to that register after inspection.
- Do not generate, request, or write prompts for supplementary asset images, character cards, environments, props, vehicle variants, or VFX cards.
- If precise sentence-level alignment is required and has not been supplied, state that the user needs to provide or approve an external timing source before audio-locked cuts can be claimed.

Treat supplied lyrics and dialogue as locked source material. Never rewrite, extend, translate, or replace them unless the user explicitly requests it.

## Route the Production Type Before Planning

- **Music video (MV):** a song, lyrics, musical performance, dance, or music-led narrative drives the timing. Apply the MV timing and performance rules in this skill.
- **Digital presenter / spoken video:** a visible person delivers a tutorial, explanation, interview, commentary, or narration. Before planning, read [references/digital-presenter-workflow.md](references/digital-presenter-workflow.md). Speech cadence and visible interaction with the supplied environment drive the shot plan; do not import MV-only singing, dance, lyric-card, beat, or score assumptions.
- **Hybrid:** if music and speech both drive material parts of the cut and the priority is unclear, ask the user whether it is music-led or speech-led.

Both routes share the official H3 structure, the actual supplied-image register, local `P# → <Picture N>` mapping, locked wording, concrete actions and cuts, and the standalone `<Audio N>` reference contract. Keep route-specific rules separate.

## MiniMax H3 Official Prompt Foundation — Non-Negotiable

The complete official MiniMax H3 skills snapshot is bundled at `references/minimax-h3-official-skills/`, sourced from `https://github.com/MiniMax-AI/MiniMax-H3` commit `d21241f0a4b3acbb34c97dae47fa417b7065e438`. It is the authoritative foundation for every H3 prompt written by this skill. All Free-edition workflow, storyboard, cinematography, reference-register, and HTML conventions apply only inside that official framework; they may not change official modes, fields, labels, section order, timing notation, or audio semantics.

### Mandatory routing

1. Default to `references/minimax-h3-official-skills/h3-prompt-writing/SKILL.md`. Read its `references/base-en.txt` for T2VA/I2VA/FL2VA/L2VA or its `references/ref-en.txt` for Ref2VA before drafting.
2. Use Ref2VA when reference images, videos, or audio are uploaded. Preserve exactly: `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`.
3. Detect whether the request materially matches an official scene-specific skill: `3d-animation-short-generator`, `brand-promo-video-generator`, `co-op-game-intro-generator`, `handdrawn-live-video-generator`, `minimalist-product-ad-generator`, `music-video-subtitle-generator`, `paper-collage-explainer-generator`, or `papercraft-stop-motion-explainer`.
4. If a scene-specific skill appears relevant, name it and explain why, then obtain user confirmation before switching. Never silently replace the generic H3 foundation; once confirmed, use the specialized skill alongside `h3-prompt-writing`.

### Official audio-reference contract

- `<Audio N>` is a standalone audio label, never content nested inside `<Subject N>` and never one of the nine visual-picture slots.
- For a presenter’s voice reference, define it as a separate `subject_definitions` entry and bind the speaker: `<Audio 1> is the voice-timbre reference for <Subject 1> (S1), sourced from “filename.mp3”.`
- Use `[reference generation + audio reference]` in `summary` for timbre-only guidance; use `[reference generation + audio reuse]` only when the source signal is copied.
- In `retention_analysis`, record `<Audio N>: reference` for timbre/delivery, `fully_copy` or `partially_copy` for reused signal, or `weak_reference` only for broad similarity.
- Cite `<Audio N>` in `detailed_description` at its actual speech/audio role. Keep dialogue in `<d>[Language] ...</d>`; reserve `non_diegetic_music` for audience-only music.
- Keep project audio assets in `audio_references` using stable `A#` IDs, and map each `A#` explicitly to its H3-local `<Audio N>` label.

## Timing and Shot Design

1. Inspect the complete supplied audio or timing evidence before making cuts. Respect user-given cue times as hard constraints.
2. Keep each complete lyric or spoken line inside one shot. Use `MM:SS:ddd` ranges normalized to 0.1 seconds when verified timing exists; derive duration from the same boundaries in every page and audio label.
3. Confirm the visible performance ratio before planning when singers, dancers, speakers, or interviewees appear on camera. Balance performance against narrative, action, scenery, or other requested content.
4. Match visual change to vocal entrances, line endings, pauses, drops, silence, music peaks, dialogue beats, and the requested story logic. Do not use mechanically uniform durations.
5. Classify every transition as continuous or a hard cut. A continuous successor begins with the exact prior terminal frame; a hard cut declares a new composition, lens/axis, lighting premise, and main movement.

## Supplied-Reference Register and MiniMax H3

Assign every supplied usable image a stable global `P#` ID. Inspect the actual file before naming or describing it. `P#` is project-global; `<Picture N>` is local to one H3 generation unit.

MiniMax H3 accepts at most nine visual images per unit. Choose the ordered upload list first, then map its first image to `<Picture 1>`, second to `<Picture 2>`, and so on. Define every uploaded image inside a relevant `subject_definitions` entry, for example `<Subject 1> is the performer in <Picture 1> (P1), ...`.

Use short canonical names consistently from `subject_definitions` through the prompt body. In English copy-ready Ref2VA prompts, use exactly this field order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Define every referenced audio file as its own `<Audio N>` line in `subject_definitions`, bind it to the corresponding speaker `(Sx)` where applicable, use the matching official task prefix in `summary`, and give it an official audio relationship marker in `retention_analysis`.

Write `detailed_description` in coherent chronological prose:

1. image texture and motivated lighting: key direction/quality, fill, reflection, rim/separation and exposure;
2. composition and principal action: focal-length lens, camera position, screen placement, existing environment and main action;
3. complete visible performance, dialogue, choreography, narrative or combat progression with camera movement tied to the action;
4. a concrete terminal frame.

For visible singing or speech, name the performer and use only the exact line in that unit within `<d>[Language] ...</d>`. For action, specify attacker/defender route, contact or defense, result, environmental reaction, camera response, and end state. Use internal `[Shot N] At MM:SS.mmm` only when an internal cut or complex cue genuinely needs it.

## HTML Delivery and Project Output Iron Rule

**Never create a project-output Markdown file.** The complete user-facing deliverable is three standalone HTML files:

1. `TITLE_参考图片清单.html` — supplied-image `P#` register, usage and inspection notes; it contains no image-generation prompts.
2. `TITLE_MiniMaxH3_Shotlist.html` — bilingual H3 prompts, local reference mapping, lyrics/dialogue, time and duration chips.
3. `TITLE_全中文分镜列表.html` — Chinese review list with time, duration, scene, action, continuity and `P#` references.

All user-facing scripts, lyrics, timing, reference mapping, prompts, review notes and revisions belong in these pages. The manifest and validation data are machine-readable inputs rather than project deliverables. Create a manifest only to generate a requested page package; for a prompt-only or shotlist-only request, do not create it as an extra output.

Use the blank templates in `assets/templates/` plus `assets/project-manifest.template.json`. Set all three `page_titles` fields from the new project. The templates must use those fields for both the browser title and visible heading; never inherit a previous project's type label.

The HTML pages are self-contained and include data, styling, rendering, search/filter controls, copy buttons, clickable time-range copy feedback, individual `P#` chips, quick jumps where applicable, and a fixed return-to-top control.

## Final Check

- timing, lyric/dialogue boundaries, audio labels and durations agree across the three pages;
- every prompt has at most nine supplied `P#` references; local `<Picture N>` positions match upload order and do not exceed nine;
- references have actual visible roles, canonical names stay consistent, and no prompt invents geometry absent from its supplied asset;
- all visible performance text matches the locked source and the unit range;
- the generic official H3 writing guide for the selected mode was read before drafting; a scene-specific official skill was used only after explicit user confirmation;
- every referenced audio file is separately defined as `<Audio N>`, bound to its speaker `(Sx)` when applicable, declared as audio reference or audio reuse in `summary`, marked with the matching official relationship in `retention_analysis`, and cited in its playback role;
- lighting, camera path, action, continuity and terminal frames are concrete and reproducible;
- the reference page lists supplied `P#` assets only and contains no image-generation prompt;
- no project-output Markdown file is created;
- every inline HTML script parses and page interactions remain intact after load.
