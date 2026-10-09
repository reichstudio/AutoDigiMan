# Digital-Presenter / Spoken-Video Workflow

Use this reference only when a visible presenter is speaking a script, tutorial, interview, explanation, commentary, or narration. It is not an MV substitute.

## What carries over from the MV route

- Read the official generic H3 prompt-writing skill and the selected mode guide first. With uploaded pictures or voice references, use Ref2VA and retain its six official fields and label semantics.
- Inspect each supplied image before describing it. `P#` is the project asset ID; `<Picture N>` is the shot-local upload position. Map them in upload order and cite visual references where they appear.
- Keep the supplied script verbatim, use a stable speaker ID, put performed words only in `<d>[Language] ...</d>`, and keep every `<Audio N>` separate from visual subjects.
- Treat all transitions as concrete visual decisions. Tie lenses, camera routes, action state changes, and cut times to what the viewer can see.
- Keep pages self-contained and ensure that the rendered copy button returns the entire prompt string.

## What is specific to a digital presenter

1. **Speech, not music, sets the pacing.** Use user-provided phrase/timing evidence when available. Otherwise call boundaries provisional. Do not call spoken text lyrics, infer beat drops, force dance, or calculate a musical-performance ratio unless the user explicitly asks for a hybrid or music-led result.
2. **Make the supplied environment operational.** For every scene reference, identify concrete visible anchors—such as a desk, screen, console, corridor, cabinet, door, seating, or display—and give the presenter a plausible, simple interaction or route using those anchors. Preserve the scene’s actual viewpoint, layout, equipment, and spatial depth in the prompt body; scene images are not merely lighting or mood references.
3. **Design body performance with the framing.** Choose wide, full-body, medium, and close shots according to the action and information being delivered. Do not default every shot to a face close-up, and do not impose a blanket ban on close-ups. A close view is appropriate when facial emphasis is the point; a wider view is appropriate when walking, object use, or environmental interaction matters.
4. **Use economical spoken-action choreography.** Give each unit a small, legible progression: a route or interaction, a few natural gestures tied to the spoken point, and an outcome/next-state. Avoid ornamental gesture lists, generic lighting paragraphs, and boilerplate preservation language that does not affect generation.
5. **Plan internal cuts only when they help.** A 4–15 second H3 unit may remain one shot or include `[Shot N] At MM:SS.mmm` cuts. Use a cut to reveal a relevant environment feature, move from route to interaction, change emphasis, or improve speech readability. State whether dialogue and lip sync continue across the cut. Do not split mechanically.
6. **Write chronological prompt prose, not appended warnings.** State reference-derived composition, movement, interaction, speaking, and cut result in playback order. Describe a final visual state naturally as part of the last action; do not append filler such as “End with …”. Do not add unrequested negative prompts.
7. **Audio roles stay precise.** For a voice-timbre file, use a standalone line such as `<Audio 1> is the voice-timbre reference for <Subject 1> (S1), sourced from “filename.mp3”.` Use `[reference generation + audio reference]` and `<Audio 1>: reference` when only timbre/delivery is guided. Use an audio-reuse relationship only if the signal itself is copied.

## Deliverable language and page behavior

- The English H3 pane is the copy-ready official prompt and remains in English except for the locked dialogue inside `<d>`.
- The Chinese pane is a working translation: retain required H3 field names and reference tokens, but write all descriptive prose in Chinese. Never leave untranslated English narrative sentences in it.
- For a spoken-video project without audience-only music, write `non_diegetic_music:` followed by `N/A.`. If the user actually requests a score, describe only that requested audience-only score.
- Use `本段口播` or `本段台词` in review pages for speech-led projects; reserve `本段歌词` and MV-specific page labels for music-led projects.
- When a prompt is stored in an HTML attribute for copy, escape `&`, `<`, `>`, `"`, and `'`, or use a text-node/clipboard source that preserves the full string. Test a rendered copy button with a prompt containing dialogue quotes and `<Audio 1>` before delivery.

## Free-edition boundary

Use supplied visual references only. Do not create, request, or prompt for supplementary presenter, scene, prop, or effect images unless the user explicitly changes this edition’s scope.

## Review checklist

- Every prompt body identifies the actual scene-reference composition and visible anchors, not only a color palette or generic atmosphere.
- Presenter framing, movement, prop/surface interaction, and gestures serve the spoken point.
- Internal cuts have valid local timestamps, a visual reason, and explicit speech/lip-sync continuity when speech crosses them.
- The Chinese prose contains no leftover English narrative wording; a no-score spoken unit uses `N/A.`.
- Prompt prose is concise and reproducible; it does not accumulate generic preservation boilerplate or unrequested negative constraints.
