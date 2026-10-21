"use strict";

const $ = (id) => document.getElementById(id);
const escapeHTML = (value) => String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
const valid = {
  flow: ["consumer", "business"], variant: ["modal", "inline"],
  state: ["entry", "empty", "permission", "review", "sending", "failed", "unknown", "success"],
  outcome: ["success", "failed", "unknown"], width: ["full", "narrow"]
};
const params = new URLSearchParams(location.search);
const mode = Object.fromEntries(Object.entries(valid).map(([key, values]) => [key, values.includes(params.get(key)) ? params.get(key) : values[0]]));
const tasks = [
  {id: "task-01", name: "春季模板", category: "活动", published: false},
  {id: "task-02", name: "入门模板", category: "指南", published: false},
  {id: "task-03", name: "回访模板", category: "服务", published: false}
];
const selection = new Set();
const feedback = [];
const draft = {service: "20 分钟线上体验", date: new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 10)};
let config;
let revision = 0;
let timer;
let exportURL;

function syncAddress() {
  const query = new URLSearchParams(mode);
  history.replaceState(null, "", "?" + query);
  $("state-label").textContent = {entry: "入口", empty: "空内容", permission: "权限不足", review: "确认信息", sending: "提交中", failed: "明确失败", unknown: "结果未知", success: "模拟成功"}[mode.state];
}

function setState(state) {
  revision += 1;
  clearTimeout(timer);
  mode.state = state;
  render();
}

function closeDialog() {
  if ($("confirmation").open) {
    $("confirmation").close();
  }
}

function resetTask() {
  selection.clear();
  tasks.forEach((task) => { task.published = false; });
  setState("entry");
  $("scenario").value = "entry";
}

function consumerEntry() {
  return `<h3>预约一次体验</h3><p class="lead">先选择服务与时间，再确认预约信息。示例费用为 0 元。</p>
    <form id="task-form"><div class="form-grid">
    <div><label for="service">体验服务</label><select id="service"><option>20 分钟线上体验</option><option>30 分钟方案咨询</option></select></div>
    <div><label for="date">预约日期</label><input id="date" type="date" required value="${escapeHTML(draft.date)}"></div></div>
    <div class="actions"><button type="submit" id="review-trigger">查看确认信息</button></div></form>`;
}

function businessEntry() {
  return `<h3>模板发布任务</h3><p class="lead">选择需要发布的模板，确认本次操作范围。数据仅用于讨论批量操作。</p>
    <div class="table-wrap"><table><caption class="sr-only">示例模板与发布状态</caption><thead><tr><th>选择</th><th>模板名称</th><th>分类</th><th>状态</th></tr></thead><tbody>
    ${tasks.map((task) => `<tr><td><label><input type="checkbox" data-row="${task.id}" ${selection.has(task.id) ? "checked" : ""} ${task.published ? "disabled" : ""}><span class="sr-only">选择${task.name}</span></label></td><td>${task.name}</td><td>${task.category}</td><td>${task.published ? "已发布（模拟）" : "待发布"}</td></tr>`).join("")}
    </tbody></table></div><p id="selection-status" class="selection-status" role="status">已选择 ${selection.size} 项</p>
    <div class="actions"><button type="button" id="review-trigger" ${selection.size ? "" : "disabled"}>批量发布所选项</button></div>`;
}

function confirmContent() {
  const summary = mode.flow === "consumer"
    ? `<p>服务：${escapeHTML(draft.service)}</p><p>日期：${escapeHTML(draft.date)}</p><p>示例费用：0 元</p>`
    : `<p>将发布 ${selection.size} 项：${tasks.filter((task) => selection.has(task.id)).map((task) => task.name).join("、") || "示例场景尚未选择项目"}。</p>`;
  return `<h3 id="confirmation-title" tabindex="-1">确认本次${mode.flow === "consumer" ? "预约" : "发布"}</h3>${summary}
    <p class="state-explanation">这是候选交互，确认只触发浏览器内模拟。此处尚未确定生产系统的撤销或取消规则。</p>
    <div class="actions"><button type="button" id="submit-task" ${mode.flow === "business" && !selection.size ? "disabled" : ""}>确认${mode.flow === "consumer" ? "预约" : "发布"}</button><button type="button" class="secondary" id="back-to-edit">返回修改</button></div>`;
}

