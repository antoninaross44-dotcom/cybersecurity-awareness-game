-- Seed data. db.py only runs this file once — the FIRST time the database
-- is created — so this never causes duplicates on later launches.

INSERT INTO modules (name, type) VALUES ('Password & Account Security', 'password');

-- Challenge 1: password strength
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    1,
    'You are creating a new online account. Which password is safest to use?',
    1,
    'Correct! Long, random passphrases are much harder to crack than short, predictable ones.',
    'Not quite. That password is short and easy to guess. A longer, random passphrase is much safer.'
);
INSERT INTO response_options (challenge_id, text) VALUES (1, 'Tr0ub4dor&3-Xk!mPz9qL');
INSERT INTO response_options (challenge_id, text) VALUES (1, 'password123');

-- Challenge 2: password reuse
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    1,
    'You use the exact same password for your email and your mobile money app. Is this safe?',
    4,
    'Correct. Reusing one password everywhere means a single breach can expose every account that shares it.',
    'Not quite. If one of these accounts is breached, attackers will try the same password on the other.'
);
INSERT INTO response_options (challenge_id, text) VALUES (2, 'Yes, it is easier to remember one password');
INSERT INTO response_options (challenge_id, text) VALUES (2, 'No, each account should have its own password');

-- Challenge 3: multi-factor authentication
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    1,
    'An app offers to turn on two-factor authentication (2FA) for your account. What should you do?',
    5,
    'Correct. 2FA adds a second layer of protection, so a stolen password alone is not enough to break in.',
    'Not quite. A password alone can be guessed, leaked, or reused elsewhere. 2FA protects you even if that happens.'
);
INSERT INTO response_options (challenge_id, text) VALUES (3, 'Turn it on, it adds an extra layer of protection');
INSERT INTO response_options (challenge_id, text) VALUES (3, 'Skip it, my password is already enough');

-- Challenge 4: remembering many passwords
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    1,
    'You have accounts on many different sites and are struggling to remember unique passwords for each. What is the safest solution?',
    8,
    'Correct. A password manager generates and stores a unique, strong password for every account, so you only need to remember one.',
    'Not quite. Using one simple password everywhere means a breach on one site puts every other account at risk too.'
);
INSERT INTO response_options (challenge_id, text) VALUES (4, 'Use the same simple password on every site');
INSERT INTO response_options (challenge_id, text) VALUES (4, 'Use a password manager to generate a unique password for each site');

-- ============================================================
-- Module 2: Phishing & Social Engineering
-- Each challenge includes scenario_type + display_data so the UI can render
-- a realistic mockup (fake email / SMS / call / login page) instead of a
-- plain paragraph of text.
-- ============================================================
INSERT INTO modules (name, type) VALUES ('Phishing & Social Engineering', 'phishing');

-- Challenge 5: fake bank email
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect, scenario_type, display_data)
VALUES (
    2,
    'What should you do with this email?',
    10,
    'Correct. Banks never ask you to verify details through an emailed link. Go to the bank''s website directly, or call them, instead.',
    'Not quite. This is a classic phishing tactic. Clicking the link and entering your details could hand your login straight to an attacker.',
    'email',
    '{"from_name": "SecureBank Support", "from_address": "support@securebank-verify.com", "subject": "URGENT: Your account will be suspended", "body": "Dear Customer,\n\nWe detected unusual activity on your account. Click the link below within 24 hours to verify your details, or your account will be suspended.\n\n[ Verify My Account ]\n\nSecureBank Security Team"}'
);
INSERT INTO response_options (challenge_id, text) VALUES (5, 'Click the link and enter my details to avoid losing access');
INSERT INTO response_options (challenge_id, text) VALUES (5, 'Do not click the link; log in to the bank''s website directly instead');

-- Challenge 6: prize/lottery scam SMS
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect, scenario_type, display_data)
VALUES (
    2,
    'What should you do with this message?',
    12,
    'Correct. Urgent deadlines and requests for personal ID numbers by text are a common scam pattern, not a real prize.',
    'Not quite. Legitimate prizes do not demand your NRC number under a tight deadline by text message. This pressure is designed to stop you thinking it through.',
    'sms',
    '{"sender": "+260-77-000-1234", "message": "CONGRATULATIONS! You''ve WON K5,000 in the Airtel Lucky Draw! Reply with your NRC number within 1 HOUR to claim your prize. Offer expires soon!"}'
);
INSERT INTO response_options (challenge_id, text) VALUES (6, 'Reply immediately with my NRC number so I do not miss the deadline');
INSERT INTO response_options (challenge_id, text) VALUES (6, 'Ignore or delete the message, this is a common scam');

-- Challenge 7: vishing (voice phishing) requesting OTP
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect, scenario_type, display_data)
VALUES (
    2,
    'What should you do on this call?',
    14,
    'Correct. Legitimate providers never ask you to read out an OTP over the phone. Sharing it can let an attacker take over your account.',
    'Not quite. An OTP is meant to prove it is really you, only to you. Reading it out to a caller gives them exactly what they need to break in.',
    'phone_call',
    '{"caller_name": "Unknown Caller", "caller_number": "+260-96-XXX-XXXX", "call_note": "\"Hello, this is MTN Customer Support. We''re verifying your SIM card. Can you please read out the one-time PIN you just received by text?\""}'
);
INSERT INTO response_options (challenge_id, text) VALUES (7, 'Read out the OTP since they already know my phone number');
INSERT INTO response_options (challenge_id, text) VALUES (7, 'Refuse to share the OTP and hang up; legitimate providers never ask for it');

