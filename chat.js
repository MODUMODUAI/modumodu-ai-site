/* 홈페이지 모두모두 챗봇: 표정·첫인사·리액션 */
(function () {
  const cfg = window.MODUMODU_SITE || {};
  const api = String(cfg.memberApi || "").replace(/\/+$/, "");
  const KEY = "modumodu-chat";
  const HELLO_KEY = "modumodu-chat-hello-v1";
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
  const FACE = `<span class="mchat-face" style="width:72px;height:72px"><svg class="mchat-buddy-svg" viewBox="0 0 96 96" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="MBGs72" x1="18" y1="10" x2="78" y2="88" gradientUnits="userSpaceOnUse">
      <stop stop-color="#4db2ff"/><stop offset="1" stop-color="#0b7dda"/>
    </linearGradient>
  </defs>
  <ellipse cx="48" cy="86" rx="26" ry="5" fill="#0b5cab" opacity=".14"/>
  <circle cx="48" cy="50" r="34" fill="url(#MBGs72)"/>
  <circle cx="34" cy="38" r="10" fill="#fff" opacity=".22"/>
  <g class="mchat-antenna">
    <path d="M48 20v7" stroke="#ffd56a" stroke-width="3" stroke-linecap="round"/>
    <circle class="mchat-star" cx="48" cy="14" r="5.5" fill="#ffd56a"/>
    <circle cx="48" cy="14" r="2.4" fill="#fff6c8"/>
  </g>
  <g class="mchat-think" aria-hidden="true">
    <circle class="d1" cx="72" cy="22" r="3.2" fill="#fff"/>
    <circle class="d2" cx="80" cy="14" r="4.2" fill="#fff"/>
    <circle class="d3" cx="88" cy="8" r="5" fill="#fff"/>
  </g>
  <ellipse class="mchat-eye mchat-eye-l" cx="36.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <ellipse class="mchat-eye mchat-eye-r" cx="59.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <circle cx="37.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="60.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="38.8" cy="48.5" r="1.1" fill="#fff"/>
  <circle cx="61.8" cy="48.5" r="1.1" fill="#fff"/>
  <ellipse class="mchat-blush" cx="27" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <ellipse class="mchat-blush" cx="69" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <path class="mchat-smile" d="M39 61c3.2 4.2 10.8 4.2 14 0" fill="none" stroke="#17324d" stroke-width="2.6" stroke-linecap="round"/>
  <path class="mchat-smile-big" d="M37 60c4.2 6.2 14.8 6.2 19 0" fill="none" stroke="#17324d" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M41 72v-6.5l7 5.2 7-5.2V72" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".92"/>
</svg></span>`;
  const FACE_SM = `<span class="mchat-face" style="width:40px;height:40px"><svg class="mchat-buddy-svg" viewBox="0 0 96 96" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="MBGs40" x1="18" y1="10" x2="78" y2="88" gradientUnits="userSpaceOnUse">
      <stop stop-color="#4db2ff"/><stop offset="1" stop-color="#0b7dda"/>
    </linearGradient>
  </defs>
  <ellipse cx="48" cy="86" rx="26" ry="5" fill="#0b5cab" opacity=".14"/>
  <circle cx="48" cy="50" r="34" fill="url(#MBGs40)"/>
  <circle cx="34" cy="38" r="10" fill="#fff" opacity=".22"/>
  <g class="mchat-antenna">
    <path d="M48 20v7" stroke="#ffd56a" stroke-width="3" stroke-linecap="round"/>
    <circle class="mchat-star" cx="48" cy="14" r="5.5" fill="#ffd56a"/>
    <circle cx="48" cy="14" r="2.4" fill="#fff6c8"/>
  </g>
  <g class="mchat-think" aria-hidden="true">
    <circle class="d1" cx="72" cy="22" r="3.2" fill="#fff"/>
    <circle class="d2" cx="80" cy="14" r="4.2" fill="#fff"/>
    <circle class="d3" cx="88" cy="8" r="5" fill="#fff"/>
  </g>
  <ellipse class="mchat-eye mchat-eye-l" cx="36.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <ellipse class="mchat-eye mchat-eye-r" cx="59.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <circle cx="37.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="60.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="38.8" cy="48.5" r="1.1" fill="#fff"/>
  <circle cx="61.8" cy="48.5" r="1.1" fill="#fff"/>
  <ellipse class="mchat-blush" cx="27" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <ellipse class="mchat-blush" cx="69" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <path class="mchat-smile" d="M39 61c3.2 4.2 10.8 4.2 14 0" fill="none" stroke="#17324d" stroke-width="2.6" stroke-linecap="round"/>
  <path class="mchat-smile-big" d="M37 60c4.2 6.2 14.8 6.2 19 0" fill="none" stroke="#17324d" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M41 72v-6.5l7 5.2 7-5.2V72" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".92"/>
</svg></span>`;
  const FACE_AV = `<span class="mchat-face" style="width:28px;height:28px"><svg class="mchat-buddy-svg" viewBox="0 0 96 96" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="MBGs28" x1="18" y1="10" x2="78" y2="88" gradientUnits="userSpaceOnUse">
      <stop stop-color="#4db2ff"/><stop offset="1" stop-color="#0b7dda"/>
    </linearGradient>
  </defs>
  <ellipse cx="48" cy="86" rx="26" ry="5" fill="#0b5cab" opacity=".14"/>
  <circle cx="48" cy="50" r="34" fill="url(#MBGs28)"/>
  <circle cx="34" cy="38" r="10" fill="#fff" opacity=".22"/>
  <g class="mchat-antenna">
    <path d="M48 20v7" stroke="#ffd56a" stroke-width="3" stroke-linecap="round"/>
    <circle class="mchat-star" cx="48" cy="14" r="5.5" fill="#ffd56a"/>
    <circle cx="48" cy="14" r="2.4" fill="#fff6c8"/>
  </g>
  <g class="mchat-think" aria-hidden="true">
    <circle class="d1" cx="72" cy="22" r="3.2" fill="#fff"/>
    <circle class="d2" cx="80" cy="14" r="4.2" fill="#fff"/>
    <circle class="d3" cx="88" cy="8" r="5" fill="#fff"/>
  </g>
  <ellipse class="mchat-eye mchat-eye-l" cx="36.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <ellipse class="mchat-eye mchat-eye-r" cx="59.5" cy="48" rx="6.2" ry="7.2" fill="#fff"/>
  <circle cx="37.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="60.5" cy="50" r="3.1" fill="#17324d"/>
  <circle cx="38.8" cy="48.5" r="1.1" fill="#fff"/>
  <circle cx="61.8" cy="48.5" r="1.1" fill="#fff"/>
  <ellipse class="mchat-blush" cx="27" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <ellipse class="mchat-blush" cx="69" cy="58" rx="5" ry="3" fill="#ff9bb8" opacity=".55"/>
  <path class="mchat-smile" d="M39 61c3.2 4.2 10.8 4.2 14 0" fill="none" stroke="#17324d" stroke-width="2.6" stroke-linecap="round"/>
  <path class="mchat-smile-big" d="M37 60c4.2 6.2 14.8 6.2 19 0" fill="none" stroke="#17324d" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M41 72v-6.5l7 5.2 7-5.2V72" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".92"/>
</svg></span>`;

  const root = document.createElement("div");
  root.className = "mchat";
  root.dataset.mood = "idle";
  root.innerHTML = `
    <button type="button" class="mchat-open" aria-label="모두모두 챗봇 열기">
      <span class="mchat-open-bubble" aria-hidden="true">물어보세요!</span>
      ${FACE}
      <span class="mchat-open-label">모두모두</span>
    </button>
    <section class="mchat-panel" hidden aria-label="모두모두 챗봇">
      <header>
        <div class="mchat-head">
          ${FACE_SM}
          <div>
            <strong>모두모두</strong>
            <em class="mchat-status">궁금한 건 무엇이든 물어봐요</em>
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
  const bubble = root.querySelector(".mchat-open-bubble");
  const status = root.querySelector(".mchat-status");
  let moodTimer = 0;

  function setMood(mood, note) {
    root.dataset.mood = mood || "idle";
    if (note) status.textContent = note;
    else if (mood === "think") status.textContent = "생각 중이에요…";
    else if (mood === "happy") status.textContent = "이렇게 도와드렸어요!";
    else status.textContent = "궁금한 건 무엇이든 물어봐요";
  }

  function avatar() {
    return FACE_AV;
  }

  function renderCard(card) {
    if (!card || typeof card !== "object") return "";
    const rows = Array.isArray(card.rows) ? card.rows : [];
    const list = rows.map((row) => `<li><span>${esc(row && row.label)}</span><strong>${esc(row && row.value)}</strong></li>`).join("");
    const badge = card.badge ? `<span class="mchat-card-badge">${esc(card.badge)}</span>` : "";
    const note = card.note ? `<p class="mchat-card-note">${esc(card.note)}</p>` : "";
    return `<div class="mchat-card" data-type="${esc(card.type || "")}"><div class="mchat-card-head"><strong>${esc(card.title || "")}</strong>${badge}</div><ul>${list}</ul>${note}</div>`;
  }

  function renderCta(cta) {
    if (cta !== "trial") return "";
    return `<a class="mchat-cta" href="#join">무료 체험 시작하기</a>`;
  }

  function renderAssistant(m) {
    const parts = [];
    if (m.card) parts.push(renderCard(m.card));
    const text = String(m.text || "").trim();
    if (text) parts.push(`<div class="mchat-row ai">${avatar()}<div class="mchat-msg ai">${esc(text).replace(/\n/g, "<br>")}</div></div>`);
    if (m.cta) parts.push(renderCta(m.cta));
    return `<div class="mchat-block">${parts.join("")}</div>`;
  }

  function paint(busy) {
    const greet = `<div class="mchat-block"><div class="mchat-row ai">${avatar()}<div class="mchat-msg ai">안녕! 나는 <b>모두모두</b>야.<br>가격·무료 체험·기능·설치 무엇이든 편하게 물어봐 줘.</div></div></div>`;
    log.innerHTML = greet + messages.map((m) => {
      if (m.role === "user") return `<div class="mchat-row me"><div class="mchat-msg me">${esc(m.text).replace(/\n/g, "<br>")}</div></div>`;
      return renderAssistant(m);
    }).join("") + (busy ? `<div class="mchat-row ai">${avatar()}<div class="mchat-msg ai mchat-typing"><span></span><span></span><span></span></div></div>` : "");
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
    setMood("think");
    paint(true);
    try {
      if (!api) throw new Error("상담 서버 주소가 없습니다.");
      const res = await fetch(`${api}/api/site/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages, source: "site" }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "상담 연결이 원활하지 않습니다.");
      let answer = String(data.answer || "").trim();
      const help = Array.isArray(data.help) ? data.help.filter(Boolean) : [];
      if (help.length) answer = `${answer}\n\n(프로그램 도움말: ${help.join(" · ")})`;
      const item = { role: "assistant", text: answer };
      if (data.card && typeof data.card === "object") item.card = data.card;
      if (data.cta) item.cta = data.cta;
      else if (data.card && data.card.cta) item.cta = data.card.cta;
      messages.push(item);
      if (data.ai === false) showLeave(true);
      setMood("happy");
      clearTimeout(moodTimer);
      moodTimer = setTimeout(() => setMood("idle"), 2200);
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} '담당자에게 남기기'로 남겨 주시면 이메일로 답드릴게요.`, cta: "trial" });
      showLeave(true);
      setMood("idle");
    }
    save();
    paint(false);
  }

  root.querySelector(".mchat-open").addEventListener("click", () => {
    panel.hidden = false;
    root.classList.add("is-open");
    paint(false);
    input.focus();
  });
  root.querySelector(".mchat-close").addEventListener("click", () => {
    panel.hidden = true;
    root.classList.remove("is-open");
  });
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
    setMood("think");
    try {
      const res = await fetch(`${api}/api/site/chat/leave`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, text, messages, source: "site" }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "보내지 못했습니다.");
      messages.push({ role: "assistant", text: data.message || "담당자에게 전달했어요. 남겨 주신 메일로 답드릴게요.", cta: "trial" });
      showLeave(false);
      leaveForm.reset();
      setMood("happy");
      clearTimeout(moodTimer);
      moodTimer = setTimeout(() => setMood("idle"), 2200);
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} ${cfg.contactEmail || "modumoduai@gmail.com"}로 메일 주셔도 돼요.`, cta: "trial" });
      setMood("idle");
    } finally {
      button.disabled = false;
      save();
      paint(false);
    }
  });

  // 첫 방문 한 번만 인사 말풍선
  try {
    if (!localStorage.getItem(HELLO_KEY)) {
      localStorage.setItem(HELLO_KEY, "1");
      bubble.textContent = "안녕, 나는 모두모두야!";
      bubble.classList.add("is-hello");
      root.classList.add("is-hello");
      setTimeout(() => {
        if (root.classList.contains("is-open")) return;
        bubble.textContent = "물어보세요!";
        bubble.classList.remove("is-hello");
        root.classList.remove("is-hello");
      }, 6500);
    }
  } catch (e) { /* ignore */ }
})();
