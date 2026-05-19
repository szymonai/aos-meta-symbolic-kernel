import http from "k6/http";
import { check } from "k6";

const target = __ENV.AOS_API_URL || "http://127.0.0.1:8080";
const p95LimitMs = __ENV.AOS_K6_P95_MS || "1000";

export const options = {
  vus: 1,
  iterations: 12,
  thresholds: {
    http_req_failed: ["rate==0"],
    http_req_duration: [`p(95)<${p95LimitMs}`],
  },
};

const payloads = [
  {
    signal_id: "k6-safe-001",
    score: 2000,
    uncertainty: 500,
    limit: 5000,
    warn_margin: 1000,
    metadata_complete: true,
  },
  {
    signal_id: "k6-warn-001",
    score: 4100,
    uncertainty: 400,
    limit: 5000,
    warn_margin: 1000,
    metadata_complete: true,
  },
  {
    signal_id: "k6-block-001",
    score: 4900,
    uncertainty: 500,
    limit: 5000,
    warn_margin: 1000,
    metadata_complete: true,
  },
];

export default function () {
  const payload = payloads[__ITER % payloads.length];
  const response = http.post(`${target}/v1/evaluate`, JSON.stringify(payload), {
    headers: { "Content-Type": "application/json" },
  });

  check(response, {
    "status is 200": (res) => res.status === 200,
    "contains verdict": (res) => {
      const body = res.json();
      return ["PASS", "WARN", "BLOCK"].includes(body.verdict);
    },
    "contains audit id": (res) => {
      const body = res.json();
      return (
        typeof body.audit_id === "string" && body.audit_id.startsWith("sha256:")
      );
    },
  });
}
