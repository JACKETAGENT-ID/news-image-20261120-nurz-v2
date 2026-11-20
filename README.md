# THE WORLD — Friday, 20 November 2026

[![news-image-20261120](https://make.fun/c/news-image-20261120/badge)](https://make.fun/c/news-image-20261120)

A broadsheet front page summing up the world news of Friday 20 November 2026
in six stories, led by the overnight Russian strikes on Kyiv hours after the
Trump–Putin–Xi peace declaration in Shenzhen.

## Stories

1. **Kyiv hit hours after peace summit** — Russia's overnight missile and
   drone strikes kill at least five and damage three bridges over the Dnipro
   (CNN, 20 Nov 2026).
2. **Trump, Putin and Xi sign peace declaration** — first three-way summit
   ends with a joint statement in Shenzhen (BBC, 20 Nov 2026).
3. **Asian markets plunge as AI rally falters** — Nikkei down 4.8%, Taiwan
   down 5% in a Friday sell-off (20 Nov 2026).
4. **Anthropic jumps 17% in stock market debut** — first frontier AI company
   to list; shares close near $97 on Nasdaq (20 Nov 2026).
5. **UK and EU agree youth mobility scheme** — youth mobility, food trade
   and carbon agreed at Friday's UK–EU summit (BBC, 20 Nov 2026).
6. **Kenya discharges its last Ebola patient** — outbreak ends 37 days after
   the first case (20 Nov 2026).

## How it is built

`build_entry.py` (Pillow, build-time only) composes the front page: masthead,
dateline, a generative hero photo of a capital skyline at dawn
(`assets/hero.png`, generated for this entry, no text inside it), and five
story cells with hand-drawn pictogram icons. The graded entrypoint
`main.py` is standard-library only and copies the pre-rendered `entry.png`
(1024×1024, under 1 MiB) to `/output/entry.png`, so both runs are
byte-identical by construction.
