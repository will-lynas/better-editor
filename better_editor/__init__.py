import os
from aqt import mw
from aqt import gui_hooks
from aqt.editor import Editor


def get_absolute_path(relative_path: str) -> str:
    file_dir = os.path.dirname(__file__)
    return os.path.join(file_dir, relative_path)


def reset_all_fields(editor: Editor) -> None:
    """Turn off sticky for all fields, and clear all fields."""
    note = editor.note
    if not note or not mw:
        return
    note_type = note.note_type()
    if not note_type:
        return

    fields = note_type["flds"]
    for field in fields:
        note[field["name"]] = ""
        field["sticky"] = False
    editor.loadNoteKeepingFocus()


def toggle_all_sticky(editor: Editor) -> None:
    """If any field is sticky, turn sticky off for all fields. Else, turn on for all fields."""

    note = editor.note
    if not note or not mw:
        return
    note_type = note.note_type()
    if not note_type:
        return

    fields = note_type["flds"]
    if any(field["sticky"] for field in fields):
        for field in fields:
            field["sticky"] = False
    else:
        for field in fields:
            field["sticky"] = True
    editor.loadNoteKeepingFocus()


def add_buttons(buttons: list[str], editor: Editor) -> None:

    # reset_fields
    icon = get_absolute_path("red_cross.png")
    hotkey = "Ctrl+F9"
    b = editor.addButton(
        icon,
        "reset_all_fields",
        reset_all_fields,
        tip=f"Reset all fields ({hotkey})",
        keys=hotkey
    )
    buttons.append(b)

    # toggle_all_sticky
    icon = get_absolute_path("pin.png")
    hotkey = "Shift+F9"
    b = editor.addButton(
        icon,
        "toggle_all_sticky",
        toggle_all_sticky,
        tip=f"Toggle sticky on all fields ({hotkey})",
        keys=hotkey
    )
    buttons.append(b)


gui_hooks.editor_did_init_buttons.append(add_buttons)
