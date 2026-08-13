# Darian's Mansion — Thorne Estate Canonical Reference

Status: CANONICAL SOURCE REFERENCE
Source: Creator-provided finalized Darian's Mansion document
Project use: Observer Sandbox world/environment authority for the Thorne Estate

## Scope and implementation boundary

This document preserves the Creator-provided canonical mansion description that the current Observer Sandbox estate environment is based on.

Current implementation policy:
- the existing Observer Sandbox world models the **interior estate first**;
- interior rooms, facilities, objects and training environments should reconcile against this reference;
- exterior traversal and outdoor estate systems remain deferred until explicitly implemented;
- implementation may be incremental, but it must not silently contradict this reference;
- where the runtime contains a provisional layout detail that is not specified here, it remains provisional rather than becoming new canon by implication.

## Darian's Mansion — The Thorne Estate

**Location:** South Lake Tahoe, California  
**Architecture Style:** Modern fortress with high-tech security and tactical reinforcements  
**Ownership History:** Previously owned by Elias Thorne, inherited by Darian

## 1. Structural Overview

### Size & Layout

- Expansive three-story estate with a reinforced underground level.
- Covers approximately 15,000 sq. ft. on 50 acres of private land.
- Secluded in the forested outskirts of South Lake Tahoe.

### Main Areas

#### Living Quarters

- Minimalistic yet luxurious; designed for comfort and practicality.
- Bedrooms: Darian's master suite, guest rooms, and Quasi's room.
- Common Areas: Open living room with fireplace, panoramic windows, and reinforced steel doors.

#### Training Hall

- High-tech combat simulation room with interactive AI opponents.
- Obstacle Course and Combat Pit for sparring and agility drills.
- Advanced VR Tactical Simulator for weapon proficiency and battle planning.

#### Top-Class Home Gym

- Fully equipped with modern machines for strength, endurance, and agility training.
- Olympic-level weightlifting setup.
- Cardio and speed-focused equipment, including high-speed treadmills and an altitude training chamber.

#### Surveillance & Intelligence Hub

- Houses Elias's old encrypted files, classified documents, and high-tech monitoring systems.
- Secure mainframe server for hacking, intelligence retrieval, and Dominion Order research.
- Encrypted communications center for off-grid messaging.

#### Armory & Storage

- Stockpiled firearms, knives, explosives, and survival gear.
- Hidden weapons cache behind biometric lock safes.
- Special hand-to-hand combat weapons collection, including custom knuckle dusters, karambits, and tomahawks.

#### Garage & Workshop

- Houses modified vehicles, including tactical motorcycles, armored SUVs, and all-terrain vehicles.
- Advanced weapons engineering bench for customization and repairs.
- Spare explosives, tracking devices, and survival kits.

#### Library & Study

- Contains Elias's research, old Dominion Order history, and classified combat strategies.
- Large collection of philosophical and psychological books.

#### Medical Room

- Fully equipped medical bay with surgery-grade tools.
- Automated first-aid station with advanced scanners.
- Emergency blood supply, IV drips, and regenerative medicine storage.

#### Food Supply Storage Room

- Large pantry stocked with long-term survival rations.
- Special freezer section for fresh food and emergency supply cache.
- High-end nutrition supplements for performance enhancement.

## 2. Outdoor & Underground Features

### Private Lake Access

- Hidden dock for covert departures and escape routes.
- Private water purification system.

### Underground Bunker

- Reinforced escape chamber with backup supplies and weapons.
- Hidden off-grid survival chamber.

### Tactical Obstacle Course

- Built for extreme agility and endurance training.
- Includes wall climbs, barbed wire crawl zones, and high-speed sprinting tracks.

## 3. Security & Defense Systems

### Surveillance System

- 360-degree thermal and motion sensor cameras.
- AI-powered facial recognition software for tracking movement.

### Defensive Infrastructure

- Bulletproof glass and reinforced walls with military-grade protection.
- Underground panic rooms for emergency shelter.
- Tactical escape tunnels leading to safe exit points.

### Access Restrictions

- Biometric security locks; only Darian and Quasi have full clearance.
- Encrypted safe rooms with Elias's unknown hidden safes.

## 4. Narrative Importance

- **Darian's Stronghold:** His only secure base of operations after returning from his training with Kane.
- **Elias's Legacy:** The mansion holds hidden clues about Elias's past and his disappearance.
- **Potential Battleground:** The Dominion Order may target this stronghold.
- **Quasi's Presence:** This location shapes Darian and Quasi's growing bond.

## Observer Sandbox reconciliation notes

The current `config/worlds/home.v1.json` already represents the Thorne Estate as the active world foundation, including the three-story/underground structure and major interior spaces such as the living room, library, garage/workshop, intelligence hub, communications room, Training Hall, Top-Class Home Gym, Medical Bay, Armory & Storage, Food Supply Storage, and Underground Bunker.

The current implementation is intentionally incomplete relative to this canonical reference. In particular, the Training Hall and Top-Class Home Gym are still sparse in equipment and training-method coverage. The next approved environment-expansion work should enrich those interior surfaces before broader profile progression expansion.

Deferred from the current interior-only implementation line:
- private lake access and hidden dock;
- outdoor tactical obstacle course;
- exterior estate traversal;
- external escape-route traversal and broader Tahoe world traversal.

These deferred features remain canonical facts but are not yet runnable world surfaces.
