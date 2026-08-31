# -*- coding: utf-8 -*-
"""
Original content for the nine service/device pages plus buy-sell-trade.
Every page has its own distinct structure and prose -- none of these are a
find/replace of a shared template with only the device name swapped.

No prices, repair times, certifications, manufacturer authorization,
guarantees, or success rates are stated anywhere in this file.
"""

from src.data.business import BIZ, SERVICE_AREAS, DISCLOSURE_LONG

CITY = BIZ["address"]["city"]

APPLE_DISCLOSURE = (
    "Smart Geeks is an independent repair shop. We are not Apple, and we are "
    "not authorized, certified, or approved by Apple Inc. “MacBook,” "
    "“iMac,” “Mac mini,” and “Apple” are trademarks of "
    "Apple Inc., used here only to identify the devices we can work on."
)

GENERAL_DISCLOSURE = (
    "Smart Geeks is an independent repair shop and is not affiliated with, "
    "authorized by, or endorsed by any device manufacturer. Brand and model "
    "names are used only to identify the devices we can work on."
)


SERVICES = [
    # ------------------------------------------------------------------ #
    {
        "slug": "laptop-repair",
        "nav_label": "Laptop repair",
        "h1": "Laptop Repair in Surrey, BC",
        "title_tag": f"Laptop Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Independent laptop repair in Surrey, BC for screens, batteries, "
            "keyboards, charging ports, and hardware faults. Bring your laptop "
            "in or contact Smart Geeks to describe the issue."
        ),
        "card_summary": "Screens, batteries, keyboards, charging, and hardware faults on Windows and other PC laptops.",
        "icon": "laptop",
        "whatsapp_key": "laptop-repair",
        "answer": (
            "Smart Geeks repairs PC laptops in Surrey, BC, including screen, battery, "
            "keyboard, charging-port, and internal hardware issues. Every laptop is "
            "assessed on the bench before any repair work begins, and we'll explain "
            "what we find before proceeding."
        ),
        "overview": [
            "Laptops fail for a lot of different reasons, and it isn't always obvious "
            "whether the cause is hardware, software, or something in between. Our "
            "bench process is built to tell the difference before any parts are "
            "ordered or work begins, so you're not paying to guess.",
            "We work on laptops from the common Windows-based manufacturers -- Dell, "
            "HP, Lenovo, Asus, Acer, and others -- covering everything from a cracked "
            "screen to a laptop that won't power on at all.",
        ],
        "symptoms": [
            "Laptop won't turn on, or powers on with no display",
            "Cracked, flickering, or discoloured screen",
            "Battery drains quickly or the laptop won't hold a charge",
            "Charging port feels loose or the laptop won't charge at all",
            "Overheating, loud fan noise, or the laptop shuts off under load",
            "Keyboard keys that don't register, or a trackpad that misbehaves",
            "Slow performance, freezing, or repeated crashes",
            "Liquid spill or visible physical damage",
            "Loose or cracked hinges",
            "No sound, no webcam, or Wi-Fi/Bluetooth that won't connect",
        ],
        "diagnostic": [
            "We start with a visual inspection for physical or liquid damage, then run "
            "a power-on and POST (power-on self-test) check to see how far the laptop "
            "gets before it fails.",
            "From there we test the battery and charging circuit, check display output "
            "and graphics behaviour, and run storage and memory diagnostics. This lets "
            "us separate a hardware fault from a software or operating-system problem "
            "before recommending any repair.",
        ],
        "repair_steps": [
            ("Intake and symptom review", "We note exactly what you're experiencing and any relevant history (drops, spills, recent updates)."),
            ("Bench diagnostics", "We test the affected components and isolate whether the fault is hardware, software, or both."),
            ("Findings and options", "We explain what we found in plain language before any repair work starts."),
            ("Repair", "Depending on the fault, this may mean a screen, battery, keyboard, or charging-port replacement, or board-level work."),
            ("Function test and handback", "We verify the repair holds under normal use before returning the laptop to you."),
        ],
        "factors": [
            "How old the laptop is and whether replacement parts are still available for that model",
            "Whether the damage is cosmetic (screen, keys) or affects internal components",
            "Whether a fault turns out to need board-level repair rather than a simple part swap",
            "Whether your data has been backed up, which affects how we handle storage-related repairs",
        ],
        "what_to_bring": [
            "The laptop and its charger",
            "Any error messages you've seen, ideally as a photo",
            "A general idea of when the issue started and whether anything changed beforehand",
            "Please don't send passwords or passcodes through our contact form -- if we need the laptop unlocked to test it, we'll talk through that with you in person or by phone.",
        ],
        "related": ["desktop-repair", "motherboard-chip-level-repair", "buy-sell-trade"],
        "faqs": [
            ("Can you fix a laptop that won't turn on at all?",
             "A laptop with no power at all can be caused by several things, from a "
             "failed charging port to a board-level fault. We run a bench diagnostic "
             "first to find the actual cause before recommending a repair path."),
            ("Do you work on gaming laptops?",
             "Yes, the same diagnostic and repair process applies to gaming laptops. "
             "Thermal issues and GPU-related faults are common on higher-performance "
             "models, and we test for those specifically."),
            ("What if my laptop has liquid damage?",
             "Liquid damage is assessed case by case. Corrosion can affect components "
             "in ways that aren't visible right away, so we'll walk you through what we "
             "find during diagnostics rather than assuming the outcome in advance."),
            ("Will you back up my files before working on my laptop?",
             "We recommend backing up anything important before drop-off whenever "
             "that's possible, since some repairs (like storage replacement) can affect "
             "data. We're happy to talk through your specific situation."),
        ],
        "disclosure": GENERAL_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "desktop-repair",
        "nav_label": "Desktop repair",
        "h1": "Desktop Computer Repair in Surrey, BC",
        "title_tag": f"Desktop Computer Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Desktop PC repair in Surrey, BC for power issues, crashes, no-display "
            "faults, and component failures. Custom builds and prebuilt towers welcome."
        ),
        "card_summary": "Power supply, boot, crash, and component diagnostics for prebuilt and custom-built desktop towers.",
        "icon": "desktop",
        "whatsapp_key": "desktop-repair",
        "answer": (
            "Smart Geeks diagnoses and repairs desktop computers in Surrey, BC, "
            "including prebuilt towers and custom builds -- power issues, random "
            "shutdowns, no-display faults, and component failures."
        ),
        "overview": [
            "Desktop towers are easier to open up than laptops, but that also means "
            "there are more individual components that can be the actual source of a "
            "problem: power supply, motherboard, RAM, storage, or graphics card.",
            "We test components individually rather than replacing parts on a guess, "
            "which matters most on custom builds where compatibility and existing "
            "configuration need to be respected.",
        ],
        "symptoms": [
            "Desktop won't power on at all",
            "Random shutdowns or restarts during use",
            "Blue screen errors or repeated crashes",
            "No display output even though the PC seems to power on",
            "Unusual noises -- clicking, grinding, or a loud fan",
            "Overheating or thermal shutdowns",
            "Slow performance that's gotten noticeably worse",
            "Won't boot into the operating system",
            "USB ports or other connections that have stopped working",
        ],
        "diagnostic": [
            "We test the power supply under load first, since a failing PSU can look "
            "like a dozen different problems. From there we check POST behaviour and "
            "any beep or error codes the motherboard reports.",
            "Individual components -- RAM, storage, graphics card -- are tested in "
            "isolation where possible, along with a thermal inspection, so we can tell "
            "you specifically which part is at fault rather than replacing things "
            "speculatively.",
        ],
        "repair_steps": [
            ("Intake", "We record the symptoms and ask about any recent hardware or software changes."),
            ("Bench diagnostics", "Power supply, POST behaviour, and individual components are tested."),
            ("Component isolation", "We narrow the fault down to a specific part wherever the symptoms allow it."),
            ("Repair or replacement", "This may include PSU or RAM replacement, storage swap, GPU reseating, or a thermal service (paste and fan cleaning)."),
            ("Stability test and handback", "We run the system under normal load before returning it to confirm the fix holds."),
        ],
        "factors": [
            "Whether replacement parts are compatible with your existing build",
            "The age of the system and availability of matching components",
            "Whether the desktop is a custom build or a manufacturer prebuilt, which affects part sourcing",
            "How much dust or thermal buildup has accumulated, which can mimic other faults",
        ],
        "what_to_bring": [
            "The full tower and its power cable",
            "Note any recent hardware changes, software updates, or power events (like an outage) before the issue started",
            "If it's a custom build, any details you have on the components used are helpful",
        ],
        "related": ["laptop-repair", "motherboard-chip-level-repair", "buy-sell-trade"],
        "faqs": [
            ("Do you work on custom-built PCs?",
             "Yes. We test components individually and take your existing configuration "
             "into account rather than assuming a one-size-fits-all fix."),
            ("My PC turns on but there's no display -- what's usually the cause?",
             "That can point to a graphics card, RAM seating, motherboard, or display "
             "cable issue. It's exactly the kind of symptom our bench diagnostic is "
             "built to narrow down before any parts are replaced."),
            ("Can you clean dust out of my computer?",
             "Yes, thermal servicing (cleaning and, where needed, reapplying thermal "
             "paste) is part of what we offer when overheating or fan noise is the "
             "concern."),
        ],
        "disclosure": GENERAL_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "printer-repair",
        "nav_label": "Printer repair",
        "h1": "Printer Repair in Surrey, BC",
        "title_tag": f"Printer Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Printer repair in Surrey, BC for paper jams, print-quality issues, "
            "connectivity errors, and mechanical faults on home and small-office printers."
        ),
        "card_summary": "Paper jams, print-quality issues, connectivity errors, and mechanical faults.",
        "icon": "printer",
        "whatsapp_key": "printer-repair",
        "answer": (
            "Smart Geeks repairs home and small-office printers in Surrey, BC -- "
            "paper jams, streaky or faded prints, connectivity errors, and mechanical "
            "faults like feed roller or print-head problems."
        ),
        "overview": [
            "Printer problems are often mechanical (a worn feed roller, a jammed "
            "carriage) or connectivity-related (Wi-Fi, USB, or driver issues), and the "
            "fix looks very different depending on which one it is.",
            "We check both sides -- the physical mechanism and the connection/software "
            "path -- rather than assuming a paper jam is always a paper jam.",
        ],
        "symptoms": [
            "Repeated paper jams",
            "Streaky, faded, or banded print output",
            "Printer won't connect over Wi-Fi or USB",
            "Error lights or error codes on the printer's display",
            "Scanner not working even though printing does",
            "Clogged or misaligned print head",
            "Feed roller slipping or not picking up paper",
            "Driver or connectivity errors from your computer",
        ],
        "diagnostic": [
            "We start by reading and looking up any error code the printer is "
            "displaying, then physically inspect the print head, rollers, and paper "
            "path for wear or obstruction.",
            "We test the connection method you use -- USB, Wi-Fi, or network -- and run "
            "a test print and scan cycle to see exactly where the process breaks down.",
        ],
        "repair_steps": [
            ("Intake and error review", "We note the error codes or symptoms and how the printer connects to your devices."),
            ("Mechanical and connectivity check", "We inspect the print mechanism and test the connection path separately."),
            ("Repair or cleaning", "This may mean a roller or print-head service, a mechanical repair, or a connectivity reconfiguration."),
            ("Test print and handback", "We run a full test print and scan cycle before returning the printer."),
        ],
        "factors": [
            "Parts availability for older or discontinued printer models",
            "The condition of the ink or toner delivery system",
            "Whether the issue is mechanical or a firmware/driver problem, which affects the repair path",
        ],
        "what_to_bring": [
            "The printer and its power cable",
            "A note or photo of any error codes shown on the display",
            "Your Wi-Fi network name if the printer needs to be reconnected (please don't send your Wi-Fi password through the contact form -- we'll ask for it in person if needed)",
        ],
        "related": ["desktop-repair", "buy-sell-trade"],
        "faqs": [
            ("Can you fix a printer that won't connect to Wi-Fi?",
             "In many cases, yes -- this is often a configuration or driver issue rather "
             "than a hardware fault, and we test the connection path directly."),
            ("Is it worth repairing an older printer?",
             "That depends on parts availability for your specific model and the fault "
             "involved. We'll let you know what we find so you can decide."),
        ],
        "disclosure": GENERAL_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "gaming-console-repair",
        "nav_label": "Gaming console repair",
        "h1": "Gaming Console Repair in Surrey, BC",
        "title_tag": f"Gaming Console Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Gaming console repair in Surrey, BC for PlayStation, Xbox, and Nintendo "
            "Switch: power issues, overheating, disc drive faults, and HDMI port damage."
        ),
        "card_summary": "Power, overheating, disc drive, and HDMI issues on PlayStation, Xbox, and Nintendo Switch.",
        "icon": "console",
        "whatsapp_key": "gaming-console-repair",
        "answer": (
            "Smart Geeks repairs game consoles in Surrey, BC across the common "
            "platforms -- power and overheating issues, disc drive faults, HDMI port "
            "damage, and controller sync problems."
        ),
        "overview": [
            "Consoles run hot, run for long stretches, and get moved around more than "
            "most electronics, so power, thermal, and port issues are the most common "
            "faults we see.",
            "We work across PlayStation, Xbox, and Nintendo Switch hardware, and treat "
            "each generation's known failure points differently rather than applying "
            "one generic process to all of them.",
        ],
        "symptoms": [
            "Console won't power on or shows no display output",
            "Overheating and shutting itself off during play",
            "Disc drive not reading discs, or making grinding noises",
            "Controller won't sync or disconnects repeatedly",
            "Damaged or loose HDMI port",
            "Storage errors or corrupted save data",
            "Loud fan noise",
            "Software freezing or repeated crash loops",
        ],
        "diagnostic": [
            "We test the power circuit and check board-level behaviour first, since a "
            "console with no output can fail for reasons ranging from a power fault to "
            "a damaged HDMI port to an internal short.",
            "Thermal system inspection, disc drive mechanism checks, and storage "
            "integrity tests follow, matched to the specific symptom you've described.",
        ],
        "repair_steps": [
            ("Intake", "We note the platform, symptom, and any recent drops, spills, or overheating events."),
            ("Bench diagnostics", "We test power, video output, thermal behaviour, and the disc drive as relevant."),
            ("Repair", "This may be a thermal service, mechanical disc-drive repair, HDMI port replacement, or board-level work."),
            ("Function test and handback", "We confirm the console powers on, outputs video, and runs stable before returning it."),
        ],
        "factors": [
            "Which console generation you have, which affects part availability",
            "How extensive any internal damage is (liquid, drops, prior repair attempts)",
            "Whether the issue is hardware or a software/firmware fault",
        ],
        "what_to_bring": [
            "The console and its power cable",
            "Let us know which platform and model (for example, PS5 disc or digital edition)",
            "Please don't bring or share your account login details -- our diagnostics don't require them",
        ],
        "related": ["motherboard-chip-level-repair", "buy-sell-trade"],
        "faqs": [
            ("Do you repair PS5, Xbox Series X/S, and Nintendo Switch?",
             "Yes, we work across current and several previous console generations. "
             "Let us know your specific model when you get in touch."),
            ("My console shuts off after a while -- is that a thermal issue?",
             "That's a common symptom of dust buildup or degraded thermal paste, but we "
             "test to confirm before assuming that's the cause."),
        ],
        "disclosure": GENERAL_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "macbook-repair",
        "nav_label": "MacBook repair",
        "h1": "MacBook Repair in Surrey, BC",
        "title_tag": f"MacBook Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Independent MacBook repair in Surrey, BC for screens, batteries, "
            "keyboards, charging ports, and logic board issues. Not affiliated with Apple."
        ),
        "card_summary": "Screen, battery, keyboard, charging, and logic board diagnostics for MacBook, MacBook Air, and MacBook Pro.",
        "icon": "macbook",
        "whatsapp_key": "macbook-repair",
        "answer": (
            "Smart Geeks is an independent repair shop that works on MacBook, "
            "MacBook Air, and MacBook Pro models in Surrey, BC -- screens, batteries, "
            "keyboards, charging, and logic board issues. We are not affiliated with Apple."
        ),
        "overview": [
            "MacBooks pack a lot into a thin chassis, which means some faults -- "
            "particularly charging, battery, and logic board issues -- need careful "
            "diagnosis rather than a straight part swap.",
            "As an independent shop, we're upfront that some repairs on tightly "
            "integrated or soldered components are more involved than on a typical "
            "Windows laptop, and we'll explain what that means for your specific model "
            "before starting any work.",
        ],
        "symptoms": [
            "MacBook won't power on",
            "Screen issues: cracked glass, backlight failure, or flickering display",
            "Battery won't hold a charge, or appears swollen",
            "Keyboard keys not registering or a trackpad that misbehaves",
            "Liquid spill on the keyboard or logic board",
            "Charging port not accepting power",
            "Kernel panics, spinning wheel, or the Mac won't boot past the logo",
            "Logic board faults",
        ],
        "diagnostic": [
            "We check for liquid-damage indicators and visible corrosion first, since "
            "that materially changes the diagnostic path, then test the power and "
            "charging circuit.",
            "From there we run a diagnostic boot test and, where the symptoms point to "
            "it, a logic-board-level inspection to identify the specific fault before "
            "discussing repair options with you.",
        ],
        "repair_steps": [
            ("Intake and assessment", "We document the symptoms and any known history (drops, spills, prior repairs)."),
            ("Diagnostic testing", "Power, display, keyboard/trackpad, and logic-board behaviour are tested as relevant to your symptom."),
            ("Repair options", "We explain what we found and what repair paths are realistic for your specific model before proceeding."),
            ("Repair", "Component-level or board-level work, depending on what the diagnostic shows."),
            ("Function test and handback", "We verify the fix under normal use before returning the MacBook."),
        ],
        "factors": [
            "Part availability for your specific MacBook model, especially for older or soldered components",
            "How extensive any liquid damage or corrosion is",
            "Whether the fault is component-level or requires logic-board-level repair",
        ],
        "what_to_bring": [
            "The MacBook and its charger",
            "We recommend signing out of iCloud/Find My My Mac before drop-off where possible, so we can fully test the device",
            "Please don't share your Apple ID password with us -- it's not something our diagnostics need",
        ],
        "related": ["imac-repair", "mac-mini-repair", "motherboard-chip-level-repair"],
        "faqs": [
            ("Is Smart Geeks an authorized Apple repair provider?",
             "No. Smart Geeks is an independent repair shop and is not authorized, "
             "certified, or approved by Apple. We're upfront about that so you can "
             "decide what's right for your situation."),
            ("Can you fix a MacBook with a swollen battery?",
             "A swollen battery is a safety-relevant issue we take seriously. We assess "
             "it on the bench and will explain what we find and the options available."),
            ("Will repairing my MacBook affect my data?",
             "Some repairs (particularly anything involving storage) can carry that "
             "risk. We recommend backing up beforehand whenever that's possible, and "
             "we'll flag it directly if a specific repair carries extra risk to your data."),
        ],
        "disclosure": APPLE_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "imac-repair",
        "nav_label": "iMac repair",
        "h1": "iMac Repair in Surrey, BC",
        "title_tag": f"iMac Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Independent iMac repair in Surrey, BC for power issues, display faults, "
            "storage failure, and internal hardware diagnostics. Not affiliated with Apple."
        ),
        "card_summary": "Power, display, storage, and internal hardware diagnostics for all-in-one iMac desktops.",
        "icon": "imac",
        "whatsapp_key": "imac-repair",
        "answer": (
            "Smart Geeks repairs iMac all-in-one desktops in Surrey, BC -- power "
            "issues, display panel faults, storage failures, and internal hardware "
            "problems. We are an independent shop, not affiliated with Apple."
        ),
        "overview": [
            "An iMac packs the display and internal computer into a single all-in-one "
            "chassis, which makes some repairs more involved than on a separate "
            "monitor-and-tower setup -- opening the unit itself usually means removing "
            "the display.",
            "We take that into account when quoting time and approach, and we'll walk "
            "you through what a given repair actually involves for your iMac's generation.",
        ],
        "symptoms": [
            "iMac won't power on",
            "Display panel issues: no image, dim backlight, or discoloured picture",
            "No video output despite the unit appearing to power on",
            "Loud fan noise or overheating",
            "Signs of hard drive or SSD failure (slow boot, clicking noises, frequent errors)",
            "Won't boot past the startup logo",
            "Ports (USB, Thunderbolt, SD card) not working",
        ],
        "diagnostic": [
            "Because the power supply is built into the chassis on most iMac models, "
            "we test it directly rather than assuming an external cause. We also check "
            "the display panel and backlight independently of the logic board.",
            "Storage diagnostics and an internal thermal inspection round out the "
            "process, since overheating and drive failure are common causes of the "
            "symptoms we see most often.",
        ],
        "repair_steps": [
            ("Intake", "We record the symptom and the iMac's approximate age/generation."),
            ("Diagnostic testing", "Power, display, storage, and thermal behaviour are tested."),
            ("Careful disassembly", "Where the repair requires it, the display is removed following the model's service approach."),
            ("Repair", "Component replacement or board-level work, depending on the fault."),
            ("Reassembly and function test", "We confirm display, power, and I/O all work correctly before handback."),
        ],
        "factors": [
            "Whether your iMac is an Intel or Apple Silicon model, which affects parts and process",
            "Part availability for older iMac generations",
            "Whether the all-in-one design makes a specific repair more time-consuming than the equivalent tower/monitor setup",
        ],
        "what_to_bring": [
            "The iMac and its power cable",
            "Your keyboard and mouse, if the issue involves peripherals",
            "We recommend signing out of iCloud/Find My Mac beforehand where possible",
        ],
        "related": ["macbook-repair", "mac-mini-repair", "motherboard-chip-level-repair"],
        "faqs": [
            ("Can a cracked or dim iMac screen be repaired?",
             "Display panel issues can often be addressed, though the repair involves "
             "careful disassembly since the screen is part of the all-in-one chassis. "
             "We'll explain the process for your specific model."),
            ("Do you work on older iMac models?",
             "We do, though part availability varies by generation -- we'll let you "
             "know during diagnostics whether the part your iMac needs is realistically sourceable."),
        ],
        "disclosure": APPLE_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "mac-mini-repair",
        "nav_label": "Mac mini repair",
        "h1": "Mac Mini Repair in Surrey, BC",
        "title_tag": f"Mac Mini Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Independent Mac mini repair in Surrey, BC for power issues, no-display "
            "faults, overheating, and storage problems. Not affiliated with Apple."
        ),
        "card_summary": "Power, video output, thermal, and storage diagnostics for the compact Mac mini desktop.",
        "icon": "macmini",
        "whatsapp_key": "mac-mini-repair",
        "answer": (
            "Smart Geeks repairs Mac mini desktops in Surrey, BC -- power issues, "
            "no-display faults, overheating, and storage problems. We are an "
            "independent shop and are not affiliated with Apple."
        ),
        "overview": [
            "The Mac mini's compact case means components are tightly packed, which "
            "makes an accurate diagnosis before opening the unit especially important.",
            "We support both Intel-based and Apple Silicon Mac mini generations, and "
            "the diagnostic and repair approach differs between them, particularly for "
            "storage and logic-board work.",
        ],
        "symptoms": [
            "Mac mini won't power on",
            "No video output on any connected display or port",
            "Overheating or unusually loud fan noise",
            "Storage failure signs -- slow performance, errors, or won't boot",
            "Won't boot past the startup screen",
            "Thunderbolt, USB-C, or other port failures",
        ],
        "diagnostic": [
            "We test power delivery first, then check video output across every port "
            "the model supports, since a no-display symptom can come from the cable, "
            "the port, or the internal graphics path.",
            "Storage diagnostics and a thermal inspection follow, since the compact "
            "chassis runs warmer than a full-size tower and heat-related faults are common.",
        ],
        "repair_steps": [
            ("Intake", "We note the symptom and which Mac mini generation you have."),
            ("Diagnostic testing", "Power, video output, storage, and thermal behaviour are checked."),
            ("Repair", "Component-level work or, where necessary, board-level repair."),
            ("Function test and handback", "We confirm the unit boots, outputs video, and runs stable before returning it."),
        ],
        "factors": [
            "Whether your Mac mini is Intel-based or Apple Silicon",
            "Part availability, particularly for older Intel generations",
            "How tightly packed the internal layout is on your specific model, which can affect repair time",
        ],
        "what_to_bring": [
            "The Mac mini and its power cable",
            "Your display cable if the issue is specifically about video output",
            "We recommend signing out of iCloud/Find My Mac beforehand where possible",
        ],
        "related": ["macbook-repair", "imac-repair", "motherboard-chip-level-repair"],
        "faqs": [
            ("Do you repair both Intel and Apple Silicon Mac mini models?",
             "Yes, though the diagnostic and repair process differs between them -- "
             "let us know your model when you reach out."),
            ("My Mac mini has no display output on any port -- can that be fixed?",
             "That's a symptom we test for specifically, checking cables, ports, and "
             "the internal video path. We'll explain what we find before recommending a repair."),
        ],
        "disclosure": APPLE_DISCLOSURE,
    },
    # ------------------------------------------------------------------ #
    {
        "slug": "motherboard-chip-level-repair",
        "nav_label": "Motherboard & chip-level repair",
        "h1": "Motherboard and Chip-Level Repair in Surrey, BC",
        "title_tag": f"Motherboard & Chip-Level Repair in {CITY}, BC | Smart Geeks",
        "meta_description": (
            "Chip-level motherboard and logic board repair in Surrey, BC: charging "
            "port and power diagnostics, liquid-damage boards, and no-power faults."
        ),
        "card_summary": "Board-level diagnostics, charging-port and power-circuit repair, and liquid-damage board recovery.",
        "icon": "chip",
        "whatsapp_key": "motherboard-chip-level-repair",
        "answer": (
            "Smart Geeks offers chip-level motherboard and logic board repair in "
            "Surrey, BC for devices that won't power on, won't charge, or have "
            "suffered liquid or short-circuit damage that a simple part swap won't fix."
        ),
        "overview": [
            "This is our most technical repair category, covering laptop motherboards, "
            "Mac logic boards, and desktop boards at the component level -- charging "
            "ports, power circuits, and micro-soldering work -- rather than at the "
            "whole-board-replacement level.",
            "Chip-level repair is genuinely more involved and carries more variability "
            "than a straightforward part swap. We assess each board on its own merits "
            "and explain honestly what's realistic before any work begins, including "
            "when a board is too far gone to recover economically.",
        ],
        "symptoms": [
            "Device is completely dead with no signs of power",
            "Charging port is loose, damaged, or the device won't charge despite a working cable",
            "Device still won't power on after liquid exposure, even once dried out",
            "Visible board damage, burning smell, or discoloured components",
            "Intermittent power -- the device powers on sometimes and not others",
            "Device shorts out or a charger reports an unusual current draw",
        ],
        "diagnostic": [
            "We inspect the board under magnification for visible damage or corrosion, "
            "then use multimeter and continuity testing to trace power rails and "
            "identify where the circuit is failing.",
            "For liquid-damage cases specifically, we look for corrosion patterns and "
            "shorted components, since the visible damage often doesn't match where "
            "the actual fault is.",
        ],
        "repair_steps": [
            ("Intake and honest risk disclosure", "We explain upfront that chip-level repair on a severely damaged board isn't always possible, and that we'll stop and tell you if that's the case."),
            ("Board-level diagnostic", "Multimeter testing and visual inspection identify the specific failure point."),
            ("Targeted component repair", "This may include charging-port replacement, capacitor or IC-level work, or corrosion cleanup, depending on the fault."),
            ("Power and function test", "We verify the board holds power and the device functions normally under test."),
            ("Findings report", "If a board can't be economically recovered, we'll tell you that directly rather than continuing to bill for further attempts."),
        ],
        "factors": [
            "The severity of corrosion or physical damage, which is the single biggest factor in whether chip-level repair is realistic",
            "Availability of the specific component that needs replacing",
            "Whether the board is a laptop motherboard, Mac logic board, or desktop board, which changes tooling and approach",
        ],
        "what_to_bring": [
            "The device itself, along with its charger if the fault is charging-related",
            "Any details you have about what happened (a spill, a drop, a burning smell) -- this genuinely helps narrow the diagnosis",
        ],
        "related": ["laptop-repair", "macbook-repair", "desktop-repair"],
        "faqs": [
            ("Can every board be repaired at the chip level?",
             "No, and we won't pretend otherwise. Severely corroded or physically "
             "damaged boards sometimes can't be recovered economically. We assess each "
             "board individually and tell you honestly what we find."),
            ("What's the difference between chip-level repair and a normal repair?",
             "A normal repair usually swaps a whole part (a screen, a battery, a whole "
             "board). Chip-level repair works on individual components on the board "
             "itself -- a charging port, a capacitor, a damaged trace -- which takes "
             "more specialized diagnostic work."),
            ("My phone or tablet charging port is damaged -- do you handle that?",
             "Our chip-level and charging-port work is focused on the laptop, desktop, "
             "and Mac categories we specialize in. Get in touch and we can let you know "
             "whether your specific device is something we can take on."),
        ],
        "disclosure": GENERAL_DISCLOSURE,
    },
]


