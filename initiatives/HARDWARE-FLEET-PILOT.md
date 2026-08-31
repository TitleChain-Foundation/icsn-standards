# Hardware Fleet Pilot — Illustrative Implementation

> **Not standards text.** This is one illustrative, non-normative implementation of [RFC 0001: Hardware Onboarding Standard](../rfcs/0001-hardware-onboarding-standard.md). It exists to make the RFC's device/component title hierarchy concrete against real, currently available hardware and real budget numbers. It does not endorse, certify, or exclusively select any vendor. Per [GOVERNANCE.md](../GOVERNANCE.md)'s independence clause, no single vendor or implementation defines a Foundation standard, and any hardware whose components can be individually titled can conform to RFC 0001.

## Why Framework anchors this illustration

RFC 0001's title hierarchy depends on a device having legible, separable component identity — a mainboard, storage, a compute/graphics module, expansion cards — each independently serialized and replaceable. Framework's product line is used here because it is currently one of the clearest examples of that property: modular laptops, a compact desktop, refurbished systems, and a public repair/upgrade-parts marketplace, priced and sold at the component level rather than as a sealed unit. Any vendor with equivalent component legibility could anchor an equally valid illustration.

## Illustrative comparison

Current US-dollar starting prices as of this writing; final totals vary substantially with RAM, SSD, OS, graphics, expansion cards, taxes, and shipping.

| System | Starting price | Best illustrative RFC 0001 role | Sovereignty & repairability | Main limitation |
|---|---|---|---|---|
| Framework Laptop 16 (Ryzen AI 300) | $1,249 base | Primary contributor endpoint | Exceptional — modular ports, storage, memory, keyboard, upgradeable graphics | Laptop thermal/power envelope |
| Framework Laptop 16 + RTX 5070 | base + GPU module | Portable CUDA/inference node | Strong — GPU lives in a replaceable Expansion Bay module | 12GB VRAM limits larger local models |
| Framework Desktop (Ryzen AI Max+ 395, 128GB) | from $1,269 | Local-AI / RAG / private inference node | Strong chassis ethos; CPU/RAM soldered, less modular than Laptop 16 | Not CUDA — different software stack from NVIDIA |
| NVIDIA DGX Spark | $4,699 MSRP | Shared CUDA/DGX reference lab node | Moderate — local ownership, but a closed vendor appliance | High price; vendor-stack concentration |
| Apple Mac Studio M5 Ultra | $5,499–$18,299 | Selective Apple-native specialist node | Weakest of this set — integrated, difficult to service, no CUDA | Low hardware provenance/repair control |
| Conventional Windows/Linux PC + discrete GPU | Varies | General dev, CUDA, simulation | Variable — can be highly repairable if deliberately specified | No inherent provenance or non-capture philosophy by default |

**On "faster than two DGX" style claims:** a high-memory Mac Studio M5 Ultra can be genuinely competitive — or superior — on specific memory-bound local-inference workloads, because its unified-memory capacity and bandwidth let one machine hold a model that smaller-VRAM systems cannot. It is not a universal compute claim; it says nothing about CUDA training, TensorRT, FP4 throughput, or NVIDIA-specific frameworks, where linked DGX Sparks have the advantage. Any public comparison should specify model, quantization, context length, tokens/second, time-to-first-token, concurrency, framework, and power draw rather than a blanket "faster" statement.

## Illustrative fleet tiers

| Tier | Hardware | Role |
|---|---|---|
| 1 — Issued developer node | Framework Laptop 16, 64–96GB RAM, 2–4TB NVMe, Linux-first | Core engineers/contributors |
| 2 — Local-AI node | Framework Desktop 128GB | Private RAG, docs assistant, identity/attestation workflows, offline demos |
| 3 — CUDA lab lane | 1 DGX Spark (add a second only if benchmarks justify it) | Shared CUDA/PyTorch/TensorRT validation — not issued per person |
| 4 — Mac exception lane | Mac Studio M5 Ultra, 0–1 units | Apple-platform builds/signing, media/keynote only — not a fleet standard |

## Illustrative 10-person pilot purchase mix

| Item | Qty | Purpose |
|---|---|---|
| Framework Laptop 16, 64GB/2TB baseline | 8 | General engineering, node operation, protocol dev |
| Framework Laptop 16 + RTX 5070 | 2 | CUDA, visual AI, portable demos |
| Framework Desktop Max+ 395, 128GB | 2 | Private local AI, RAG, model-serving experiments |
| NVIDIA DGX Spark | 1 | CUDA/DGX compatibility, benchmark lab |
| Mac Studio M5 Ultra | 0–1 | Only if macOS builds or 256–512GB workflows are immediately needed |

Illustrative budget: roughly $45,000–$60,000 before tax, shipping, accessories, and support for a 10-person pilot. A practical working figure is about $52,000 hardware-only, with a 10–15% contingency bringing an authorization range to $58,000–$60,000. These are planning numbers for this illustration, not a committed Foundation budget.

## Status

No pilot has been deployed against this illustration. It is published to make RFC 0001 concrete for review, not as evidence that the RFC is implemented. See RFC 0001's [Conformance](../rfcs/0001-hardware-onboarding-standard.md#conformance) section for what an actual reference implementation would need to demonstrate.

## Review and sponsorship

This is a proposed public-interest pilot seeking technical review, implementation partners, and funding. The equipment mix and budget are planning assumptions for review; no purchase, vendor selection, deployment, or sponsorship is represented as complete.

- Read [RFC 0001](../rfcs/0001-hardware-onboarding-standard.md) before reviewing the pilot.
- Share general feedback in the [Hardware Onboarding Standard Discussion](https://github.com/TitleChain-Foundation/icsn-standards/discussions/33), including repairable alternatives to the named example systems.
- Contribute to the open [hardware and infrastructure issues](https://github.com/TitleChain-Foundation/icsn-standards/issues?q=is%3Aissue+is%3Aopen+label%3A%22skill%3A+hardware-infrastructure%22) covering privacy, recovery, conformance evidence, and partner credentialing.
- Review the Foundation's [sponsorship policy](../SPONSORS.md). Organizations interested in underwriting equipment, accessibility, security review, testing, or pilot operations can [contact the Foundation](mailto:hello@titlechainfoundation.org) to define scope, independence, deliverables, conflicts, and public impact reporting.

Sponsorship does not purchase standards influence, vendor endorsement, conformance status, access to participant data, or control over pilot participants.
