/* 홈페이지 모두모두 챗봇: 귀여운 캐릭터 버튼 → AI 안내, 담당자 남기기 */
(function () {
  const cfg = window.MODUMODU_SITE || {};
  const api = String(cfg.memberApi || "").replace(/\/+$/, "");
  const KEY = "modumodu-chat";
  const BUDDY = "./chat-buddy.svg?v=1";
  let messages = [];
  try { messages = JSON.parse(sessionStorage.getItem(KEY) || "[]"); } catch (e) { messages = []; }
  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(messages.slice(-30))); } catch (e) { /* 무시 */ } };
  const esc = (t) => String(t || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const QUICK = [
    "가격이 궁금해요",
    "무료 체험은 어떻게 하나요?",
    "품절 자동 관리는 어떻게 쓰나요?",
    "공급처는 어떻게 추가하나요?",
    "마진율·마진액은 어디서 보나요?",
    "설치는 어떻게 하나요?",
  ];

  const root = document.createElement("div");
  root.className = "mchat";
  root.innerHTML = `
    <button type="button" class="mchat-open" aria-label="모두모두 챗봇 열기">
      <span class="mchat-open-bubble" aria-hidden="true">물어보세요!</span>
      <img class="mchat-buddy" src="${BUDDY}" width="72" height="72" alt="" />
      <span class="mchat-open-label">모두모두</span>
    </button>
    <section class="mchat-panel" hidden aria-label="모두모두 챗봇">
      <header>
        <div class="mchat-head">
          <img class="mchat-buddy mchat-buddy-sm" src="${BUDDY}" width="40" height="40" alt="" />
          <div>
            <strong>모두모두</strong>
            <em>궁금한 건 무엇이든 물어봐요</em>
          </div>
        </div>
        <button type="button" class="mchat-close" aria-label="닫기">✕</button>
      </header>
      <div class="mchat-log" aria-live="polite"></div>
      <div class="mchat-quick"></div>
      <form class="mchat-form"><input type="text" maxlength="800" placeholder="예: 무료 체험은 어떻게 해요?" aria-label="질문" /><button type="submit">보내기</button></form>
      <button type="button" class="mchat-leave-open">담당자에게 남기기 (이메일로 답변)</button>
      <form class="mchat-leave" hidden>
        <input type="email" required placeholder="답받을 이메일" aria-label="답받을 이메일" />
        <textarea rows="3" maxlength="2000" placeholder="남길 내용 (대화 내용도 함께 전달됩니다)" aria-label="남길 내용"></textarea>
        <button type="submit">담당자에게 보내기</button>
      </form>
      <p class="mchat-note">모두모두가 홈페이지 안내와 프로그램 도움말을 보고 답해요. 비밀번호·카드번호는 적지 마세요.</p>
    </section>`;
  document.body.append(root);
  const panel = root.querySelector(".mchat-panel");
  const log = root.querySelector(".mchat-log");
  const input = root.querySelector(".mchat-form input");
  const quick = root.querySelector(".mchat-quick");
  const leaveForm = root.querySelector(".mchat-leave");

  function avatar() {
    return `<img class="mchat-avatar" src="${BUDDY}" width="28" height="28" alt="" />`;
  }

  function renderCard(card) {
    if (!card || typeof card !== "object") return "";
    const rows = Array.isArray(card.rows) ? card.rows : [];
    const list = rows.map((row) => {
      const label = esc(row && row.label);
      const value = esc(row && row.value);
      return `<li><span>${label}</span><strong>${value}</strong></li>`;
    }).join("");
    const badge = card.badge ? `<span class="mchat-card-badge">${esc(card.badge)}</span>` : "";
    const note = card.note ? `<p class="mchat-card-note">${esc(card.note)}</p>` : "";
    return `<div class="mchat-card" data-type="${esc(card.type || "")}">
      <div class="mchat-card-head"><strong>${esc(card.title || "")}</strong>${badge}</div>
      <ul>${list}</ul>
      ${note}
    </div>`;
  }

  function renderCta(cta) {
    if (cta !== "trial") return "";
    return `<a class="mchat-cta" href="#join">무료 체험 시작하기</a>`;
  }

  function renderAssistant(m) {
    const parts = [];
    if (m.card) parts.push(renderCard(m.card));
    const text = String(m.text || "").trim();
    if (text) {
      parts.push(`<div class="mchat-row ai">${avatar()}<div class="mchat-msg ai">${esc(text).replace(/\n/g, "<br>")}</div></div>`);
    }
    if (m.cta) parts.push(renderCta(m.cta));
    return `<div class="mchat-block">${parts.join("")}</div>`;
  }

  function paint(busy) {
    const greet = `<div class="mchat-block"><div class="mchat-row ai">${avatar()}<div class="mchat-msg ai">안녕! 나는 <b>모두모두</b>야.<br>가격·무료 체험·기능·설치 무엇이든 편하게 물어봐 줘.</div></div></div>`;
    log.innerHTML = greet + messages.map((m) => {
      if (m.role === "user") return `<div class="mchat-row me"><div class="mchat-msg me">${esc(m.text).replace(/\n/g, "<br>")}</div></div>`;
      return renderAssistant(m);
    }).join("")
      + (busy ? `<div class="mchat-row ai">${avatar()}<div class="mchat-msg ai mchat-typing"><span></span><span></span><span></span></div></div>` : "");
    quick.innerHTML = messages.length ? "" : QUICK.map((q) => `<button type="button">${esc(q)}</button>`).join("");
    log.scrollTop = log.scrollHeight;
  }

  function goJoin(e) {
    const link = e.target.closest("a.mchat-cta");
    if (!link) return;
    e.preventDefault();
    panel.hidden = true;
    root.classList.remove("is-open");
    const target = document.getElementById("join");
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    else location.hash = "join";
  }

  async function ask(text) {
    const q = String(text || "").trim();
    if (!q) return;
    messages.push({ role: "user", text: q });
    save();
    paint(true);
    try {
      if (!api) throw new Error("상담 서버 주소가 없습니다.");
      const res = await fetch(`${api}/api/site/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages, source: "site" }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "상담 연결이 원활하지 않습니다.");
      let answer = String(data.answer || "").trim();
      const help = Array.isArray(data.help) ? data.help.filter(Boolean) : [];
      if (help.length) {
        answer = `${answer}\n\n(프로그램 도움말: ${help.join(" · ")})`;
      }
      const item = { role: "assistant", text: answer };
      if (data.card && typeof data.card === "object") item.card = data.card;
      if (data.cta) item.cta = data.cta;
      else if (data.card && data.card.cta) item.cta = data.card.cta;
      messages.push(item);
      if (data.ai === false) showLeave(true);
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} '담당자에게 남기기'로 남겨 주시면 이메일로 답드릴게요.`, cta: "trial" });
      showLeave(true);
    }
    save();
    paint(false);
  }
  root.querySelector(".mchat-open").addEventListener("click", () => { panel.hidden = false; root.classList.add("is-open"); paint(false); input.focus(); });
  root.querySelector(".mchat-close").addEventListener("click", () => { panel.hidden = true; root.classList.remove("is-open"); });
  root.querySelector(".mchat-form").addEventListener("submit", (e) => { e.preventDefault(); const t = input.value; input.value = ""; ask(t); });
  quick.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) ask(b.textContent); });
  log.addEventListener("click", goJoin);
  function showLeave(open) {
    leaveForm.hidden = !open;
    panel.classList.toggle("is-leave", Boolean(open));
    if (open) leaveForm.querySelector("input")?.focus();
  }
  root.querySelector(".mchat-leave-open").addEventListener("click", () => showLeave(leaveForm.hidden));
  leaveForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = leaveForm.querySelector("input").value.trim();
    const text = leaveForm.querySelector("textarea").value.trim();
    const button = leaveForm.querySelector("button");
    button.disabled = true;
    try {
      const res = await fetch(`${api}/api/site/chat/leave`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, text, messages, source: "site" }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "보내지 못했습니다.");
      messages.push({ role: "assistant", text: data.message || "담당자에게 전달했어요. 남겨 주신 메일로 답드릴게요.", cta: "trial" });
      showLeave(false);
      leaveForm.reset();
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} ${cfg.contactEmail || "modumoduai@gmail.com"}로 메일 주셔도 돼요.`, cta: "trial" });
    } finally {
      button.disabled = false;
      save();
      paint(false);
    }
  });
})();
