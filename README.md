# Breach - Management Horror Game

**Survive 20 days at an abandoned research station while reality unravels.**

## Quick Start

```bash
git clone https://github.com/Vertynskiy/Breach.git
cd Breach
pip install pygame
python main.py
```

## Overview

Breached is a psychological management simulator where you must balance resource management, sanity preservation, and existential threats during 20 days of isolation at Station-7.

You're Dr. Mikhail Sokolov, assigned to an abandoned research station after its previous director vanished. The facility was built above an anomaly zone. As days pass, reality begins to unravel.

## Game Systems

### Day/Night Cycle
- **DAY (08:00 - 19:59)**: Preparation phase
  - Repair equipment
  - Manage resources  
  - Analyze anomaly data
  - Strategic planning

- **NIGHT (20:00 - 07:59)**: Survival phase
  - Real-time monitoring
  - Respond to events
  - Avoid manifestations
  - Maintain consciousness

### 5 Resource Types (Difficulty-Scaled)

| Resource | Normal | Hard | Insane | Recovery |
|----------|--------|------|--------|----------|
| **Fuel** | -2.5/hour day, -6/hour night | -3/hour day, -7.5/hour night | -4/hour day, -10/hour night | None |
| **Food** | -0.3/hour | -0.5/hour | -0.8/hour | None |
| **Water** | -0.25/hour | -0.4/hour | -0.6/hour | None |
| **Parts** | Repair costs vary | +20% cost | +50% cost | Found in anomaly zones |
| **Batteries** | -1/2 hours night | -1/1.5 hours night | -1/hour night | Solar panels (day) |

**Special Resources:**
- **Sedatives** (0-10): -30 sanity, +15% fuel consumption for 1 hour
- **Isotopes** (0-8): Calibrate anomaly sensors, ±5% to accuracy
- **Director's Logs** (0-20): Collectible lore, sanity varies by content

### Sanity System (0-100)

```
0-30:   STABLE - Everything normal
31-60:  ANXIOUS - Audio glitches, screen flicker, +10% resource drain
61-80:  PANICKED - Visual hallucinations, false alarms, +25% drain  
81-100: FRACTURED - Cannot distinguish real/fake, -5 sanity/min
        At 100 for 10 minutes → GAME OVER (Irreversible Break)
```

**Sanity Modifiers:**
- Darkness: -1/minute
- Isolation: -0.5/minute
- Anomaly events: -5 to -30
- Finding logs: -5 to +20 (contextual)
- Sedatives: -30 (once)
- Reading logs/journal: +1/minute

### 5 Work Stations

#### 1. MAIN OBSERVATION
- Window with dynamic sky/terrain
- Spotlight control (1 fuel/5 min)
- External sensor readouts
- Visual anomaly warnings

#### 2. CONTROL PANEL  
- Generator (fuel management, 3 power modes)
- Life support (heating, ventilation, lighting)
- Daily duty log (mandatory, 3x/day)
- System alerts

#### 3. ANOMALY MONITORS (FNAF-style)
- 4 camera feeds (corridor, engine room, entrance, roof)
- Battery drain: 1/30 minutes
- Manifestation alerts
- Recording system

#### 4. LABORATORY
- **Spectrometer**: Wave analysis mini-game → Isotopes
- **Radio**: Director's log playback + Morse code decryption
- **Magnetometer**: Anomaly activity graph + Storm prediction
- **Chemistry**: Create sedatives from compounds (if recipe found)

#### 5. JOURNAL & ARCHIVE
- **Duty Log**: Mandatory entries
- **Personal Notes**: Free form
- **Director's Logs**: Lore (20 entries)
- **Anomaly Maps**: Mark phenomena locations  
- **Manuals**: Equipment guides

### Event System

#### Type A: Routine (60% chance)
- Generator fluctuation
- Equipment malfunction  
- Supply decay
- **Resolution**: 2-3 choices, different resource costs

#### Type B: Anomalous (30% chance)
- Manifestation sighting
- Sensor anomaly
- Physical phenomenon
- **Triggers**: Night, sanity >40, magnetic storm
- **Resolution**: Affects sanity + story progression

#### Type C: Critical (10% chance)
- Director's body discovery
- Dimensional breach
- Offer/ultimatum from anomaly
- **Triggers**: Specific days, found logs, cumulative choices
- **Impact**: Leads to endings

## Difficulty Modes

### NORMAL (20 days)
- Balanced resource economy
- Mix of routine + anomalous events
- 5-6 events/day average
- Recommended for first playthrough

### HARD (20 days)
- 20% increased resource consumption
- Anomalous events 2x as frequent
- Sanity penalties +20%
- Fewer supplies available

### INSANE (20 days) 
- 40% increased resource consumption
- 90% anomalous events
- Sanity baseline starts at 50
- Permanent equipment failures
- Director's logs contain false information

## Endings (6 Total)

### SURVIVAL
1. **Exile** - Escape with proof (Normal/Hard)
2. **Sealed** - Seal the breach, stay forever (Normal/Hard)

### COMPROMISE  
3. **Bargain** - Make a deal with the anomaly (All difficulties)
4. **Merged** - Become something new (All difficulties)

### FAILURE
5. **Overrun** - Breach consumed you (All difficulties)
6. **Fractured** - Sanity collapse at day 20 (All difficulties)

## Architecture

```
breach/
├── main.py              # Entry point
├── settings.py          # Game constants
├── game.py              # Main game loop
├── src/
│   ├── core/
│   │   ├── resource_manager.py
│   │   ├── sanity_system.py
│   │   ├── time_manager.py
│   │   ├── event_generator.py
│   │   ├── save_system.py
│   │   └── game_state.py
│   ├── ui/
│   │   ├── screen_manager.py
│   │   ├── observation_screen.py
│   │   ├── control_panel.py
│   │   ├── monitors.py
│   │   ├── laboratory.py
│   │   └── journal.py
│   ├── content/
│   │   ├── events.json
│   │   ├── logs.json
│   │   ├── dialogue.json
│   │   └── anomalies.json
│   └── audio/
│       └── sound_manager.py
├── assets/
│   ├── textures/
│   ├── fonts/
│   └── audio/
└── docs/
    ├── GDD.md           # Full design doc
    └── BALANCE.md       # Economy tuning
```

## Development Roadmap

- [x] Repository setup
- [ ] Core systems (GameState, TimeManager, ResourceManager)
- [ ] UI Framework (5 screens)
- [ ] Event system
- [ ] Sanity mechanics
- [ ] Save/Load system
- [ ] Content (events, logs, dialogue)
- [ ] Audio design
- [ ] Polish & optimization

## Inspirations

- **FNAF** - Camera monitoring tension
- **60 Seconds** - Resource scarcity decisions
- **Papers Please** - Monotonous work with moral weight
- **SCP Foundation** - Anomaly containment lore
- **The Stanley Parable** - Narrative density

---

**Version**: 0.1.0 (Pre-Alpha)  
**License**: MIT  
**Author**: Vertynskiy
