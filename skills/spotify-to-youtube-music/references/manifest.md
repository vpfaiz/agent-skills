# Canonical verification manifest

Source positions are unique per playlist, starting at 1. Destination entries must be the complete actual saved playlist in displayed order, excluding recommendations. Preserve repeated IDs as separate entries.

```json
{
  "playlists": [{
    "name": "Example collection",
    "source_count": 3,
    "source_entries": [
      {"position": 1, "title": "Song A", "status": "matched", "video_id": "example-a", "evidence": "Observed artist, album, version, duration, provider"},
      {"position": 2, "title": "Song B (Lo-fi)", "status": "unresolved", "reason": "Only a different remix found"},
      {"position": 3, "title": "Song A", "status": "matched", "video_id": "example-a", "evidence": "Same verified recording, repeated source occurrence"}
    ],
    "destination_entries": [
      {"video_id": "example-a", "title": "Song A"},
      {"video_id": "example-a", "title": "Song A"}
    ]
  }]
}
```

Add source/destination URLs and detailed match evidence locally as needed. Allowed statuses: matched, unresolved, unavailable. Matched entries require video_id and nonempty evidence. Other entries require a reason. Evidence can be a string or object; the script checks existence, not musical validity.

Run `scripts/audit_manifest.py manifest.json`. Exit 0 means supplied coverage and destination sequence reconcile; exit 1 means invalid data or mismatch. A live transfer is verified only when supplied rows came from the complete actual destination.
