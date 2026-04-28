# DoseKeeper — Privacy Policy

_Last updated: 2026-04-27_

DoseKeeper helps you track medications and supplements, see your schedule, log doses, and (optionally) share supply status with people you trust. This document explains what we collect, what we do with it, and how to get it back or delete it.

We are intentionally narrow: data is collected only to make the app work for you. We do not sell, rent, or share your data with advertisers, and we do not use third-party analytics or tracking SDKs.

## 1. Who runs DoseKeeper

DoseKeeper is built and operated by **Jonas Enterprises**.
Contact: **K2@jonasenterprises.com**

## 2. What we collect

We collect only what's needed to run the features you use.

| Data | Why | Source |
|---|---|---|
| Email address | Sign in, password reset, sending you reminder/refill emails if you turn that on | You, at sign-up |
| Display name | Personalized greetings (e.g. "Good morning, Kevin") | You, in Settings |
| Timezone | Anchoring schedules and reminders to your local day | You, in Settings (defaults to your device) |
| Daily routine times | Mapping "morning / lunch / dinner / bedtime" slots to clock times | You, in Settings |
| Medications, supplements, peptides | The list of items you track — name, brand, strength, form, prescriber notes, inventory, schedule | You, in the Library |
| Dose history | Whether each dose was taken / skipped / snoozed, and when | You, on the Today screen |
| Trips | Planned trips and pack-list math | You, in Trips |
| Caretaker links | Invite codes you create or redeem, plus the resulting relationships and the permissions you grant each caretaker | You, in Caregiving / Permissions |
| Order requests | When you ask a caretaker to reorder for you, or when you act as someone's orderer | You, in Library / Orderer |
| Push notification token | Sending dose reminders and reorder alerts to this specific device | Your device, when you enable push notifications |
| Pharmacy / source preferences | Surfacing the right reorder link when supply runs low | You, in the Library |

We do **not** collect: precise location, contacts, photos beyond what you scan during bottle OCR (and that scan stays on your device — only the parsed fields you confirm are saved), advertising identifiers, analytics events, screen recordings, or any data from other apps.

## 3. How we use what we collect

Everything above is used to operate the features you actually see in the app:

- Showing your supplements and dose schedules.
- Sending reminders and reorder alerts to the channels you enable.
- Letting caretakers you've invited see what you've authorized them to see.
- Placing or relaying reorder requests through links / pharmacy integrations you set up.
- Restoring your data when you sign in on a new device.

We do not profile you, score you, or feed your data into machine-learning training sets.

## 4. Where it lives

DoseKeeper stores data in a Supabase-managed Postgres database hosted on Amazon Web Services (AWS) infrastructure. Supabase acts as our processor; access is restricted by Postgres row-level security so that only your account (and caretakers you've explicitly authorized) can read your rows.

Push notifications are delivered through the Apple Push Notification service (APNs). The push token tied to your device is stored alongside your account so the server knows where to send a reminder.

If you enable a third-party pharmacy integration (e.g., Walgreens) we send only the fields that integration needs to deep-link a refill (typically supplement name + your store identifier you provided). We don't sit between your pharmacy and you on an ongoing basis.

If you set a manual reorder URL or use Amazon-search-based reorder, tapping that link opens the third party in your browser/app; from that point their privacy policy applies.

## 5. Sharing with third parties

We do not sell or rent your data, and we do not share it with advertisers, data brokers, or analytics vendors.

Limited operational sharing:

- **Supabase** — managed database & auth provider. Stores your data on our behalf under a Data Processing Agreement.
- **Apple Push Notification service** — delivers reminders to your device.
- **People you invite** — caretakers and orderers see what you authorize them to see, and only that. You can revoke access at any time in Settings → Permissions.

## 6. Children

DoseKeeper is intended for adults managing their own medications or assisting another adult. It is not directed at children under 13. If a parent or guardian is using the app on behalf of a child, the data lives under the adult's account.

## 7. Your rights

You can:

- **Access / export** your data — the History screen has a CSV export of your full dose log.
- **Edit / delete individual items** — supplements, schedules, trips, caretakers, doses, etc. all have inline edit/delete.
- **Revoke caretaker access** — Settings → Who can help, then Remove or downgrade.
- **Sign out** — Settings → Sign out.
- **Delete your account** — email **K2@jonasenterprises.com** with the email address tied to your account; we will delete your profile, supplements, doses, schedules, trips, caretaker links, and push subscriptions within 14 days of receiving the request. (Auth records that we are legally required to retain for tax or fraud-prevention purposes will be retained only for those purposes.)

If you live in a jurisdiction with formal data-subject rights (GDPR, UK GDPR, CCPA / CPRA, etc.), the rights above already satisfy access, correction, deletion, and portability. Contact us if you'd like a written response.

## 8. Security

- All transit is HTTPS / TLS.
- Authentication uses one-time email links / passwords managed by Supabase Auth.
- Database access is gated by Postgres row-level security on every table.
- Push payloads contain only the supplement name + slot, never sensitive prescription notes or dosing rationale.

No system is perfectly secure. If we ever detect a breach affecting your data we will notify you by email at the address tied to your account.

## 9. Changes to this policy

If we materially change what we collect or how we use it, we will update the "Last updated" date at the top of this document and surface a notice in the app on next launch.

## 10. Questions

Email **K2@jonasenterprises.com**. We read every message.
