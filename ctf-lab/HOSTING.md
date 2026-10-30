# Hosting this like TryHackMe / Hackversity — free and low-cost options

Short answer: you can host **this lab and a real CTF platform** for free for
yourself or a small group. What you cannot get for free is the full commercial
model — per-user isolated attack VMs plus a VPN at scale — because that burns
real compute and costs money. Below is what is realistically free.

## Truly free, always-on (best option)

**Oracle Cloud Always Free.** Oracle's free tier includes Arm-based compute and
small x86 instances that stay free indefinitely, which is enough to run Docker
plus a CTF platform for a small group. This is the closest thing to a free
always-on server. See the [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/).
Content was rephrased for licensing compliance.

On that VM you can run:

- **CTFd** — the popular open-source CTF platform (challenges, scoreboard,
  teams). [CTFd on GitHub](https://github.com/CTFd/CTFd). Deploy with Docker
  Compose.
- This lab's target app, in a container, as one or more challenges.

## Free trials and limited free tiers (not permanent)

- **Google Cloud** has an always-free small VM in some regions plus a trial
  credit; **AWS** gives a 12-month micro instance; **Azure** gives a credit and
  some always-free services. Good to start, but trials expire.
  Check each provider's current free-tier page before relying on it.

## Free ephemeral environments (great for practice, not hosting)

- **GitHub Codespaces** and **Gitpod** give browser-based dev machines with a
  monthly free allowance — ideal for running this lab in the browser without a
  local install.
- **Killercoda** and **Play with Docker** provide free, time-boxed interactive
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
