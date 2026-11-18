// ASD-RAG student demo frontend — static, no build step, no external calls.
// Talks only to this same-origin FastAPI backend (/api/chat, /api/system/status).
// Does not store conversation text anywhere outside the browser tab's own memory.
"use strict";

const SUGGESTED_QUESTIONS = [
  "Rối loạn phổ tự kỷ là gì?",
  "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?",
  "Tự kỷ được chẩn đoán như thế nào?",
  "Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì?",
  "Vắc-xin có gây tự kỷ không?",
  "Hôm nay thời tiết thế nào?",
];

const messagesEl = document.getElementById("messages");
const evidenceListEl = document.getElementById("evidence-list");
const form = document.getElementById("composer");
const input = document.getElementById("query-input");
const sendBtn = document.getElementById("send-btn");
const suggestionsEl = document.getElementById("suggestions");
const badgesEl = document.getElementById("mode-badges");

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderSuggestions() {
  SUGGESTED_QUESTIONS.forEach((q) => {
    const btn = el("button", "suggestion-btn", q);
    btn.type = "button";
    btn.addEventListener("click", () => {
      input.value = q;
      form.requestSubmit();
    });
    suggestionsEl.appendChild(btn);
  });
}

function addUserMessage(text) {
  const wrap = el("div", "msg msg-user");
  wrap.appendChild(el("div", "bubble", text));
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addAssistantMessage({ text, tags = [], isError = false, isLoading = false }) {
  const wrap = el("div", "msg msg-assistant" + (isError ? " is-error" : "") + (isLoading ? " is-loading" : ""));
  if (tags.length) {
    const row = el("div", "tag-row");
    tags.forEach(([label, cls]) => row.appendChild(el("span", "tag " + cls, label)));
    wrap.appendChild(row);
  }
  wrap.appendChild(el("div", "bubble", text));
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

// Each evidence item is numbered ("Nguồn 1", "Nguồn 2", …) in the panel, never shown as a bare "C1" code
// — the raw citation_id stays a programmatic key only, matching the task's "no C1/C2/C3" requirement.
function renderEvidence(evidence) {
  evidenceListEl.innerHTML = "";
  if (!evidence || evidence.length === 0) {
    evidenceListEl.appendChild(el("p", "evidence-empty", "Không có bằng chứng cho câu hỏi gần nhất."));
    return;
  }
  evidence.forEach((item, i) => {
    const card = el("div", "evidence-card");
    const head = el("div", "ev-head");
    head.appendChild(el("span", null, `Nguồn ${i + 1}`));
    card.appendChild(head);

    const nameNode = item.source_url
      ? (() => {
          const a = document.createElement("a");
          a.href = item.source_url;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
          a.textContent = item.title || item.source_id;
          return a;
        })()
      : el("span", null, item.title || item.source_id);
    const nameLine = el("div", "ev-name");
    nameLine.appendChild(nameNode);
    card.appendChild(nameLine);

    const locator = item.page ? `Trang ${item.page}` : (item.char_range ? `Vị trí ${item.char_range}` : null);
    const metaParts = [item.section, locator].filter(Boolean);
    if (metaParts.length) card.appendChild(el("div", "ev-meta", metaParts.join(" · ")));
    if (item.support_type && item.support_type !== "direct") {
      card.appendChild(el("div", "ev-support-note",
        "Nguồn đề cập chủ đề này một cách gián tiếp, không phải chuyên biệt."));
    }
    if (item.age_mismatch) {
      card.appendChild(el("div", "ev-support-note", "Nguồn không xác nhận rõ độ tuổi cụ thể được hỏi."));
    }
    card.appendChild(el("div", "ev-excerpt", item.excerpt));
    evidenceListEl.appendChild(card);
  });
}

async function loadSystemStatus() {
  try {
    const res = await fetch("/api/system/status");
    if (!res.ok) return;
    const data = await res.json();
    badgesEl.innerHTML = "";
    if (data.demo_mode) badgesEl.appendChild(el("span", "badge badge-demo", "DEMO MODE"));
    const liveAny = data.live_query_embedding_enabled || data.live_reranking_enabled || data.live_llm_enabled;
    badgesEl.appendChild(el("span", "badge badge-cache", liveAny ? "LIVE PROVIDER ENABLED" : "CACHE-ONLY"));
  } catch (err) {
    // Status badge is cosmetic; a failed fetch here must not block the chat form.
  }
}

// Every mode is labeled honestly — none of these claim to be a real LLM answer. See
// app/answer/answer_generator.py for what each mode actually does.
function tagsForMode(mode, retrievalStatus) {
  const byMode = {
    topic_template: [["MẪU CÓ KIỂM CHỨNG NGUỒN (KHÔNG PHẢI LLM)", "tag-template"]],
    extractive_fallback: [["TRÍCH DẪN TRỰC TIẾP (CHƯA CÓ BẢN TỔNG HỢP)", "tag-fallback"]],
    insufficient_evidence: [["CHƯA ĐỦ BẰNG CHỨNG", "tag-no-results"]],
    safety_refusal_dosing: [["TỪ CHỐI VÌ AN TOÀN — CẦN BÁC SĨ", "tag-safety"]],
    safety_caution_unproven_cure: [["CẢNH BÁO — CHƯA CÓ BẰNG CHỨNG", "tag-safety"]],
    greeting_template: [["CHÀO HỎI", "tag-greeting"]],
    out_of_scope: [["NGOÀI PHẠM VI ASD", "tag-no-results"]],
  };
  const tags = byMode[mode] || [["KHÔNG XÁC ĐỊNH", "tag-no-results"]];
  if (retrievalStatus === "no_results" && mode !== "insufficient_evidence") {
    tags.push(["KHÔNG CÓ KẾT QUẢ", "tag-no-results"]);
  }
  return tags;
}

async function sendQuery(query) {
  addUserMessage(query);
  const loadingBubble = addAssistantMessage({ text: "Đang truy xuất bằng chứng…", isLoading: true });
  sendBtn.disabled = true;

  let body;
  let httpOk = false;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 }),
    });
    httpOk = res.ok;
    body = await res.json();
  } catch (err) {
    loadingBubble.remove();
    addAssistantMessage({
      text: "Không thể kết nối tới máy chủ demo cục bộ. Kiểm tra backend đã chạy chưa.",
      isError: true,
      tags: [["LỖI KẾT NỐI", "tag-blocked"]],
    });
    sendBtn.disabled = false;
    return;
  }

  loadingBubble.remove();
  sendBtn.disabled = false;

  if (!httpOk || body.status === "blocked" || body.status === "error") {
    const code = body.error ? body.error.code : "UNKNOWN_ERROR";
    const message = body.error ? body.error.message : "Yêu cầu thất bại an toàn.";
    addAssistantMessage({
      text: message,
      isError: true,
      tags: [[code, "tag-blocked"]],
    });
    renderEvidence([]);
    return;
  }

  addAssistantMessage({ text: body.answer, tags: tagsForMode(body.answer_mode, body.retrieval_status) });
  renderEvidence(body.evidence);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = input.value.trim();
  if (!query) return;
  input.value = "";
  sendQuery(query);
});

renderSuggestions();
loadSystemStatus();