function bindEntry() {
  if (mode.flow === "consumer") {
    $("service").value = draft.service;
    $("service").onchange = (event) => { draft.service = event.target.value; };
    $("date").oninput = (event) => { draft.date = event.target.value; };
    $("task-form").onsubmit = (event) => { event.preventDefault(); setState("review"); };
  } else {
    document.querySelectorAll("[data-row]").forEach((input) => {
      input.onchange = () => {
        if (input.checked) selection.add(input.dataset.row); else selection.delete(input.dataset.row);
        $("selection-status").textContent = `已选择 ${selection.size} 项`;
        $("review-trigger").disabled = !selection.size;
      };
    });
    $("review-trigger").onclick = () => setState("review");
  }
}

function beginSubmission() {
  if (mode.state !== "review" || (mode.flow === "business" && !selection.size)) return;
  setState("sending");
  const current = revision;
  timer = setTimeout(() => {
    if (current !== revision) return;
    if (mode.outcome === "success") tasks.filter((task) => selection.has(task.id)).forEach((task) => { task.published = true; });
    setState(mode.outcome);
  }, 700);
}

function render() {
  closeDialog();
  syncAddress();
  $("preview").classList.toggle("narrow", mode.width === "narrow");
  $("task-title").textContent = mode.flow === "consumer" ? "C 端示例 · 预约体验" : "B 端示例 · 批量任务";
  if (["entry", "review"].includes(mode.state)) {
    $("announcement").textContent = "";
    $("content").innerHTML = mode.flow === "consumer" ? consumerEntry() : businessEntry();
    bindEntry();
    if (mode.state === "review") {
      $("content").querySelectorAll("input, select, button").forEach((control) => { control.disabled = true; });
      if (mode.variant === "modal") {
        $("confirmation-content").innerHTML = confirmContent();
        $("confirmation").showModal();
      } else {
        $("confirmation-content").replaceChildren();
        $("content").insertAdjacentHTML("beforeend", `<section class="summary-box" aria-labelledby="confirmation-title">${confirmContent()}</section>`);
      }
      $("confirmation-title").focus();
      $("submit-task").onclick = beginSubmission;
      $("back-to-edit").onclick = () => { setState("entry"); $("review-trigger").focus(); };
    }
    return;
  }
  const results = {
    empty: ["暂无可用内容", "这个场景用于讨论空状态下的说明与下一步。可以重置，继续查看默认示例。", "返回示例入口"],
    permission: ["当前账号无操作权限", "这里需要项目明确谁可以操作、如何申请权限。原型不会提供可绕过权限的提交入口。", "返回示例入口"],
    sending: ["正在提交（模拟）", "正在演示提交中的反馈。当前按钮禁止重复提交；可通过左侧切换其他讨论场景。", null],
    failed: ["操作已明确失败（模拟）", "保留原选择，修改或确认后可以重试。本状态与没有收到结果的情况分别处理。", "保留选择并返回修改"],
    unknown: ["暂时无法确认结果（模拟）", "不把超时当作失败，也不直接重复提交。查询同一模拟任务后再展示结果。", "查询模拟任务"],
    success: ["操作已成功（模拟）", mode.flow === "consumer" ? "预约信息已在原型中确认。实际项目还需设计查看、改期和取消等适用入口。" : "所选模板的模拟发布结果已更新。可返回列表检查本次选择与状态。", "返回示例入口"]
  };
  const [title, explanation, action] = results[mode.state];
  $("content").innerHTML = `<section class="result"><span class="mark" aria-hidden="true">${mode.state === "success" ? "✓" : "·"}</span><h3 id="result-title" tabindex="-1">${title}</h3><p class="lead">${explanation}</p>${action ? `<div class="actions"><button id="result-action" type="button">${action}</button></div>` : ""}</section>`;
  $("result-title").focus();
  $("announcement").textContent = title;
  if (action) $("result-action").onclick = () => {
    if (mode.state === "unknown") {
      tasks.filter((task) => selection.has(task.id)).forEach((task) => { task.published = true; });
      setState("success");
    } else if (mode.state === "failed") { setState("entry"); $("review-trigger").focus(); }
    else if (mode.state === "success" && mode.flow === "business") { selection.clear(); setState("entry"); $("workspace").focus(); }
    else { resetTask(); $("workspace").focus(); }
  };
}

