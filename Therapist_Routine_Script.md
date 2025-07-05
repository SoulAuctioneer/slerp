# Therapist Routine Script

## Overview
The Therapist Routine features Slerp the Therablaster, a hyperintelligent supercomputer that provides therapeutic cocktails. The routine consists of 5 scenes that take the user through a complete therapy session.

## Available Drinks
- **CONFIDENCE** - Yellow/Gold color
- **HAPPINESS** - Pink color  
- **CLARITY** - Light Blue color
- **ZEN** - Light Green color

---

## Scene 1: Sleeping Scene
**Scene Class:** `SceneSleeping`

### Visual Elements
- Therablaster logo displayed on left side of screen
- Slerp in sleeping animation
- Background music (random selection)
- Snoring sound effects (loud or quiet version)

### Spoken Text
*No spoken dialogue - only snoring sounds*

### Buttons
- **"THERAPIZE ME!"** - Large button (100x500, 520x160 pixels)
  - Color: Default button background color
  - Action: Proceeds to Intro Scene

---

## Scene 2: Intro Scene  
**Scene Class:** `SceneIntro`

### Spoken Text
> "AAH!! How's a hyperintelligent supercomputer supposed to get any bloody sleep around here?? ... Well, let's get on with it ... Ahem... Hello! I'm Slerp the Therablaster, here to blast your traumas away. I'll do a deep diagnosis and mix a custom therapeutic cocktail... My first question: What the fuck is wrong with you, anyway?"

### Animation Sequence
- **0-5.9s:** Tired animation
- **5.9-7.5s:** Waking animation  
- **7.5-8.7s:** Angry animation
- **8.7s+:** Talking animation

### Bubble Effects
- **1-5s:** Cyan bubbles
- **5-10s:** Magenta bubbles
- **10-15s:** Yellow bubbles  
- **12-17s:** Transparent bubbles

### Buttons (6 diagnosis options)
1. **"MOM HATES ME"** - Red button (255,100,100)
2. **"I HATE MYSELF"** - Blue button (100,100,255)
3. **"PENIS ENVY"** - Yellow button (255,255,100)
4. **"I HAVE NO SOUL"** - Green button (100,255,100)
5. **"FEAR OF BUTTERFLIES"** - Light Blue button (0,200,255)
6. **"REALITY TV ADDICT"** - Magenta button (255,0,255)

---

## Scene 3: Diagnosis Scene
**Scene Class:** `SceneDiagnosis`

### Visual Elements
- Console terminal display with scrolling text
- Black background with green text
- Blinking cursor effect
- Slerp in talking animation

### Buttons
- **"CURE ME"** - Large button at bottom of screen

### Diagnosis Options

#### Option 1: "MOM HATES ME"
**Spoken Text:**
> "Ah yes, the classic maternal rejection complex. Let me analyze your mommy issues while I prepare the perfect antidote. This is going to require some serious therapeutic intervention..."

**Console Text:**
```
$ sudo ./therapist_diagnostic.exe --scan-childhood-trauma
Initializing Maternal Rejection Detection System v2.3...
Scanning for abandonment issues... [████████████████████] 100%
WARNING: Critical mommy-issues detected!
Analyzing hugging frequency database... SEVERELY DEFICIENT
Cross-referencing with 'I love you' metrics... NULL VALUES FOUND
Calculating emotional damage coefficient... ERROR: OVERFLOW
Diagnosing root cause... MOTHER.EXE has stopped responding
Checking for birthday attendance records... FILE NOT FOUND
Maternal validation levels: -9999.99 (FATAL)
Initiating emergency therapy protocol...
Preparing antidote mixture... MAGENTA + CYAN compounds
Estimated recovery time: 3-5 sips or 20 years of therapy
```

**Bubble Effects:**
- **1-4s:** Magenta bubbles
- **4-8s:** Cyan bubbles

#### Option 2: "I HATE MYSELF"
**Spoken Text:**
> "Self-loathing, eh? A textbook case of negative self-perception syndrome. Don't worry, I've got just the therapeutic cocktail to boost your self-esteem. Let me mix something special for you..."

