---
id: TEST-native-subagent-technical
title: 原生子 Agent 注册技术验证
status: current
version: 1
owner: acceptance
---

# 技术验证拆解与对齐 Review

## 有效输入与版本

用户原始要求与授权、[设计 v3](design.md)、[计划 v1](implementation-plan.md)、[用例 v1](acceptance-cases.md)，基线 adb8bed。执行前绑定代码指纹与完整差异。本轮无独立产品 RULE，以设计 AC1–AC7 为预期来源，以下设计约束不创建新业务规则。

## 用例与技术检查映射

| 检查 | 用户用例 | 来源及链路 | 必需证据 |
| --- | --- | --- | --- |
| CHK-01 | TC-01/02 | AC1/2，安装/迁移 | 隔离 CLI 集成、六文件与归属读回 |
| CHK-02 | TC-03 | AC1/2，升级资源 | 特殊路径目标实际解码、存在及旧根排除 |
| CHK-03 | TC-04 | AC3，真实启用/缓存/归属/正文 | 独立异常、实际版本错误/缺失及来源错配拒绝、修复重试 |
| CHK-04 | TC-05/06 | AC4，预检至 CLI 边界 | 名称样本、文件快照、CLI 调用序列 |
| CHK-05 | TC-07 | AC5，失败/回滚/重试 | 多位置写入异常、字节及存在性对照 |
| CHK-06 | TC-08 | 设计四，锁/提交前复检 | 受控期间修改、独立进程占用拒绝/释放重试 |
| CHK-07 | TC-09/10 | AC6，预检/移除/清理 | 各状态读回与 CLI 移除是否发生 |
| CHK-08 | TC-11 | AC5/6，卸载恢复 | 角色/归属/仓库记录删除故障、字节恢复/重装 |
| CHK-09 | TC-12 | AC7，目录及配置不变量 | 自定义/默认目录及无关配置前后对照 |
| CHK-10 | TC-13 | AC1/3/7，实际交付 | 主 Agent 真实 CLI，验收者独立读回 |
| CHK-11 | TC-14 | AC7、设计七，原生宿主 | 实际角色选择调用及元数据；识别和执行分开 |
| CHK-12 | TC-15 | 用户要求、设计二/六 | 官方来源、宿主版本与交付说明边界 |
| CHK-13 | TC-16 | 设计七、计划三 | 同一断言旧缺失失败/新通过 |
| CHK-14 | TC-16 | 仓库升级约定 | 双端同步、三清单/资源、构建/实际安装一致 |

## 逐项执行设计

### 实际入口绑定

自动化执行入口：仓库根目录运行 `python3 -m unittest discover -s tests -p 'test_native_agents.py'` 和 `python3 -m unittest discover -s tests -p 'test_plugin_installation.py'`。下表测试名分别属于这两文件的 NativeAgentTests/AgentNameTests、PluginPackageTests；表中人工补充亦须实际执行并留结果，不能凭自动化数量替代。

| 检查 | 自动化测试或可执行核验入口 |
| --- | --- |
| CHK-01 | 安装 test_install_check_remove_preserve_user_configuration；native test_install_repeat_check_and_links_under_special_path；CHK-13 的旧无注册到新 install 同条件夹具 |
| CHK-02 | native test_upgrade_updates_all_resource_paths_and_keeps_other_configuration、test_install_repeat_check_and_links_under_special_path |
| CHK-03 | 安装 test_corrupt_installed_cache_does_not_register_roles、test_active_version_and_source_must_match_before_registration；native test_missing_roles_are_detected_and_repaired、test_registry_foreign_source_and_malformed_shape_are_rejected。补充在临时夹具分别修改 NativeAgents.state 的 owner/files集合/指纹/source_root/plugin_root，删除状态，调用 check，逐次恢复原字节后换下一场景；manager 的 installed_entry 模拟 enabled=False 再 check，均须 ValueError |
| CHK-04 | 安装 test_native_conflict_stops_before_plugin_cli；native test_unowned_modified_and_linked_targets_are_preserved、test_different_filename_same_name_is_conflict、test_directories_and_registry_cannot_be_links，AgentNameTests 全部；补充将固定目标建成目录后 install，必须预检拒绝 |
| CHK-05 | native test_file_error_rolls_back_entire_registration_and_record、test_first_install_error_leaves_no_owned_files_and_can_retry；故障位置4/7/8，升级目标内容须实际不同 |
| CHK-06 | native test_changes_during_cli_are_not_overwritten、test_lock_rejects_an_independent_process_then_allows_retry |
| CHK-07 | 安装 test_install_check_remove_preserve_user_configuration、test_modified_owned_role_stops_remove_before_plugin_cli；native test_remove_owned_only_and_idempotent、test_unowned_modified_and_linked_targets_are_preserved；补充无state且有个人同名文件，remove后保持字节 |
| CHK-08 | native test_remove_failure_rolls_back_files_and_allows_reinstall，故障位置3/7/8，随后重新安装 |
| CHK-09 | 安装 test_install_check_remove_preserve_user_configuration；native特殊用户目录全部测试。补充临时HOME与CODEX_HOME取不同路径，默认目录放哨兵config/AGENTS/角色，指定目录执行生命周期，前后逐字节比较 |
| CHK-10 | 主 Agent 真实 `python3 scripts/manage_plugin.py install` / `check`；验收者读取返回路径、registry六项、缓存 package-files.json 与源码逐文件 SHA256、六份正文链接 |
| CHK-11 | 桌面捆绑CLI新进程；普通exec JSON不足时，app-server的thread/start使用ephemeral=true、experimentalRawEvents=true捕获实际spawn_agent及返回。原始探针`.dev-flow/native-app-server-probe.py`，独立`native-independent-acceptance/native-raw-readback.py`。六个agent_type不继承历史，核对选择参数、自动加载及completed，未实证不通过 |
| CHK-12 | 读取 docs/plugin.md 页面安装小节，核对官方 Subagents、Package your plugin、Hooks 页面及 CLI --version；记录支持与未知，不执行绕过信任 |
| CHK-13 | git show adb8bed:scripts/manage_plugin.py 提取旧模块到忽略目录；同临时源码/CLI先旧install断言6角色缺失，再新install断言6角色且check通过，原始记录 .dev-flow/native-registration-baseline.json |
| CHK-14 | sync_host_agents.py --check、manage_plugin.py build；三清单 version==0.6.0，生成 six roles/16 skills；最终 install/check 对照源码与缓存 |

