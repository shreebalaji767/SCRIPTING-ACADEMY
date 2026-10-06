# Google Play Store Package — Scripting Academy V24

## App identity
- **App name:** Scripting Academy
- **Application ID:** `com.shreebalaji.scriptingacademy`
- **Version:** 24.0
- **Version code:** 22
- **Category:** Education
- **Pricing:** Free
- **Target SDK:** Android 16 / API 36
- **Minimum Android:** Android 7.0 / API 24

## Short description
Learn programming, scripting, mathematics, systems and administration with a practical Android learning lab.

## Full description
Scripting Academy is a practical learning app for people who want to understand programming, scripting, systems and IT administration from the ground up.

Learn through lessons, quizzes, practice tasks, notes, progress tracking and projects.

The app includes a Windows-focused learning path covering Batch/CMD, VBScript, Windows JScript, WSF, HTA, WMI, Registry automation and Windows administration concepts.

For users who have their own Windows PC, the optional Windows Lab Agent can connect the Android app to real Windows toolchains. Supported runtimes are detected on the Windows computer and real compiler/interpreter output is returned. When a runtime is unavailable, the app reports that it is unavailable rather than pretending that code executed.

Core learning data is stored locally on the device. No account is required for the core app.

## Privacy policy
https://shreebalaji767.github.io/SCRIPTING-ACADEMY/privacy.html

## Developer website
https://shreebalaji767.github.io/SCRIPTING-ACADEMY/

## Play Console checklist
- [ ] Create the app in Google Play Console.
- [ ] Upload the signed `app-release.aab`.
- [ ] Complete Store listing.
- [ ] Add app icon and required screenshots.
- [ ] Add feature graphic where requested by Play Console.
- [ ] Complete App content / declarations.
- [ ] Complete Data safety using the actual released build and its current data practices.
- [ ] Set the privacy policy URL above.
- [ ] Complete Content rating.
- [ ] Configure target audience.
- [ ] Complete Ads declaration accurately.
- [ ] Create an internal testing release before production.
- [ ] Review Play Console pre-launch and policy warnings.
- [ ] Submit the appropriate testing/production track for review.

## Signing
The repository never stores the keystore.

Configure these GitHub Actions secrets:
- `PLAY_STORE_KEYSTORE_BASE64`
- `PLAY_STORE_KEYSTORE_PASSWORD`
- `PLAY_STORE_KEY_ALIAS`
- `PLAY_STORE_KEY_PASSWORD`

Run **Publish Signed Scripting Academy AAB** only after all four secrets are configured.

The workflow verifies the AAB with `jarsigner` before publishing the GitHub Release.

## Important
The Windows Lab Agent executes submitted code on the user's selected Windows computer. It should only be used on a trusted machine/network and should never be exposed directly to the public internet.