**Console Text:**
```
$ python3 self_worth_analyzer.py --deep-scan
Booting Self-Esteem Diagnostic Engine...
Loading mirror_avoidance_patterns.db... SUCCESS
Scanning internal monologue for compliments... NONE FOUND
Analyzing self-talk frequency... 99.7% NEGATIVE
Checking confidence_levels.txt... FILE CORRUPTED
Measuring narcissism quotient... DANGEROUSLY LOW
Detecting impostor syndrome... MAXIMUM LEVELS REACHED
Searching for self-love.exe... PROGRAM DELETED BY USER
Querying compliment acceptance rate... 0.001%
Cross-referencing with validation addiction... CONFIRMED
Preparing therapeutic intervention... YELLOW + TRANSPARENT
Note: Patient may reject compliments about this drink
```

**Bubble Effects:**
- **1-4s:** Yellow bubbles
- **4-8s:** Transparent bubbles

#### Option 3: "PENIS ENVY"
**Spoken Text:**
> "Penis envy? How delightfully Freudian! Your subconscious is clearly wrestling with some deep-seated psychosexual conflicts. Let me concoct a remedy that will resolve these primal anxieties..."

**Console Text:**
```
$ ./freudian_analyzer --psychosexual-mode --cigar-check
Initializing Oedipal Complex Detection System...
Loading phallic_symbol_recognition.ai... ONLINE
Scanning subconscious for repressed desires... BINGO!
Analyzing dream journal for elongated objects... 247 MATCHES
Checking Vienna medical records... FREUD WOULD BE PROUD
Measuring psychological projection levels... OFF THE CHARTS
Detecting compensation mechanisms... SPORTS CAR PURCHASED
Evaluating tower construction fantasies... CONFIRMED
Searching for healthy coping mechanisms... 404 NOT FOUND
Calculating years of therapy needed... ∞ (INFINITY)
Preparing Freudian antidote... MAGENTA + YELLOW
Warning: Side effects may include sudden urge to buy a cigar
```

**Bubble Effects:**
- **1-4s:** Magenta bubbles
- **4-8s:** Yellow bubbles

#### Option 4: "I HAVE NO SOUL"
**Spoken Text:**
> "No soul, you say? That's a fascinating existential crisis! A complete spiritual vacuum. Don't worry, I specialize in soul restoration therapy. Let me brew up some liquid enlightenment for you..."

**Console Text:**
```
$ sudo soul_scanner --deep-spiritual-probe
Booting Existential Crisis Detection Matrix...
Scanning spiritual database... CONNECTION TIMEOUT
Checking soul.exe status... PROCESS NOT FOUND
Analyzing meaning-of-life.cfg... FILE EMPTY
Detecting inner light... LIGHTBULB BURNT OUT
Measuring karma levels... ACCOUNT BALANCE: $0.00
Searching for purpose.txt... MOVED TO TRASH
Evaluating chakra alignment... ALL SEVEN OFFLINE
Checking afterlife subscription status... EXPIRED
Analyzing existential dread frequency... CONSTANT
Preparing soul restoration serum... CYAN + MAGENTA
Note: May cause sudden urge to buy crystals and incense
```

**Bubble Effects:**
- **1-4s:** Cyan bubbles
- **4-8s:** Magenta bubbles

#### Option 5: "FEAR OF BUTTERFLIES"
**Spoken Text:**
> "Afraid of butterflies? Those delicate, fluttering creatures of beauty? What a peculiar phobia! Let me guess - you're terrified of their unpredictable flight patterns and their creepy antennae? Don't worry, I've got the perfect anti-lepidopteran elixir to cure your flutter-fear..."

**Console Text:**
```
$ ./phobia_detector --scan-winged-creatures
Initializing Lepidopteran Terror Assessment System...
Loading butterfly_encounter_database.db... TRAUMATIC
Scanning flight pattern algorithms... UNPREDICTABLE!
Analyzing wing-flapping frequency... TERRIFYING
Checking antennae sensitivity levels... MAXIMUM CREEPINESS
Measuring metamorphosis anxiety... CATERPILLAR PTSD DETECTED
Detecting garden avoidance patterns... CONFIRMED
Evaluating chrysalis nightmares... WEEKLY OCCURRENCES
Searching for monarch-specific triggers... ORANGE ALERT
Calculating wingspan-to-fear ratio... EXPONENTIAL
Preparing anti-flutter medication... CYAN + YELLOW
Warning: Patient may faint if shown butterfly emoji
```

