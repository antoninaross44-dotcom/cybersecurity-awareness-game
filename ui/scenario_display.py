"""Scenario display renderers.

Each function takes a tkinter parent frame and a display_data dict, and
builds a small, realistic-looking mockup of the thing the scenario is
about — a fake email, a text message, an incoming call, or a lookalike
login page. This is what makes FR4 ("present realistic but simulated
scenarios") actually visible to the player, instead of just describing
the scenario in a paragraph of text.

Each render_* function returns nothing — it just packs widgets into the
frame it's given. Call clear_and_render() from the UI layer; it picks the
right renderer based on challenge.scenario_type, or falls back to plain
text for scenario_type == "generic".
"""

import tkinter as tk

_EMAIL_BG = "#f4f4f4"
_EMAIL_HEADER_BG = "#e8e8e8"
_SMS_BUBBLE_BG = "#d9f7c4"
_CALL_BG = "#1a2b4c"
_BROWSER_CHROME_BG = "#e0e0e0"
_DANGER_TEXT = "#8a1f1f"


def clear_and_render(frame: tk.Frame, challenge) -> None:
    """Clear the frame, then render the right mockup for this challenge."""
    for widget in frame.winfo_children():
        widget.destroy()

    renderer = _RENDERERS.get(challenge.scenario_type, _render_generic)
    renderer(frame, challenge.display_data)


def _render_generic(frame: tk.Frame, data: dict) -> None:
    # No special mockup — used for password and quiz challenges, where the
    # question itself (shown separately by the caller) is enough.
    pass


def _render_email(frame: tk.Frame, data: dict) -> None:
    card = tk.Frame(frame, bg=_EMAIL_BG, highlightbackground="#bbbbbb", highlightthickness=1)
    card.pack(fill="x", pady=(0, 4))

    header = tk.Frame(card, bg=_EMAIL_HEADER_BG)
    header.pack(fill="x")

    tk.Label(
        header, bg=_EMAIL_HEADER_BG, anchor="w", justify="left", font=("Arial", 10, "bold"),
        text=f"From: {data.get('from_name', '')} <{data.get('from_address', '')}>"
    ).pack(fill="x", padx=10, pady=(8, 0))

    tk.Label(
        header, bg=_EMAIL_HEADER_BG, anchor="w", justify="left", font=("Arial", 11, "bold"),
        text=data.get("subject", "")
    ).pack(fill="x", padx=10, pady=(2, 8))

    tk.Label(
        card, bg=_EMAIL_BG, anchor="w", justify="left", font=("Arial", 10),
        wraplength=460, text=data.get("body", "")
    ).pack(fill="x", padx=10, pady=10)


def _render_sms(frame: tk.Frame, data: dict) -> None:
    tk.Label(
        frame, anchor="w", font=("Arial", 9), fg="#555555",
        text=f"Text message from {data.get('sender', '')}"
    ).pack(fill="x", pady=(0, 4))

    bubble_row = tk.Frame(frame)
    bubble_row.pack(fill="x")

    bubble = tk.Label(
        bubble_row, bg=_SMS_BUBBLE_BG, anchor="w", justify="left", font=("Arial", 10),
        wraplength=340, text=data.get("message", ""), padx=12, pady=10
    )
    bubble.pack(side="left")


def _render_phone_call(frame: tk.Frame, data: dict) -> None:
    card = tk.Frame(frame, bg=_CALL_BG)
    card.pack(fill="x", pady=(0, 4))

    tk.Label(
        card, bg=_CALL_BG, fg="white", font=("Arial", 9),
        text="\u260E  Incoming call"
    ).pack(pady=(10, 0))

    tk.Label(
        card, bg=_CALL_BG, fg="white", font=("Arial", 13, "bold"),
        text=data.get("caller_name", "Unknown Caller")
    ).pack()

    tk.Label(
        card, bg=_CALL_BG, fg="#cccccc", font=("Arial", 10),
        text=data.get("caller_number", "")
    ).pack(pady=(0, 10))

    tk.Label(
        frame, anchor="w", justify="left", font=("Arial", 10, "italic"),
        wraplength=460, fg="#333333", text=data.get("call_note", "")
    ).pack(fill="x", pady=(8, 0))


def _render_login_page(frame: tk.Frame, data: dict) -> None:
    browser = tk.Frame(frame, highlightbackground="#bbbbbb", highlightthickness=1)
    browser.pack(fill="x", pady=(0, 4))

    chrome = tk.Frame(browser, bg=_BROWSER_CHROME_BG)
    chrome.pack(fill="x")

    address_bar = tk.Label(
        chrome, bg="white", fg=_DANGER_TEXT, font=("Consolas", 10), anchor="w",
        text=data.get("url", ""), padx=8, pady=4
    )
    address_bar.pack(fill="x", padx=8, pady=6)

    page_body = tk.Frame(browser, bg="white")
    page_body.pack(fill="x", pady=20)

    tk.Label(page_body, bg="white", font=("Arial", 14, "bold"), text=data.get("logo_text", "")).pack(pady=(10, 4))
    tk.Label(page_body, bg="white", font=("Arial", 11), text=data.get("page_title", "")).pack(pady=(0, 12))

    fake_field = tk.Entry(page_body, width=30, state="disabled")
    fake_field.pack(pady=4)
    fake_field2 = tk.Entry(page_body, width=30, show="*", state="disabled")
    fake_field2.pack(pady=4)


_RENDERERS = {
    "email": _render_email,
    "sms": _render_sms,
    "phone_call": _render_phone_call,
    "login_page": _render_login_page,
    "generic": _render_generic,
}
