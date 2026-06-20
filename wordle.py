#!/usr/bin/env python3
"""Terminal Wordle — daily 5-letter word game with streaks."""

import json
import os
import sys
from datetime import date
from pathlib import Path

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[42m\033[30m"   # correct letter, correct position
YELLOW = "\033[43m\033[30m"   # correct letter, wrong position
GRAY   = "\033[100m\033[37m"  # letter not in word

# ── Word list (500 common 5-letter words) ─────────────────────────────────────
WORDS = """about above abuse actor acute admit adopt adult after again
agent agree ahead alarm album alert alike alien align alive alley
allow alone along aloud altar alter angel anger angle angry anime
ankle annex antic anvil apart apple apply april arbor arcane argue
arise armor aroma arose array arrow arson aside asked asset atone
attic audio audit avail avoid awake award aware awful badly baker
basic basin basis batch beach beard beast began begin being below
bench billy binds birth black blade blame bland blank blast blaze
bleed bless blind blink bliss block blood bloom blown blues blunt
board boner bonus boost booth bound brace braid brain brand brave
bread break breed bride brief bring broad broke broom brown brush
buddy build built bulge bunch burst buyer cabin cable camel candy
cargo carry catch cause cedar chair chaos charm chase cheap check
chest chief child china chord civic civil claim clamp clank clash
clasp class clean clear clerk click cliff climb cling clink clock
clone close cloth cloud clown coach coast color comet comic comma
coral count court cover craft crane crash crave cream creek creep
crisp cross crowd crush crust crypt cubic cubic curve cycle daddy
daily dairy daisy dance death debug debut debut decoy dense depot
depth derby devil dirty disco ditty dodge doing doubt dough draft
drain drama drank drape dream dress dried drift drill drink drive
drone drove drown druid drunk dryer dunce dwarf dying eager early
earth eight elite elbow elite email ember empty enemy enjoy enter
entry equal error essay evade event every exact exam excel exist
extra fable faced facts fairy false fancy farce feast ferry fetch
fever fever field fiend fifth fifty fight final flame flank flare
flask fleet flesh flick fling float flock flood floor flora floss
flour flown fluff fluke flume flunk flute focal foggy folio force
forge forth forum found frame frank fraud fresh front frost froze
froze fruit fully gauge gauze gavel gavel gavel giant given gizmo
given glare glass glide globe gloom gloss glove glyph gnome going
golem grace grade grain grand grant grape grasp grave great greed
green greet grind groan groin group grove growl grown guard guava
guess guide guile guise gusto gypsy haste hatch haunt haven heart
heavy hence herbs heron hinge hippo hoist holly homer horse hotel
hound house human humor hunky hurry hyena ideal idiot image impel
inane index indie inert inner input inter intro irony ivory joker
joust judge juice juicy jumbo jumpy juror kayak knack kneel knelt
knife knoll knope knot known label labor lapse large laser latch
later laugh layer leach learn lease least leave ledge legal lemon
level light lilac limit linen liner liver livid llama lobby lodge
lofty login loose lover lower lucky lunar magic maple march marry
match mayor media mercy merge merit metal might mirth mixer modal
model modem moist money month moral motor motto mount mourn mouth
moved movie muddy music naive naval nifty night ninja noble noise
north noter novel nymph oasis occur octet offer olive onset opera
order organ other ought ounce outer ovary overt oxide ozone pacer
paint panel panic party pasta patch pause payee peace pearl penal
penny perch petal phase phone photo piano pilot pinch place plain
plait plane plank plant plead pleat plier pluck plumb plume plunk
plush point poise poker polka porch posed pouch power press price
pride prime print prior prism prize probe prone proof prose proud
prove prowl proxy prude prune psalm pubic pulse punch pupil purge
purse queen query queue quick quiet quota quote radar radix raise
rally ranch range rapid ratio reach react realm rebel recon reign
relax renew repay repel repro rerun resin retch reuse revel rider
ridge right risky rival rivet robot rodeo rouge rouge rouge rough
round rowdy royal rugby ruler rural rusty sadly saint salad sauce
scale scamp scant scare scene scone scope score scorn scout scowl
seize sense seven shade shake shale shall shame shape share shark
sharp shave shawl sheen sheet shelf shell shift shine shire shirt
shock shoal shore short shove shown shrew shrub shrug shunt siege
silky silly since sixth sixty sixty sixty sixty sixty sixty sixty
sixty sixty sixty sixty sixty sixty sixty sixty sixty sixty sixty
skate skill skimp skirt skull slack slain slang slant slash slate
slave sleek sleep sleet slept slice slide slime sling slink slope
sloth slunk small smart smash smell smelt smile smoke smite smock
smote snack snail snake snare sneak sneer snide sniff snore snort
snout soapy solar solve sorry south space spade spank spare spark
speak spear speck speed spell spend spice spicy spied spill spine
spoke spoon spore sport spout spray spree sprig spunk squad squat
staid stain stair stake stale stalk stall stare stark start stash
state stays steak steal steam steel steep steer stern stiff still
stock stoic stomp stone stood stool storm story stout stove stoic
stray strip strut stuck study stump stunt style sugar suite sunny
super swamp swear sweat sweep swept swept swift swill swipe swirl
swoop sword sworn syrup taboo taffy taken tally talon tango taunt
tawny teach tease teeth tempo tense tepid terse thank thatch their
theme thick thief thing think third thorn those three threw throw
thrum thumb thump tiara tiger timid titan today token total touch
tough towel tower toxic track trail train trait tramp trawl tread
treat trend trial trick tripe trite troll tromp troop trove truce
truck truly trump trunk truss trust truth tuber tulip tuner tunic
turbo tutor tweak tweed tweet twice twist twirl ultra umbra under
unify union unite until unzip upper usher utter vague valid valor
value valve vapid vault vaunt vicar vigor viola viper virus vista
vital vivid vocal vodka voila vouch wager waltz water weary weave
wedge weedy weigh weird whelp while whiff whim which whiff whirl
whole wider wield wispy witch witty woken world worse worst worth
would wound wrath wring wrist wrote yacht yield young youth zappy
zebra zesty zilch zippy zombie zonal""".split()

WORDS = [w for w in WORDS if len(w) == 5]

STATS_FILE = Path.home() / ".wordle_stats.json"

# ── Stats ─────────────────────────────────────────────────────────────────────
def load_stats() -> dict:
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text())
        except Exception:
            pass
    return {"streak": 0, "max_streak": 0, "played": 0, "won": 0,
            "last_date": None, "distribution": {str(i): 0 for i in range(1, 7)}}

def save_stats(stats: dict) -> None:
    STATS_FILE.write_text(json.dumps(stats, indent=2))

def update_stats(stats: dict, won: bool, guesses: int) -> None:
    today = str(date.today())
    stats["played"] += 1
    if won:
        stats["won"] += 1
        if stats["last_date"] == str(date.today().__class__.fromordinal(date.today().toordinal() - 1)):
            stats["streak"] += 1
        else:
            stats["streak"] = 1
        stats["max_streak"] = max(stats["max_streak"], stats["streak"])
        stats["distribution"][str(guesses)] = stats["distribution"].get(str(guesses), 0) + 1
    else:
        stats["streak"] = 0
    stats["last_date"] = today

def print_stats(stats: dict) -> None:
    played = stats["played"]
    won    = stats["won"]
    pct    = int(won / played * 100) if played else 0
    print(f"\n{BOLD}Statistics{RESET}")
    print(f"  Played: {played}  Won: {pct}%  "
          f"Streak: {stats['streak']}  Best: {stats['max_streak']}")
    print(f"\n{BOLD}Guess distribution{RESET}")
    max_val = max((stats["distribution"].get(str(i), 0) for i in range(1, 7)), default=1) or 1
    for i in range(1, 7):
        n = stats["distribution"].get(str(i), 0)
        bar = "█" * max(1, int(n / max_val * 20))
        print(f"  {i}  {GREEN}{bar}{RESET} {n}" if n else f"  {i}  {GRAY}{'░' * 1}{RESET} {n}")

# ── Daily word ────────────────────────────────────────────────────────────────
def daily_word() -> str:
    epoch = date(2024, 1, 1)
    idx   = (date.today() - epoch).days % len(WORDS)
    return WORDS[idx]

# ── Render a guess row ────────────────────────────────────────────────────────
def score_guess(guess: str, answer: str) -> list[str]:
    """Return list of 'green', 'yellow', 'gray' for each letter."""
    result  = ["gray"] * 5
    pool    = list(answer)

    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "green"
            pool[pool.index(g)] = None

    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in pool:
            result[i] = "yellow"
            pool[pool.index(g)] = None

    return result

def render_row(guess: str, scores: list[str]) -> str:
    colour = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
    cells  = [f"{colour[s]} {c.upper()} {RESET}" for c, s in zip(guess, scores)]
    return " ".join(cells)

def empty_row() -> str:
    return " ".join([f"{GRAY}   {RESET}"] * 5)

# ── Keyboard tracker ──────────────────────────────────────────────────────────
def render_keyboard(used: dict[str, str]) -> str:
    rows  = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    colour = {"green": GREEN, "yellow": YELLOW, "gray": GRAY, None: BOLD}
    lines = []
    for row in rows:
        parts = []
        for ch in row:
            state = used.get(ch)
            c     = colour[state]
            parts.append(f"{c} {ch.upper()} {RESET}")
        lines.append(" ".join(parts))
    return "\n".join(lines)

def update_keyboard(used: dict[str, str], guess: str, scores: list[str]) -> None:
    priority = {"green": 3, "yellow": 2, "gray": 1, None: 0}
    for ch, s in zip(guess, scores):
        if priority[s] > priority.get(used.get(ch)):
            used[ch] = s

# ── Display board ─────────────────────────────────────────────────────────────
def clear() -> None:
    os.system("clear" if os.name != "nt" else "cls")

def draw(guesses: list[tuple[str, list[str]]], used: dict[str, str],
         message: str = "") -> None:
    clear()
    print(f"\n{BOLD}  W O R D L E{RESET}\n")
    for guess, scores in guesses:
        print("  " + render_row(guess, scores))
    for _ in range(6 - len(guesses)):
        print("  " + empty_row())
    print()
    print(render_keyboard(used))
    if message:
        print(f"\n  {BOLD}{message}{RESET}")

# ── Main game loop ─────────────────────────────────────────────────────────────
def play() -> None:
    answer   = daily_word()
    stats    = load_stats()
    guesses: list[tuple[str, list[str]]] = []
    used:    dict[str, str] = {}
    word_set = set(WORDS)

    draw(guesses, used, f"Guess the 5-letter word! ({date.today()})")

    while len(guesses) < 6:
        try:
            raw = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            sys.exit(0)

        if len(raw) != 5:
            draw(guesses, used, "⚠  Enter a 5-letter word.")
            continue
        if not raw.isalpha():
            draw(guesses, used, "⚠  Letters only.")
            continue
        if raw not in word_set:
            draw(guesses, used, f"⚠  '{raw.upper()}' not in word list.")
            continue

        scores = score_guess(raw, answer)
        guesses.append((raw, scores))
        update_keyboard(used, raw, scores)

        if raw == answer:
            draw(guesses, used, praise(len(guesses)))
            update_stats(stats, True, len(guesses))
            save_stats(stats)
            print_stats(stats)
            print()
            return

        if len(guesses) == 6:
            draw(guesses, used, f"The word was: {answer.upper()}")
            update_stats(stats, False, 6)
            save_stats(stats)
            print_stats(stats)
            print()
            return

        draw(guesses, used)

def praise(n: int) -> str:
    return ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"][n - 1]

if __name__ == "__main__":
    play()
