# Hosting this like TryHackMe / Hackversity — free and low-cost options

Short answer: you can host **this lab and a real CTF platform** for free for
yourself or a small group. What you cannot get for free is the full commercial
model — per-user isolated attack VMs plus a VPN at scale — because that burns
real compute and costs money. Below is what is realistically free.

> Free-tier details verified October 2026. These change often — always confirm
> on the provider's own page before relying on them.

## Truly free, always-on (best option)

**Oracle Cloud Always Free.** Still the only major provider with a genuinely
permanent (no trial expiry) always-free VM. As of June 15, 2026 the Arm Ampere
A1 allowance was halved: roughly **2 OCPUs and 12 GB RAM** running continuously
(the docs state 1,500 OCPU-hours and 9,000 GB-hours per month), plus two small
AMD VMs. That is still comfortably enough to run Docker plus a CTF platform for
a small group. See the [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
and the [Always Free docs](https://docs.oracle.com/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm).
Content was rephrased for licensing compliance.

On that VM you can run:

- **CTFd** — the popular open-source CTF platform (challenges, scoreboard,
  teams). [CTFd on GitHub](https://github.com/CTFd/CTFd). Deploy with Docker
  Compose.
- This lab's target app, in a container, as one or more challenges.

## Credits and trials (temporary, not permanent)

Verified October 2026:

- **AWS** replaced the old 12-month free tier (July 2025) with a credits model:
  a new account gets up to **$200 in credits** ($100 on signup, up to $100 more
  for onboarding tasks), usable for about six months on the Free plan, plus a
  set of always-free services with monthly allowances. See the
  [AWS Free Tier](https://aws.amazon.com/free/). Note AWS now charges for public
  IPv4 addresses, which can quietly bill you.
- **Google Cloud** gives new users **$300 in credits for 90 days**, plus an
  always-free `e2-micro` VM in certain US regions. See
  [Google Cloud Free](https://cloud.google.com/free).
- **Azure** gives a signup credit plus some always-free services.

Trials and credits are fine to start on, but they expire or get consumed — do
not build something you need long-term on them.

## Free browser environments (great for practising, not hosting)

- **GitHub Codespaces** — a personal Free account includes about **120
  core-hours per month** (roughly 60 hours on a 2-core machine) plus some
  storage. Ideal for running these labs in the browser with no local install.
  See [Codespaces billing](https://docs.github.com/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).
- **Gitpod**, **Killercoda**, and **Play with Docker** give free, time-boxed
  Linux/Docker sessions — good for trying things, but they reset.

## Free/low tiers to host a single web target

- **Fly.io**, **Render**, and **Railway** can host a small containerised web app
  on free or cheap tiers. Fine for a web-only target like this app; not for VPN
  or multi-VM scenarios. Verify current limits, as free tiers change often.

## The honest limitation

The TryHackMe / Hack The Box experience — a fresh, isolated vulnerable machine
per user reachable over OpenVPN — needs real, per-user compute and orchestration
(Kubernetes, VM pools). That is the part that costs money. For a personal or
small-team setup, host CTFd plus containerised challenges on an Oracle Always
Free VM and skip per-user VMs: everyone solves the same shared, firewalled
targets. That covers almost all of the learning value for free.

## Easiest of all: use platforms that are already free

If the goal is to learn rather than to run a platform, these are free (or have
strong free tiers) and need no hosting from you:

- **PortSwigger Web Security Academy** — free, excellent for web app security.
- **picoCTF**, **OverTheWire**, **HackThisSite** — free CTF/wargames.
- **TryHackMe** free rooms and **Hack The Box** free tier.

## Security rules if you do host a vulnerable target

1. Never expose an intentionally vulnerable app to the open internet. Put it
   behind authentication, an allowlisted IP, or a private network.
2. Keep it isolated from anything real (separate project/VPC, no production
   credentials on the box).
3. Only invite people you trust, and only let people attack targets they are
   authorised to attack.

Sources: Oracle Cloud Free Tier, CTFd project, and each cloud provider's
free-tier documentation (links above). Content was rephrased for licensing
compliance.
