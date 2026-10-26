(() => {
  const cfg = window.MODUMODU_SITE || {};
  const toastEl = document.getElementById("toast");
  const planSelect = document.getElementById("planSelect");
  const form = document.getElementById("orderForm");
  const payStatus = document.getElementById("payStatus");
  let selectedPay = "kakaopay";
  let portoneReady = false;

  function showToast(message) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.classList.add("show");
    window.clearTimeout(showToast._timer);
    showToast._timer = window.setTimeout(() => toastEl.classList.remove("show"), 2800);
  }

  function setPayStatus(message) {
    if (payStatus) payStatus.textContent = message || "";
  }

  function applyContact() {
    const mail = document.getElementById("contactEmail");
    const kakao = document.getElementById("contactKakao");
    const bank = document.getElementById("contactBank");
    if (mail && cfg.contactEmail) {
      mail.textContent = cfg.contactEmail;
      mail.href = `mailto:${cfg.contactEmail}`;
    }
    if (kakao && cfg.contactKakao) kakao.textContent = cfg.contactKakao;
    if (bank && cfg.contactBank) bank.textContent = cfg.contactBank;
  }

  function syncPayButtons() {
    document.querySelectorAll("[data-pay]").forEach((node) => {
      const on = node.getAttribute("data-pay") === selectedPay;
      node.classList.toggle("is-active", on);
      node.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function selectPlan(plan) {
    if (!planSelect || !cfg.plans?.[plan]) return;
    planSelect.value = plan;
    document.getElementById("buy")?.scrollIntoView({ behavior: "smooth", block: "start" });
    showToast(`${cfg.plans[plan].label}을 골랐습니다.`);
    updatePayHint();
  }

  function won(amount) {
    return `${Number(amount || 0).toLocaleString("ko-KR")}원`;
  }

  function supplierChoice() {
    const packs = Math.max(0, Number(document.getElementById("supplierPacks")?.value || 0));
    const ownerclan = Boolean(document.getElementById("ownerclan")?.checked);
    const rule = cfg.supplier || {};
    const monthly = packs * Number(rule.packMonthly || 0) + (ownerclan ? Number(rule.ownerclanMonthly || 0) : 0);
    const count = Number(rule.freeCount || 10) + packs * Number(rule.packSize || 10);
    const bits = [`공급사 ${count}개`];
    if (ownerclan) bits.push("오너클랜 전체");
    return { packs, ownerclan, monthly, count, label: bits.join(" · ") };
  }

  function paymentQuote() {
    const plan = planSelect?.value || "m3";
    const info = cfg.plans?.[plan] || { label: plan, price: "", amount: 0, months: 0 };
    if (info.ownerclanOnly) {
      return {
        plan,
        info,
        extra: { label: "오너클랜 전체", monthly: Number(info.amount || 0), packs: 0, ownerclan: true, count: 0 },
        months: 1,
        supplierAmount: 0,
        amount: Number(info.amount || 0),
      };
    }
    const extra = supplierChoice();
    const months = Number(info.months || 0);
    const supplierAmount = extra.monthly * months;
    return {
      plan,
      info,
      extra,
      months,
      supplierAmount,
      amount: Number(info.amount || 0) + supplierAmount,
    };
  }

  function syncAddonFields() {
    const only = Boolean(cfg.plans?.[planSelect?.value || ""]?.ownerclanOnly);
    const packs = document.getElementById("supplierPacks");
    const box = document.getElementById("ownerclan");
    if (packs) packs.disabled = only;
    if (box) {
      box.disabled = only;
      if (only) box.checked = false;
    }
  }

  function updatePayHint() {
    syncAddonFields();
    const quote = paymentQuote();
    const button = document.getElementById("paySubmit");
    if (!quote.amount) {
      if (button) button.textContent = "무료 신청";
      setPayStatus("무료 체험은 결제 없이 신청됩니다. 공급사 추가 요금은 유료 기간에 월 단위로 붙습니다.");
      return;
    }
    const parts = [`${quote.info.label} ${quote.info.price || won(quote.info.amount)}`];
    if (quote.supplierAmount) parts.push(`${quote.extra.label} ${won(quote.supplierAmount)}`);
    if (button) button.textContent = `${won(quote.amount)} 결제하기`;
    const total = `${parts.join(" + ")} · 합계 ${won(quote.amount)}`;
    if (!cfg.portoneImpCode) {
      setPayStatus(`${total}. 가맹 연결 전에는 신청 메일이 열립니다.`);
      return;
    }
    setPayStatus(`${total} · ${cfg.payMethods?.[selectedPay]?.label || "페이"}로 결제`);
  }

  function ensurePortone() {
    if (!cfg.portoneImpCode) return false;
    if (typeof window.IMP === "undefined") {
      showToast("결제 모듈을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.");
      return false;
    }
    if (!portoneReady) {
      window.IMP.init(cfg.portoneImpCode);
      portoneReady = true;
    }
    return true;
  }

  function openInquiryMail({ planInfo, name, email, phone, message, payLabel }) {
    const to = cfg.contactEmail || "modumoduai@gmail.com";
    const subject = `[모두모두AI] ${planInfo.label} 문의 - ${name}`;
    const body = [
      "모두모두AI 이용 문의입니다.",
      "",
      `요금: ${planInfo.label} (${planInfo.price})`,
      `공급사: ${planInfo.supplierLabel || "-"}`,
      `합계: ${planInfo.totalLabel || planInfo.price}`,
      `결제수단: ${payLabel || "-"}`,
      `이름: ${name}`,
      `이메일: ${email}`,
      `연락처: ${phone || "-"}`,
      "",
      "남길 말:",
      message || "-",
    ].join("\n");
    window.location.href = `mailto:${encodeURIComponent(to)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  function requestPay({ plan, planInfo, name, email, phone, payKey }) {
    const method = cfg.payMethods?.[payKey];
    if (!method) {
      showToast("결제 수단을 다시 골라 주세요.");
      return;
    }
    if (!ensurePortone()) {
      openInquiryMail({
        planInfo,
        name,
        email,
        phone,
        message: form?.elements?.message?.value || "",
        payLabel: method.label,
      });
      showToast("가맹 연결 전이어서 문의 메일을 엽니다.");
      return;
    }

    const merchantUid = `modumodu_${plan}_${Date.now()}`;
    const payButton = document.getElementById("paySubmit");
    if (payButton) payButton.disabled = true;
    setPayStatus(`${method.label} 결제창을 여는 중…`);

    window.IMP.request_pay(
      {
        pg: method.pg,
        pay_method: "card",
        merchant_uid: merchantUid,
        name: `모두모두AI ${planInfo.label}${planInfo.supplierLabel ? ` + ${planInfo.supplierLabel}` : ""}`,
        amount: planInfo.amount,
        buyer_email: email,
        buyer_name: name,
        buyer_tel: phone || "01000000000",
        m_redirect_url: `${window.location.origin}${window.location.pathname}#buy`,
      },
      (response) => {
        if (payButton) payButton.disabled = false;
        if (response?.success || response?.imp_success) {
          setPayStatus("결제가 완료되었습니다. 이용 키를 이메일로 보내 드립니다.");
          showToast("결제가 완료되었습니다.");
          openInquiryMail({
            planInfo,
            name,
            email,
            phone,
            message: [
              form?.elements?.message?.value || "",
              "",
              `[결제완료]`,
              `imp_uid: ${response.imp_uid || "-"}`,
              `merchant_uid: ${response.merchant_uid || merchantUid}`,
              `결제수단: ${method.label}`,
            ].join("\n"),
            payLabel: method.label,
          });
          return;
        }
        const reason = response?.error_msg || response?.error_msg || "결제가 취소되었거나 실패했습니다.";
        setPayStatus(reason);
        showToast(reason);
      }
    );
  }

  document.querySelectorAll("[data-plan]").forEach((node) => {
    node.addEventListener("click", (event) => {
      const plan = node.getAttribute("data-plan");
      if (!plan || !cfg.plans?.[plan]) return;
      if (node.tagName === "A") event.preventDefault();
      selectPlan(plan);
    });
  });

  document.querySelectorAll("[data-pay]").forEach((node) => {
    node.addEventListener("click", () => {
      selectedPay = node.getAttribute("data-pay") || "kakaopay";
      syncPayButtons();
      updatePayHint();
    });
  });

  planSelect?.addEventListener("change", updatePayHint);
  document.getElementById("supplierPacks")?.addEventListener("change", updatePayHint);
  document.getElementById("ownerclan")?.addEventListener("change", updatePayHint);

  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const quote = paymentQuote();
    const planInfo = {
      ...quote.info,
      amount: quote.amount,
      supplierLabel: quote.extra.label,
      totalLabel: won(quote.amount),
    };
    const name = String(data.get("name") || "").trim();
    const email = String(data.get("email") || "").trim();
    const phone = String(data.get("phone") || "").trim();
    const message = String(data.get("message") || "").trim();
    const payLabel = cfg.payMethods?.[selectedPay]?.label || selectedPay;

    if (!quote.amount) {
      openInquiryMail({ planInfo, name, email, phone, message, payLabel: "무료 체험" });
      showToast("무료 체험 신청 메일을 열었습니다.");
      return;
    }

    requestPay({ plan: quote.plan, planInfo, name, email, phone, payKey: selectedPay });
  });

  const track = document.getElementById("marketsTrack");
  if (track && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    track.innerHTML += track.innerHTML;
  }

  document.getElementById("jumpTop")?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  document.getElementById("jumpBottom")?.addEventListener("click", () => {
    const bottom = Math.max(
      document.documentElement.scrollHeight,
      document.body.scrollHeight,
    );
    window.scrollTo({ top: bottom, behavior: "smooth" });
  });

  function pageShareUrl(hash) {
    const fixed = String(cfg.siteUrl || "").trim();
    let base;
    if (fixed) {
      base = fixed.replace(/\/+$/, "") + "/";
    } else {
      try {
        const loc = new URL(window.location.href);
        base = loc.origin + loc.pathname.replace(/index\.html$/i, "");
      } catch (_) {
        base = window.location.href.split("#")[0];
      }
    }
    const fragment = hash === undefined
      ? (window.location.hash || "")
      : (hash ? (String(hash).startsWith("#") ? String(hash) : `#${hash}`) : "");
    return `${base}${fragment}`;
  }

  async function copyShareUrl(hash) {
    const url = pageShareUrl(hash);
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(url);
      return url;
    }
    const area = document.createElement("textarea");
    area.value = url;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    area.remove();
    if (!ok) throw new Error("복사 실패");
    return url;
  }

  function shareLabel(hash) {
    const key = String(hash === undefined ? window.location.hash : hash || "")
      .replace(/^#/, "");
    if (key === "faq") return { title: "모두모두AI FAQ", text: "자주 묻는 질문 · AI 없이도 프로그램 이용료만" };
    if (key === "plans") return { title: "모두모두AI 요금", text: "프로그램 이용료 · AI는 쓸 때만" };
    if (key === "compare") return { title: "모두모두AI 비교", text: "일반 등록 도구와 비교" };
    return { title: "모두모두AI", text: "오픈마켓 상품 등록 프로그램 · AI 없이도 프로그램 이용료만" };
  }

  async function sharePage(hash) {
    const url = pageShareUrl(hash);
    const { title, text } = shareLabel(hash);
    if (navigator.share) {
      try {
        await navigator.share({ title, text, url });
        showToast("공유 창을 열었습니다.");
        return;
      } catch (error) {
        if (error?.name === "AbortError") return;
      }
    }
    await copyShareUrl(hash);
    showToast("링크를 복사했습니다. 카톡·문자에 붙여 넣으세요.");
  }

  function scrollToHashTarget() {
    const id = (window.location.hash || "").replace(/^#/, "");
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    requestAnimationFrame(() => {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  document.getElementById("sharePageLink")?.addEventListener("click", () => {
    sharePage().catch(() => showToast("링크를 복사하지 못했습니다."));
  });
  document.getElementById("sharePageLinkHero")?.addEventListener("click", () => {
    sharePage("").catch(() => showToast("링크를 복사하지 못했습니다."));
  });
  document.getElementById("shareFaqLink")?.addEventListener("click", () => {
    sharePage("faq").catch(() => showToast("FAQ 링크를 복사하지 못했습니다."));
  });

  window.addEventListener("hashchange", scrollToHashTarget);
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", () => {
      window.__modumoduOpenAtTop = false;
    });
  });
  function stayAtTop() {
    if (!window.__modumoduOpenAtTop) return;
    const root = document.documentElement;
    const previous = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
    root.style.scrollBehavior = previous;
  }

  window.addEventListener("scroll", stayAtTop, { passive: true });
  window.addEventListener("pageshow", stayAtTop);
  window.addEventListener("wheel", () => { window.__modumoduOpenAtTop = false; }, { passive: true, once: true });
  window.addEventListener("touchstart", () => { window.__modumoduOpenAtTop = false; }, { passive: true, once: true });
  window.addEventListener("keydown", () => { window.__modumoduOpenAtTop = false; }, { once: true });
  window.addEventListener("load", () => {
    if (window.__modumoduOpenAtTop) {
      stayAtTop();
      if (window.__modumoduSavedHash) {
        history.replaceState(null, "", location.pathname + location.search + window.__modumoduSavedHash);
        stayAtTop();
      }
      window.setTimeout(stayAtTop, 60);
      window.setTimeout(stayAtTop, 400);
      window.setTimeout(() => { window.__modumoduOpenAtTop = false; }, 1200);
      return;
    }
    if (window.location.hash) setTimeout(scrollToHashTarget, 80);
  });

  const joinForm = document.getElementById("join");
  const joinStatus = document.getElementById("joinStatus");

  joinForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(joinForm);
    const loginId = String(data.get("login_id") || "").trim();
    const password = String(data.get("password") || "");
    const phone = String(data.get("phone") || "").trim();
    const serial = String(data.get("serial") || "").trim();
    const api = String(cfg.memberApi || "").replace(/\/+$/, "");
    if (!api) {
      showToast("회원가입 주소가 아직 없습니다.");
      return;
    }
    if (joinStatus) joinStatus.textContent = "가입하는 중입니다.";
    fetch(`${api}/api/account/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ login_id: loginId, password, phone, serial }),
    })
      .then(async (response) => {
        const result = await response.json().catch(() => ({}));
        if (!response.ok) {
          const detail = result.detail || "가입하지 못했습니다.";
          if (joinStatus) joinStatus.textContent = detail;
          showToast(detail);
          return;
        }
        if (joinStatus) joinStatus.textContent = `${loginId} 님, 가입되었습니다. 테스트 주소에서 같은 아이디와 비밀번호로 들어가세요.`;
        showToast("회원가입이 되었습니다.");
        joinForm.reset();
      })
      .catch(() => {
        if (joinStatus) joinStatus.textContent = "가입 서버에 연결하지 못했습니다.";
      });
  });

  applyContact();
  syncPayButtons();
  updatePayHint();
  if (window.location.hash && !window.__modumoduOpenAtTop) scrollToHashTarget();
})();
