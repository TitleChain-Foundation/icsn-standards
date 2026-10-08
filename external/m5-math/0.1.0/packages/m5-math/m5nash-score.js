/**
 * M5Nash Score: JavaScript twin of core/m5nash_score.py (M5-MATH-001
 * MATH-M5NASH-DECAY, MATH-M5NASH-COMPONENT, MATH-M5NASH-COMPOSITE). Integer-only
 * (BigInt); both implementations are held to vectors/m5nash-score.vectors.json.
 */
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { canonicalSha256 } from "./canonical.js";

const HERE = dirname(fileURLToPath(import.meta.url));
export const COMPONENTS = [
  "settlement_reliability",
  "attestation_integrity",
  "information_symmetry",
  "reciprocity",
  "externality",
  "governance_participation",
];
const Q_BITS = 32n;
const Q = 1n << Q_BITS;
const SECONDS_PER_DAY = 86400;

export class M5NashScoreError extends Error {}

export function loadWeights() {
  const weights = JSON.parse(readFileSync(join(HERE, "m5nash-weights.json"), "utf-8"));
  validateWeights(weights);
  return weights;
}

export function validateWeights(weights) {
  const bps = weights.weights_bps;
  const keys = Object.keys(bps).sort();
  if (keys.join() !== [...COMPONENTS].sort().join()) {
    throw new M5NashScoreError("weights must cover exactly the six M5Nash components");
  }
  if (Object.values(bps).some((v) => !Number.isInteger(v) || v < 0)) {
    throw new M5NashScoreError("weights must be non-negative integers");
  }
  if (Object.values(bps).reduce((a, b) => a + b, 0) !== 10000) {
    throw new M5NashScoreError("weights must sum to 10000 bps");
  }
  if (weights.prior.alpha < 1 || weights.prior.beta < 1) {
    throw new M5NashScoreError("prior alpha and beta must be at least 1");
  }
  if (weights.decay.fixed_point_bits !== 32) throw new M5NashScoreError("decay must use 32-bit fixed point");
}

export function decayWeight(ageDays, dailyFactorQ32) {
  if (ageDays < 0) throw new M5NashScoreError("signals cannot be in the future");
  let result = Q;
  let base = BigInt(dailyFactorQ32);
  let exponent = BigInt(ageDays);
  while (exponent > 0n) {
    if (exponent & 1n) result = (result * base) >> Q_BITS;
    base = (base * base) >> Q_BITS;
    exponent >>= 1n;
  }
  return result;
}

function parseUtc(text) {
  if (!/(Z|[+-]\d\d:\d\d)$/.test(text)) throw new M5NashScoreError("times must be timezone-aware");
  return new Date(text);
}

export function utcIso(date) {
  return date.toISOString().replace(/\.\d{3}Z$/, "Z");
}

export function ageInDays(signalAt, asOf) {
  const seconds = Math.trunc((parseUtc(asOf) - parseUtc(signalAt)) / 1000);
  if (seconds < 0) throw new M5NashScoreError("signals cannot be in the future");
  return Math.floor(seconds / SECONDS_PER_DAY);
}

export function componentScore(goodQ, badQ, weights) {
  const alpha = BigInt(weights.prior.alpha);
  const beta = BigInt(weights.prior.beta);
  const scale = BigInt(weights.scale);
  return (scale * (goodQ + alpha * Q)) / (goodQ + badQ + (alpha + beta) * Q);
}

/**
 * signals: [{subject, component, polarity, at (ISO with zone), source_ref}]
 */
export function computeM5Score({ subject, signals, asOf, weights = null, previousRecordHash = null }) {
  const w = weights || loadWeights();
  validateWeights(w);
  const seen = new Set();
  for (const signal of signals) {
    if (signal.subject !== subject) throw new M5NashScoreError("all signals must belong to the scored subject");
    if (!COMPONENTS.includes(signal.component)) throw new M5NashScoreError(`unknown component ${signal.component}`);
    if (!["GOOD", "BAD"].includes(signal.polarity)) throw new M5NashScoreError(`unknown polarity ${signal.polarity}`);
    if (!signal.source_ref) throw new M5NashScoreError("every signal needs a source_ref");
    const key = `${signal.source_ref}\u0000${signal.component}`;
    if (seen.has(key)) throw new M5NashScoreError(`duplicate signal for ${signal.source_ref} / ${signal.component}`);
    seen.add(key);
  }
  const factors = {
    GOOD: w.decay.daily_factor_q32[String(w.decay.positive_half_life_days)],
    BAD: w.decay.daily_factor_q32[String(w.decay.negative_half_life_days)],
  };
  const sums = Object.fromEntries(COMPONENTS.map((c) => [c, { GOOD: 0n, BAD: 0n }]));
  const counts = Object.fromEntries(COMPONENTS.map((c) => [c, { GOOD: 0, BAD: 0 }]));
  for (const signal of signals) {
    sums[signal.component][signal.polarity] += decayWeight(ageInDays(signal.at, asOf), factors[signal.polarity]);
    counts[signal.component][signal.polarity] += 1;
  }
  const components = {};
  let weighted = 0n;
  for (const component of COMPONENTS) {
    const score = componentScore(sums[component].GOOD, sums[component].BAD, w);
    components[component] = {
      score: Number(score),
      weight_bps: w.weights_bps[component],
      good_weight_q32: sums[component].GOOD,
      bad_weight_q32: sums[component].BAD,
      good_signals: counts[component].GOOD,
      bad_signals: counts[component].BAD,
    };
    weighted += BigInt(w.weights_bps[component]) * score;
  }
  const m5score = Number(weighted / 10000n);
  const ordered = signals
    .map((s) => ({ subject: s.subject, component: s.component, polarity: s.polarity, at: utcIso(parseUtc(s.at)), source_ref: s.source_ref }))
    .sort((a, b) =>
      a.at !== b.at ? (a.at < b.at ? -1 : 1) : a.source_ref !== b.source_ref ? (a.source_ref < b.source_ref ? -1 : 1) : a.component < b.component ? -1 : a.component > b.component ? 1 : 0,
    );
  const record = {
    subject,
    as_of: utcIso(parseUtc(asOf)),
    m5score,
    m5nash_score_db: `${Math.floor(m5score / 10)}.${m5score % 10}`,
    components,
    weights_version: w.version,
    weights_status: w.status,
    weights_sha256: canonicalSha256(w),
    economic_consequences_enabled: w.economic_consequences_enabled,
    trust_tier: null,
    event_type: previousRecordHash ? "TRIGGERED_REVIEW" : "GENESIS",
    event_authority: "M5NASH_AGENT",
    computed_by: w.roles.score_computed_by,
    signals: ordered,
    signals_sha256: canonicalSha256(ordered),
    previous_record_hash: previousRecordHash,
  };
  record.record_hash = canonicalSha256(record);
  return record;
}
