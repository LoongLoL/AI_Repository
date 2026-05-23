/**
 * File Server — Editor page interactivity.
 *
 * Exposes `initEditor(fileEncoded)` which the template calls with the
 * URL-encoded filename.
 */
function initEditor(fileEncoded) {
  const ta = document.getElementById("ta");
  const saveBtn = document.getElementById("saveBtn");
  const toast = document.getElementById("toast");

  let dirty = false;

  ta.addEventListener("input", function () {
    dirty = true;
  });

  async function save() {
    saveBtn.disabled = true;
    saveBtn.textContent = "⏳ 保存中...";

    try {
      const body = new URLSearchParams({
        file: fileEncoded,
        content: ta.value,
      });
      const resp = await fetch("/save", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body,
      });
      const data = await resp.json();

      toast.className = "toast " + (data.ok ? "ok" : "er");
      toast.textContent = data.ok
        ? "✅ 保存成功！"
        : "❌ 失败：" + (data.error || "unknown");
      toast.style.display = "";

      if (data.ok) dirty = false;
    } catch (e) {
      toast.className = "toast er";
      toast.textContent = "❌ 网络错误";
      toast.style.display = "";
    }

    saveBtn.disabled = false;
    saveBtn.textContent = "💾 保存";

    setTimeout(function () {
      toast.style.display = "none";
      toast.className = "toast";
    }, 3000);
  }

  saveBtn.addEventListener("click", save);

  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "s") {
      e.preventDefault();
      save();
    }
  });

  window.addEventListener("beforeunload", function (e) {
    if (dirty) {
      e.preventDefault();
      e.returnValue = "";
    }
  });
}