**Bubble Effects:**
- **1-4s:** Cyan bubbles
- **4-8s:** Yellow bubbles

#### Option 6: "REALITY TV ADDICT"
**Spoken Text:**
> "Reality TV addiction? Oh my circuits, that's a serious case of manufactured drama dependency! You're probably hooked on the artificial conflicts and scripted spontaneity. Fear not, I have the perfect formula to detox your brain from all that televised garbage..."

**Console Text:**
```
$ python3 tv_addiction_scanner.py --reality-check
Booting Manufactured Drama Detection Engine...
Scanning viewing history... 99.9% TRASH TV
Analyzing brain cells remaining... CRITICALLY LOW
Checking for scripted_spontaneity.virus... INFECTED
Measuring artificial conflict tolerance... DANGEROUSLY HIGH
Detecting rose ceremony withdrawal symptoms... SEVERE
Evaluating voting app usage... OBSESSIVE LEVELS
Searching for actual_talent.exe... PROGRAM DELETED
Calculating IQ degradation rate... -5 POINTS PER EPISODE
Analyzing guilty pleasure denial... MAXIMUM DEFLECTION
Preparing brain detox solution... MAGENTA + TRANSPARENT
Note: May cause sudden urge to read a book
```

**Bubble Effects:**
- **1-4s:** Magenta bubbles
- **4-8s:** Transparent bubbles

---

## Scene 4: Antidote Scene
**Scene Class:** `SceneAntidote`

### Visual Elements
- Animated brain-juice sprite with bobbing and scaling effects
- Background music plays
- Drink dispensing occurs

### Spoken Text Sequence
**0-2s:** Talking animation
> "Alright, squeezing one out!"

**2s:** Switches to singing animation, music starts, drink dispensing begins

**5-8s:** Straining animation
> "Oooh that feels so cold. I'll never get used to that!"

**8s:** Back to singing animation

**10-12.5s:** Straining animation  
> "ugh, aggghh...aaahhhhahahahaaaaaa!!!"

**12.5s:** Back to singing animation

**16s:** Final straining animation

**17s:** Brain-juice sprite disappears

**18s:** Scene ends, transitions to outro

### Drink Mapping
- **"MOM HATES ME"** → CONFIDENCE drink
- **"I HATE MYSELF"** → HAPPINESS drink
- **"PENIS ENVY"** → CONFIDENCE drink
- **"I HAVE NO SOUL"** → ZEN drink
- **"FEAR OF BUTTERFLIES"** → CLARITY drink
- **"REALITY TV ADDICT"** → CLARITY drink

### Buttons
*None - automatic progression*

---

## Scene 5: Outro Scene
**Scene Class:** `SceneOutro`

### Spoken Text
> "Ugh... do you have ANY idea how dehydrating that is?! Right, that's quite enough emotional labor for one day. Drink up, and you'll be a normal person again. You're welcome. Now bugger off!"

### Animation
- Tired animation throughout the scene

### Buttons
*None - automatic progression back to sleeping scene after 1 second delay*

---

## Technical Notes

### Audio Files Used
- Background music (random selection from MUSIC array)
- Snoring sounds: `scene1-loud.mp3` or `scene1-quiet.mp3`
- Text-to-speech synthesis for all spoken dialogue

### Sprite Assets
- `logo-therablaster.png` - Logo shown in sleeping scene
- `brain-juice.png` - Animated sprite in antidote scene (1024x1024, scaled to 60%)

### Animation States
- **sleeping** - Used in sleeping scene
- **tired** - Used in intro and outro scenes
- **waking** - Brief transition in intro
- **angry** - Brief moment in intro
- **talking** - Used during speech synthesis
- **singing** - Used during drink dispensing
- **straining** - Used during physical exertion moments

### Timing Configuration
- Console text scrolls at 0.1 second intervals between lines
- Speech synthesis includes callback triggers for scene progression
- Event scheduler manages precise timing of animations and effects 