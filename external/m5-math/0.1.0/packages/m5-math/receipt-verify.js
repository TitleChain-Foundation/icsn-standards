/**
 * Independent verifier for M5 Value Receipts (M5-MATH-001).
 *
 * Recomputes final_wallet_split_hash from the receipt's own published
 * fields with MATH-CANONICAL-HASH, and checks the receipt's money adds up.
 * Needs nothing but the receipt itself.
 */
import { canonicalSha256 } from "./canonical.js";

export function recomputeSplitHash(receipt) {
  return canonicalSha256({
    ccf_payouts: receipt.ccf.payouts,
    source_jurisdiction: receipt.source_jurisdiction,
    destination_jurisdiction: receipt.destination_jurisdiction,
    transaction_costs: receipt.transaction_costs,
    fee_revenue_distributions: receipt.fee_revenue_distributions,
    applied_jurisdiction_rule_refs: [...new Set(receipt.applied_jurisdiction_rule_refs)].sort(),
    inputs: receipt.inputs ?? null,
  });
}

export function verifyReceipt(receipt) {
  const problems = [];
  if (recomputeSplitHash(receipt) !== receipt.final_wallet_split_hash) problems.push("split hash mismatch");
  const sum = (items) => items.reduce((total, item) => total + item.amount_micros, 0);
  const costs = sum(receipt.transaction_costs);
  if (costs !== receipt.total_transaction_cost_micros) problems.push("transaction costs do not sum");
  if (receipt.gross_value_micros - costs !== receipt.net_settled_micros) problems.push("net settled does not reconcile");
  const collected = sum(receipt.transaction_costs.filter((c) => c.revenue_class === "M5_FEE_REVENUE"));
  if (collected !== receipt.collected_m5_fee_revenue_micros) problems.push("collected fee revenue mismatch");
  if (sum(receipt.fee_revenue_distributions) !== collected) problems.push("distributions do not sum to collected fee revenue");
  const floor = Math.ceil((collected * 5) / 100);
  if (receipt.ccf.amount_micros < floor) problems.push("CCF-5 below floor");
  if (sum(receipt.ccf.payouts) !== receipt.ccf.amount_micros) problems.push("CCF payouts do not sum to the CCF amount");
  return { valid: problems.length === 0, problems };
}