### 共用环境与证据

仅在临时用户目录操作；测试验收者不注册真实个人角色。使用临时 CODEX_HOME、源码夹具与模拟 CLI，记录入口/断言/退出码/候选。主 Agent 唯一操作实际安装，验收者只读核验。先核对自动化测试名称和断言，再按映射绑定；不能以文件存在当作测试已执行。

### 安装、升级与检查

空目录、旧无注册及已有注册分别 install/check。六目标为普通文件，状态字段和完整名称集合一致。所有本地 Markdown 目标先移除尖括号并按编码前的 # 分离片段，再百分号解码；含空格、括号、#、> 缓存根必须精确落到实际缓存资源。升级排除旧根。

检查异常分别覆盖缺失/修改/链接、缺失或非法归属、角色集合/指纹/来源/缓存根不符、缓存损坏、插件禁用以及实际启用版本错误/缺失。仅缺失受管文件可重新 install 修复；冲突不得接管。

### 冲突、失败与并发

固定目标文件/链接/目录、管理目录/记录链接、不同文件真实同名与正常外来角色分别核验。名称样本含基础/字面量/多行字符串、引号键、Unicode、注释、嵌套数组/inline table 和表后 name；不确定或无效结构明确拒绝。

在角色、归属及仓库记录写入位置注入普通异常，首次及升级分别验证字节/存在性；删除阶段同样注入错误。解除故障后重装通过，不能把字节恢复解释成 CLI 回退或旧资源仍可运行。提交前修改目标必须拒绝覆盖；跨进程锁占用时返回忙，解除后成功重试，测试仅有锁文件或同进程线程不足以证明跨进程。

### 卸载与配置保护

正常/缺失受管文件可清理；修改/链接/来源冲突在 CLI 移除前整体拒绝，无归属不删除个人角色。自定义目录含空格，保留默认目录、无关角色、config.toml 与 AGENTS.md 原字节；不新增固定模型设置。

### 实际交付与宿主

主 Agent 保存安装前只读状态，运行最终 install/check；验收者独立检查缓存版本/源指纹、六角色、归属及全部链接。新进程需实际选择原生角色名进行最小只读派发，保留选择参数、结果及角色元数据；若只演练部分角色，仅声明实际覆盖。当前通用 collaboration 派发无角色参数，不能充当原生证据。入口不可用如实保留未执行和刷新方法。

### 页面与候选一致性

复核官方插件/角色/Hooks 文档、宿主版本与调查结果；未说明的能力不写成平台绝对不可能。页面安装没有已核实自动注册入口时，文档明确使用脚本。旧新相同夹具的六角色存在断言，旧因目标缺失失败、新通过；环境/导入失败不算旧失败。生成、构建与实际安装绑定最终内容，包内内容改变后重新构建/安装/核验。

## 对齐 AI Review

未主笔 design_review 已对用例与技术验证 v1 独立复核通过，正式结果见[验收报告](acceptance-result.md)。执行报告按 TC 汇总映射，未执行或失败不标通过；页面调查完成不等同页面自动注册通过。
