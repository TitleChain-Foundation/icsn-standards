/**
 * Canonical JSON and hashing for M5 evidence (M5-MATH-001, MATH-CANONICAL-HASH).
 * JavaScript twin of core/m5_canonical.py; both are held to
 * vectors/canonical-hash.vectors.json.
 */
import { createHash } from "crypto";

// Expand JavaScript's exponent notation into a plain decimal string.
function plainDecimal(value) {
  const text = String(value);
  if (!/e/i.test(text)) return text;
  const negative = text.startsWith("-");
  const [mantissa, exponentText] = (negative ? text.slice(1) : text).toLowerCase().split("e");
  const exponent = Number(exponentText);
  const [whole, fraction = ""] = mantissa.split(".");
  const digits = whole + fraction;
  const point = whole.length + exponent;
  let result;
  if (point <= 0) result = "0." + "0".repeat(-point) + digits;
  else if (point >= digits.length) result = digits + "0".repeat(point - digits.length);
  else result = digits.slice(0, point) + "." + digits.slice(point);
  return (negative ? "-" : "") + result;
}

export function canonicalValue(value) {
  if (value === null || typeof value === "boolean" || typeof value === "string") return value;
  if (typeof value === "bigint") {
    if (value > BigInt(Number.MAX_SAFE_INTEGER) || value < -BigInt(Number.MAX_SAFE_INTEGER)) {
      throw new Error("integers must be within +/-(2**53 - 1)");
    }
    return Number(value);
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("non-finite numbers cannot be canonicalized");
    if (Number.isInteger(value)) {
      if (!Number.isSafeInteger(value)) throw new Error("integers must be within +/-(2**53 - 1)");
      return value;
    }
    return plainDecimal(value);
  }
  if (Array.isArray(value)) return value.map(canonicalValue);
  if (typeof value === "object") {
    const result = {};
    for (const key of Object.keys(value)) result[key] = canonicalValue(value[key]);
    return result;
  }
  throw new Error(`cannot canonicalize ${typeof value}`);
}

function serialize(value) {
  if (Array.isArray(value)) return `[${value.map(serialize).join(",")}]`;
  if (value !== null && typeof value === "object") {
    const keys = Object.keys(value).sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    return `{${keys.map((key) => `${JSON.stringify(key)}:${serialize(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function canonicalJson(value) {
  return serialize(canonicalValue(value));
}

export function canonicalSha256(value) {
  return "sha256:" + createHash("sha256").update(canonicalJson(value), "utf8").digest("hex");
}
