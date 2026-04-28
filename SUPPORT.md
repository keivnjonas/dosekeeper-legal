# DoseKeeper — Support

Thanks for using DoseKeeper. If something isn't working, here's the fastest way to get help.

## Contact

- **Email:** K2@jonasenterprises.com
- **Bug reports / feature requests:** [GitHub Issues](https://github.com/keivnjonas/dosekeeper/issues)

We typically reply within 1–2 business days.

## Common questions

### My reminders aren't arriving

1. Open **Settings** in DoseKeeper and confirm **Push reorder alerts** and **Dose reminders** are both on.
2. Open the iOS **Settings** app → **Notifications** → **DoseKeeper**, and confirm notifications are allowed.
3. If you recently changed devices, tap the push toggle off and back on in DoseKeeper Settings to refresh the device registration.
4. Check that the time on your phone matches your real timezone. DoseKeeper anchors schedules to the timezone in **Settings → Profile**.

### I logged a dose by mistake

- On the **Today** screen, long-press a dose row and choose **Mark pending** to undo. If you used **Mark all**, an Undo toast appears for 5 seconds at the bottom of the screen.

### I can't find an old dose

- Go to **History** to see the last 90 days. For longer windows or to share with a doctor, use **Export CSV** at the bottom of History (30 / 90 / 365 day ranges).

### How do I let a family member help me reorder?

1. **Settings → Caregiving → Generate code**. Pick a preset (Caregiver, Orderer, Clinician, or Minimal).
2. Send the code to your caretaker. They sign up, then **Settings → Caregiving → Redeem code**.
3. Manage exactly what they can see in **Settings → Who can help → \[their name\]**.

### How do I delete my account?

Email **K2@jonasenterprises.com** from the address you signed up with. We will delete your profile, supplements, dose history, schedules, trips, caretaker links, and push subscriptions within 14 days.

### Where's my data stored?

In Supabase-managed Postgres. Reads and writes are gated by row-level security so that only your account, and caretakers you've explicitly authorized, can see your rows. Full details in the [Privacy Policy](PRIVACY_POLICY.md).

## Crash or error you can reproduce?

Email a short note describing what you tapped and what happened. A screenshot or screen recording helps a lot. If the issue is push-related, mention which device and iOS version you're on.
