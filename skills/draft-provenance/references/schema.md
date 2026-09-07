# provenance.json

```json
{
  "summary": {
    "title": "Rupture",
    "drafts": [{"label": "V1", "agent": "human", "words": 3381}, ...],
    "final_words": 3419,
    "share": {"human": 0.29, "machine": 0.0, "unattributed": 0.71},
    "machine_words_approved_by_human": 0,
    "moved_words": 0,
    "moves": 0,
    "unattributed_words": 2434,
    "note": "unattributed = introduced in a pass marked mixed; render as human."
  },
  "tokens": [
    {
      "text": "Tàpies",           // the word as written, punctuation attached
      "para": 1,                  // paragraph index in the final draft
      "class": "human",           // human | machine | unattributed
      "origin": "V1",             // draft label that introduced it, or "attested"
      "attested": true,           // present only when an attestation set the class
      "origin_agent": "human",
      "hands": ["human"],         // agents that touched it, in order
      "survived": 1,              // passes survived unchanged
      "moved": 0,                 // times it travelled in a moved run
      "moved_by": [],
      "move_from_para": null,     // paragraph it came from, last move
      "approved": false,          // machine word kept by a later human pass
      "churn": 0,                 // passes that changed text within 12 words
      "mix": 0.0                  // 0..1 both-hands score; drives green
    }
  ],
  "events": [
    {"step": 1, "label": "V2", "agent": "machine", "op": "replace",
     "prev": [10, 14], "cur": [10, 17], "deleted": "...", "inserted": "..."},
    {"step": 3, "label": "V4", "agent": "human", "op": "move",
     "words": 9, "from_prev": 812, "to_cur": 120, "text": "..."}
  ]
}
```

`events` is the raw record of every change per pass; `tokens` is the
per-word view of the final text. Renderers read `tokens`; audits read
`events`.