BUY_SELL_TRADE = {
    "slug": "buy-sell-trade",
    "nav_label": "Buy, sell & trade",
    "h1": "Buy, Sell, and Trade Electronics in Surrey, BC",
    "title_tag": f"Buy, Sell & Trade Electronics in {CITY}, BC | Smart Geeks",
    "meta_description": (
        "Buy, sell, or trade laptops, desktops, Mac computers, and gaming consoles "
        "at Smart Geeks in Surrey, BC. Bring your device in for an assessment."
    ),
    "card_summary": "Bring in laptops, desktops, Mac computers, and consoles to buy, sell, or trade.",
    "icon": "trade",
    "whatsapp_key": "buy-sell-trade",
    "answer": (
        "Smart Geeks buys, sells, and trades laptops, desktop computers, Mac "
        "computers, and gaming consoles in Surrey, BC. Bring your device in and "
        "we'll assess it in person before making an offer."
    ),
    "overview": [
        "If you have a working or lightly-faulty device you no longer need, or "
        "you're looking for a tested used device instead of buying new, we handle "
        "both sides of that at our Surrey location.",
        "Every device is assessed in person -- we don't quote a value sight unseen, "
        "since condition, age, and working order all affect what makes sense for both sides.",
    ],
    "what_we_accept": [
        "Laptops (Windows and MacBook)",
        "Desktop computers and Mac desktops (iMac, Mac mini)",
        "Gaming consoles and accessories",
        "Working, lightly faulty, or outdated devices you're ready to part with",
    ],
    "assessment_process": [
        ("Bring your device in", "Drop by with the device and, if you have it, its charger or power cable."),
        ("In-person inspection", "We check functionality, condition, and specs relevant to current demand."),
        ("An offer, explained", "We'll walk you through how we arrived at the offer, so it isn't a black box."),
        ("Your decision", "You decide whether to move forward -- there's no obligation to accept."),
    ],
    "factors": [
        "The device's working condition and any faults present",
        "Age and current demand for that specific model",
        "Whether accessories (charger, original packaging) are included",
        "Data-wiping: we recommend backing up and signing out of any accounts before bringing a device in to trade or sell",
    ],
    "what_to_bring": [
        "The device and its charger or power cable, if you have it",
        "Please back up your data and sign out of accounts (iCloud, Google, Microsoft) beforehand",
        "Valid ID may be requested as part of our standard intake process",
    ],
    "sustainability_note": (
        "Keeping working electronics in use, and recycling the ones that aren't, "
        "keeps them out of landfill longer -- that's part of why we offer this "
        "alongside our repair work rather than as a separate business."
    ),
    "related": ["laptop-repair", "desktop-repair", "motherboard-chip-level-repair"],
    "faqs": [
        ("Do you buy broken devices?",
         "Sometimes, depending on the device and fault -- bring it in and we'll let "
         "you know honestly whether it's something we can take."),
        ("Can I trade my old laptop toward a repair?",
         "Get in touch and describe both the device you'd trade and the repair you're "
         "considering, and we'll talk through whether that makes sense."),
        ("Do you sell used, tested devices?",
         "Yes -- when we have tested used devices available, they're sold in person "
         "at our Surrey location."),
    ],
    "disclosure": GENERAL_DISCLOSURE,
}


def all_service_slugs():
    return [s["slug"] for s in SERVICES] + [BUY_SELL_TRADE["slug"]]


def get_service(slug):
    for s in SERVICES:
        if s["slug"] == slug:
            return s
    if BUY_SELL_TRADE["slug"] == slug:
        return BUY_SELL_TRADE
    return None