-- Challenge 8: fake/lookalike login page
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect, scenario_type, display_data)
VALUES (
    2,
    'What should you do on this page?',
    16,
    'Correct. A slightly misspelled address is a strong sign of a fake login page designed to steal your password. Always check the URL before entering credentials.',
    'Not quite. A convincing-looking page is not proof it is genuine. Entering your password here would hand it straight to an attacker.',
    'login_page',
    '{"url": "https://mail-gmai1.com/login", "page_title": "Sign in to continue", "logo_text": "Mail"}'
);
INSERT INTO response_options (challenge_id, text) VALUES (8, 'Enter my username and password since the page looks correct');
INSERT INTO response_options (challenge_id, text) VALUES (8, 'Check the web address carefully and close the page if it looks wrong');

-- ============================================================
-- Module 3: Cybersecurity Quizzes & Decision Challenges
-- ============================================================
INSERT INTO modules (name, type) VALUES ('Quizzes & Decision Challenges', 'quiz');

-- Challenge 9: quiz — definition of phishing
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    3,
    'What does "phishing" mean in cybersecurity?',
    17,
    'Correct. Phishing is a technique attackers use to trick people into revealing passwords, PINs or other sensitive information.',
    'Not quite. That describes a different kind of threat. Phishing specifically means tricking people into revealing sensitive information.'
);
INSERT INTO response_options (challenge_id, text) VALUES (9, 'A technique used to trick people into revealing sensitive information');
INSERT INTO response_options (challenge_id, text) VALUES (9, 'A type of virus that automatically deletes files');

-- Challenge 10: quiz — why update software
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    3,
    'Why is it important to keep your software and apps updated?',
    20,
    'Correct. Updates often patch security weaknesses that attackers could otherwise exploit to break in.',
    'Not quite. Updates are not just cosmetic — many of them fix real security weaknesses.'
);
INSERT INTO response_options (challenge_id, text) VALUES (10, 'Updates only change how the app looks');
INSERT INTO response_options (challenge_id, text) VALUES (10, 'Updates often fix security weaknesses that attackers could exploit');

-- Challenge 11: quiz — definition of social engineering
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    3,
    'What best describes "social engineering" in cybersecurity?',
    21,
    'Correct. Social engineering means manipulating people, not computers, into giving up confidential information or access.',
    'Not quite. Social engineering targets people''s trust and behaviour, not computer code.'
);
INSERT INTO response_options (challenge_id, text) VALUES (11, 'Manipulating people into giving up confidential information or access');
INSERT INTO response_options (challenge_id, text) VALUES (11, 'Writing computer programs for social media platforms');

-- Challenge 12: decision-making challenge — USB drop attack
INSERT INTO challenges (module_id, description, correct_option_id, feedback_correct, feedback_incorrect)
VALUES (
    3,
    'You find a USB drive labelled "Salary Report 2026" in the office car park. What should you do?',
    24,
    'Correct. Unknown USB drives can contain malware set up to run automatically. Handing it to IT/security keeps you and the organisation safe.',
    'Not quite. This is a known attack technique: attackers leave infected USB drives for curious people to plug in, which can silently install malware.'
);
INSERT INTO response_options (challenge_id, text) VALUES (12, 'Plug it into my computer to see who it belongs to');
INSERT INTO response_options (challenge_id, text) VALUES (12, 'Hand it to IT or security without plugging it into any device');

-- ============================================================
-- Tips: content library used by FR19 (personalised recommendations).
-- 3 tips per module, shown when the user performs poorly in that module.
-- ============================================================
INSERT INTO tips (module_id, tip_text) VALUES (1, 'Use a unique password for every account. A password manager makes this easy to manage without memorising dozens of passwords.');
INSERT INTO tips (module_id, tip_text) VALUES (1, 'Turn on two-factor authentication (2FA) wherever it is offered. It protects your account even if your password leaks.');
INSERT INTO tips (module_id, tip_text) VALUES (1, 'Avoid predictable patterns like birthdays or "password123". Aim for long, random passphrases instead.');

INSERT INTO tips (module_id, tip_text) VALUES (2, 'Always check the sender''s actual email address, not just the display name. Attackers often spoof familiar-looking names.');
INSERT INTO tips (module_id, tip_text) VALUES (2, 'Never share a one-time PIN (OTP) with anyone who calls or messages you, even if they claim to be your provider.');
INSERT INTO tips (module_id, tip_text) VALUES (2, 'Before clicking a link, check where it really goes. Look for misspelled domains, like "gmai1" instead of "gmail".');

INSERT INTO tips (module_id, tip_text) VALUES (3, 'If a message creates urgency or pressure to act immediately, slow down. That pressure is often the scam itself.');
INSERT INTO tips (module_id, tip_text) VALUES (3, 'Unknown USB drives, links, or attachments should never be opened out of curiosity. Report them instead.');
INSERT INTO tips (module_id, tip_text) VALUES (3, 'Keep your software updated. Many updates patch security holes that attackers are actively exploiting.');
