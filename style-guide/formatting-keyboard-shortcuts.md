---
title: Formatting Keyboard Shortcuts
type: Style guide
original_format: PDF (internal style guide page)
---

> **Why this is here.** A style guide entry is a small thing that has to survive
> many writers and many years. This one picks a rule for every case someone might
> hit, shows the wrong version next to the right one, and cites the platform
> guidelines it follows so the rule is arguable on evidence instead of taste.

# How to format keyboard shortcuts

Hiya! Here's a guide on how we format keyboard shortcuts.

- Don't abbreviate
- Capitalize key names
- Use the proper separators
- Use bold to highlight keys in sentences
- List groups of shortcuts in a table
- Use the correct order for multi-key combinations
- Describe primary, (then secondary)
- Symbol keys
- Single character keys

## Don't abbreviate

Go long! Use the full, single word name of the key. Do not use symbols or abbreviations (`Fn`, `Cmd`, `ScLk`). See the full list of keys and names below for reference.

This method uses more characters, but reduces confusion and enables screen readers to speak the key name. For multi-word key names, write it out.

| Do this | Don't do this |
|---|---|
| <kbd>Control</kbd> | <kbd>Ctrl</kbd> |
| <kbd>Caps Lock</kbd> | <kbd>Caps</kbd> |
| <kbd>Command</kbd> | |

## Capitalize key names

Single-letter keys are written as a single capital letter.

Use Camel Case for single- or multi-word key names. This helps these types of key names stand out among other text.

| Do this | Don't do this |
|---|---|
| Press the <kbd>Q</kbd> key to mark as code. | Press the q key to mark as code. |
| Hold <kbd>Control</kbd> to dispense a widget. | Hold control to dispense a widget. |
| Scream at your co-workers with <kbd>Caps Lock</kbd>. | Scream at your co-workers with caps lock. |

## Use the proper separators

We use `+` (plus) as our separator character.

Group key names with space + space between keys. The space gives the keys room to breathe, and the plus `+` connects them.

| Do this | Don't do this |
|---|---|
| <kbd>Control</kbd> + <kbd>Z</kbd> | Control+Z |
| <kbd>Shift</kbd> + <kbd>Backspace</kbd> | Shift+Backspace |

## Use bold to highlight keys in sentences

When describing a keypress alongside other text, use bold to callout the key sequence. This includes the `+` separator.

If we don't highlight the keypress, a user can't scan for it, and it's easily lost in the sea of letters. How sad!

| Do this | Don't do this |
|---|---|
| Marcia couldn't grasp that **Control + V** is paste. | Marcia couldn't grasp that Control + V is paste. |
| Just press the **Space Bar**, ya dingus. | Just press the Space Bar, ya dingus. |
| Judicious use of **Delete** can save your life. | Judicious use of Delete can save your life. |

## List groups of shortcuts in a table

When describing a bunch of keyboard shortcuts at a time, take the time to put them in a table for clarity.

Group shortcuts by function, and start the line with the OS for each (Windows and Mac assumed in this example).

Here's a sample:

| Action | Shortcut |
|---|---|
| Lower the brightness one unit. | Windows: <kbd>Control</kbd> + <kbd>F4</kbd><br>Mac: <kbd>Command</kbd> + <kbd>F4</kbd> |
| Paste an image into the document. | Windows: <kbd>Control</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd><br>Mac: <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd> |
| Display a full-color photo of Nic Cage. | Windows: <kbd>Control</kbd> + <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>K</kbd><br>Mac: <kbd>Option</kbd> + <kbd>Shift</kbd> + <kbd>Command</kbd> + <kbd>K</kbd> |

## Use the correct order for multi-key combinations

Yes, there's a correct* order for listing multi-key shortcuts! As a best practice, we describe them in this sequence.

- Windows order is Control, Alt, Shift, Other
- Mac order is Control, Option, Shift, Command, Other

| Do this | Don't do this |
|---|---|
| <kbd>Control</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd> | Shift + Control + V |
| <kbd>Control</kbd> + <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>K</kbd> | Alt + Control + Shift + K |
| <kbd>Control</kbd> + <kbd>Option</kbd> + <kbd>9</kbd> | Option + Control + 9 |
| <kbd>Option</kbd> + <kbd>Command</kbd> + <kbd>Y</kbd> | Command + Option + Y |

\* See Microsoft's Guidelines for Keyboard User Interface Design and Apple's Human Interface Guidelines.

## Describe primary, (then secondary)

When writing out shortcuts in a sentence, call out the primary OS shortcut, followed by the secondary OS.

Windows is primary, Mac secondary. The name "Windows" is assumed as the primary.

Use this format:

> To dispense a pickle from the pickle machine, press **Alt + Shift + P** (Option + Shift + P on Mac).
>
> To copy the widgets, press **Control + C** (Command + C on Mac).

## Symbol keys

When describing symbol keys, we simply use the symbol itself, and not the name of the key. It's best to include the word "key" to be clear.

| Do this | Don't do this |
|---|---|
| Press the `` ` `` key to toggle the terminal. | Press backtick to toggle the terminal. |
| Hold the `&` key to make a giraffe appear. | Hold the ampersand key to make a giraffe appear. |

## Single character keys

When describing a single character key, include the word "key" to be clear.

| Do this | Don't do this |
|---|---|
| Press the <kbd>Z</kbd> key to summon a genie. | Press Z to summon a genie. |
| Hold the <kbd>H</kbd> key to use the laser pointer. Pew pew! | Hold H to use the laser pointer. Pew pew! |

---

*Internal style guide documentation.*
