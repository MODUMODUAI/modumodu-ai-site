/* 홈페이지 상담 채팅: 오른쪽 아래 버튼 → AI가 안내 자료로 답하고, '담당자에게 남기기'로 운영자 메일에 전달합니다. */
(function () {
  const cfg = window.MODUMODU_SITE || {};
  const api = String(cfg.memberApi || "").replace(/\/+$/, "");
  const KEY = "modumodu-chat";
  let messages = [];
  try { messages = JSON.parse(sessionStorage.getItem(KEY) || "[]"); } catch (e) { messages = []; }
  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(messages.slice(-30))); } catch (e) { /* 무시 */ } };
  const esc = (t) => String(t || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const QUICK = ["가격이 궁금해요", "무료 체험은 어떻게 하나요?", "어떤 마켓을 지원하나요?", "설치는 어떻게 하나요?"];

  const root = document.createElement("div");
  root.className = "mchat";
  root.innerHTML = `
    <button type="button" class="mchat-open" aria-label="상담 채팅 열기">💬 <span>상담</span></button>
    <section class="mchat-panel" hidden aria-label="모두모두AI 상담">
      <header><strong>모두모두AI 상담</strong><button type="button" class="mchat-close" aria-label="닫기">✕</button></header>
      <div class="mchat-log" aria-live="polite"></div>
      <div class="mchat-quick"></div>
      <form class="mchat-form"><input type="text" maxlength="800" placeholder="궁금한 점을 적어 주세요" aria-label="질문" /><button type="submit">보내기</button></form>
      <button type="button" class="mchat-leave-open">담당자에게 남기기 (이메일로 답변)</button>
      <form class="mchat-leave" hidden>
        <input type="email" required placeholder="답받을 이메일" aria-label="답받을 이메일" />
        <textarea rows="3" maxlength="2000" placeholder="남길 내용 (대화 내용도 함께 전달됩니다)" aria-label="남길 내용"></textarea>
        <button type="submit">담당자에게 보내기</button>
      </form>
      <p class="mchat-note">AI가 안내 자료로 답합니다. 비밀번호·카드번호는 적지 마세요.</p>
    </section>`;
  document.body.append(root);
  const panel = root.querySelector(".mchat-panel");
  const log = root.querySelector(".mchat-log");
  const input = root.querySelector(".mchat-form input");
  const quick = root.querySelector(".mchat-quick");
  const leaveForm = root.querySelector(".mchat-leave");

  function paint(busy) {
    const greet = `<div class="mchat-msg ai">안녕하세요, 모두모두AI입니다. 가격·무료 체험·기능·설치 무엇이든 물어보세요.</div>`;
    log.innerHTML = greet + messages.map((m) => `<div class="mchat-msg ${m.role === "user" ? "me" : "ai"}">${esc(m.text).replace(/\n/g, "<br>")}</div>`).join("")
      + (busy ? `<div class="mchat-msg ai mchat-typing">답을 쓰는 중…</div>` : "");
    quick.innerHTML = messages.length ? "" : QUICK.map((q) => `<button type="button">${esc(q)}</button>`).join("");
    log.scrollTop = log.scrollHeight;
  }
  async function ask(text) {
    const q = String(text || "").trim();
    if (!q) return;
    messages.push({ role: "user", text: q });
    save();
    paint(true);
    try {
      if (!api) throw new Error("상담 서버 주소가 없습니다.");
      const res = await fetch(`${api}/api/site/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "상담 연결이 원활하지 않습니다.");
      messages.push({ role: "assistant", text: data.answer || "" });
      if (data.ai === false) leaveForm.hidden = false;
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} '담당자에게 남기기'로 남겨 주시면 이메일로 답드리겠습니다.` });
      leaveForm.hidden = false;
    }
    save();
    paint(false);
  }
  root.querySelector(".mchat-open").addEventListener("click", () => { panel.hidden = false; root.classList.add("is-open"); paint(false); input.focus(); });
  root.querySelector(".mchat-close").addEventListener("click", () => { panel.hidden = true; root.classList.remove("is-open"); });
  root.querySelector(".mchat-form").addEventListener("submit", (e) => { e.preventDefault(); const t = input.value; input.value = ""; ask(t); });
  quick.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) ask(b.textContent); });
  root.querySelector(".mchat-leave-open").addEventListener("click", () => { leaveForm.hidden = !leaveForm.hidden; if (!leaveForm.hidden) leaveForm.querySelector("input").focus(); });
  leaveForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = leaveForm.querySelector("input").value.trim();
    const text = leaveForm.querySelector("textarea").value.trim();
    const button = leaveForm.querySelector("button");
    button.disabled = true;
    try {
      const res = await fetch(`${api}/api/site/chat/leave`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, text, messages }) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "보내지 못했습니다.");
      messages.push({ role: "assistant", text: data.message || "담당자에게 전달했습니다." });
      leaveForm.hidden = true;
      leaveForm.reset();
    } catch (error) {
      messages.push({ role: "assistant", text: `${error.message} ${cfg.contactEmail || "modumoduai@gmail.com"}로 메일 주셔도 됩니다.` });
    } finally {
      button.disabled = false;
      save();
      paint(false);
    }
  });
})();
