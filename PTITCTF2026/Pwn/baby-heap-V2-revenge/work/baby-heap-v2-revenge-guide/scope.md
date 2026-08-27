# Case Scope

## meta
- case_id: baby-heap-v2-revenge-guide
- created: 2026-08-22T23:08:12.1053393+07:00
- operator: local
- project_root: D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge
- primary_skill: pwn-chain/SKILL.md
- primary_id: R17
- lead_role: lead
- specialist_roles: []
- hint: CTF pwn heap binary analysis

## auth
- status: granted
- basis: ctf_public
- evidence_of_auth: User identified PTITCTF2026 local CTF challenge
- MUST NOT proceed if status != granted

## in_scope
- assets:
  - D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2-revenge
- surfaces: []
- activities: []

## out_of_scope
- assets: []
- activities: [dos, phishing_real_users, unrestricted_exfil]

## network_profile
- mode: lab_only
- notes: |
    offline | lab_only | authorized_target_only | unrestricted_lab
    Change mode only after auth.status = granted.

## deliverables
- report: true
- field_journal: true
- diagrams: true
- timeline: true

## constraints
- timebox: {}
- stealth: low
- data_handling: anonymize

## signoff
- ready_for_act: true
- checklist:
  - [x] auth.status = granted
  - [x] in_scope.assets non-empty OR offline sample path set
  - [x] network_profile.mode chosen
  - [ ] out_of_scope reviewed
  - [ ] roles assigned (see skills/ops/role-map.md)

## ops_refs
- skills/ops/scope-contract.md
- skills/ops/evidence-finding-path.md
- skills/ops/role-map.md
- skills/ops/timeline-workitem.md
- skills/ops/IDENTITY.md