$("confirmation").addEventListener("cancel", (event) => {
  event.preventDefault();
  setState("entry");
  $("review-trigger").focus();
});
$("confirmation").addEventListener("keydown", (event) => {
  if (event.key !== "Tab") return;
  const controls = [...$("confirmation").querySelectorAll("button:not(:disabled), a[href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled)")];
  if (!controls.length) return;
  const first = controls[0];
  const last = controls[controls.length - 1];
  const heading = $("confirmation-title");
  if (event.shiftKey && (document.activeElement === first || document.activeElement === heading)) {
    event.preventDefault(); last.focus();
  } else if (!event.shiftKey && (document.activeElement === last || document.activeElement === heading)) {
    event.preventDefault(); first.focus();
  }
});
for (const key of ["flow", "variant", "outcome", "width"]) {
  $(key).value = mode[key];
  $(key).onchange = (event) => {
    mode[key] = event.target.value;
    if (key === "flow") resetTask(); else render();
  };
}
$("scenario").value = valid.state.includes(mode.state) && [...$("scenario").options].some((option) => option.value === mode.state) ? mode.state : "entry";
$("scenario").onchange = (event) => setState(event.target.value);
$("reset").onclick = resetTask;
$("feedback-form").onsubmit = (event) => {
  event.preventDefault();
  if (!config) return;
  const text = $("observation").value.trim();
  if (!text) return;
  const item = {id: `FB-${String(feedback.length + 1).padStart(3, "0")}`, prototype: config.id, version: config.version, ...mode, viewport: {width: innerWidth, height: innerHeight}, kind: $("evidence-kind").value, text};
  feedback.push(item);
  const li = document.createElement("li");
  li.textContent = text;
  const context = document.createElement("small");
  context.textContent = `${item.id} · v${item.version} · ${item.flow} / ${item.variant} / ${item.state} · ${item.kind}`;
  li.append(context);
  $("feedback-list").append(li);
  $("observation").value = "";
  $("export").disabled = false;
  $("feedback-status").textContent = "已记录，请导出后保存到项目。";
};
$("export").onclick = () => {
  const payload = JSON.stringify({prototype: config, feedback}, null, 2);
  $("feedback-json").value = payload;
  $("export-panel").hidden = false;
  if (exportURL) URL.revokeObjectURL(exportURL);
  exportURL = URL.createObjectURL(new Blob([payload], {type: "application/json"}));
  $("download-feedback").href = exportURL;
  $("download-feedback").download = `feedback-${config.id.replace(/[^a-zA-Z0-9_-]/g, "_")}-v${config.version.replace(/[^a-zA-Z0-9._-]/g, "_")}.json`;
  $("feedback-status").textContent = "已生成可复制的 JSON，也可使用下载链接。请确认文件已保存，再将反馈及决定纳入项目。";
};

fetch("prototype.json").then((response) => {
  if (!response.ok) throw new Error("无法读取原型配置");
  return response.json();
}).then((data) => {
  config = data;
  document.title = config.title;
  $("title").textContent = config.title;
  $("version").textContent = `v${config.version} · ${config.status}`;
  $("question").textContent = config.question;
  $("source").textContent = config.source;
  $("simulation").textContent = config.simulation;
  for (const target of config.acceptance) {
    const li = document.createElement("li");
    li.textContent = target;
    $("acceptance").append(li);
  }
  render();
}).catch((error) => {
  $("content").textContent = error.message + "，请通过 prototype.py serve 启动并刷新。";
  $("version").textContent = "配置未加载";
  $("feedback-form").querySelector("button").disabled = true;
});
