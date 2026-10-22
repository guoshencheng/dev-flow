# 技术图示示例

以下均为虚构目标方案，只示范[图型选择与表达方法](../../../references/architecture/technical-diagrams.md)，不是本插件或某个项目的实际架构。采用时只保留本次需要的图，替换参与者、边界、协议、状态和失败语义；相邻正文补充源码/契约依据及相关 ARC/OUT，不将示例默认升级为项目要求。

## 分区、分层架构总览

问题：控制面与内网执行端各负责什么，如何通信？目标示意；外框分别代表网络区域和主机，控制面子框代表进程/运行单元，编排器内框代表同一进程中的逻辑组件。包含不表示调用，带标签的边表示运行通信或数据访问。图省略鉴权、重连与多副本细节。

```mermaid
flowchart TB
  user["使用者"]
  subgraph cloud["公网 · 控制面 / Cloud"]
    web["Dashboard / REST API · 管理入口"]
    subgraph orch["编排服务进程"]
      direction LR
      coordinator["协调模块 · 组织任务"]
      scheduler["调度模块 · 分配执行端"]
      registry["注册模块 · 管理在线执行端"]
      coordinator -->|"进程内调用：请求调度"| scheduler
      scheduler -->|"进程内查询：可用执行端"| registry
    end
    db[("任务 / 事件存储")]
    gateway["Worker Gateway · 连接与消息路由"]
    web -->|"提交 / 查询任务"| orch
    orch -->|"读写任务与事件"| db
    orch -->|"请求派发任务"| gateway
    gateway -->|"转交结果 / 连接状态"| orch
  end
  subgraph intranet["内网 · 执行区"]
    subgraph host["执行主机 A"]
      worker["Worker Daemon · 连接与执行管理"]
      executor["执行服务 · 运行任务"]
      workspace["工作目录 / Shell · 任务资源"]
      worker -->|"本机 API：启动 / 查询执行"| executor
      executor -->|"读写文件 / 运行命令"| workspace
    end
  end
  user -->|"HTTPS：管理任务"| web
  worker -->|"主动建立 WSS / TLS 连接"| gateway
  gateway -->|"已建立通道：派发任务"| worker
  worker -->|"已建立通道：上报结果"| gateway
```

读图结论：控制面管理任务与调度，执行端在内网运行任务；连接由 Worker 发起，任务通过已建立连接下发。网络连通不证明鉴权或权限已实现，实际设计仍需给出相关契约。

## 模块依赖图

问题：业务策略怎样避免依赖外部 SDK？目标示意；所有实线箭头表示源码依赖，虚线表示实现端口。装配根同时引用用例与适配器并完成注入，省略无关模块；图中方向不是请求执行顺序。

```mermaid
flowchart LR
  root["装配根"] --> usecase["任务用例"]
  root --> adapter["外部执行适配器"]
  usecase --> domain["领域规则"]
  usecase --> port["执行端口 · 由用例层拥有"]
  adapter -.->|"实现"| port
  adapter --> sdk["外部服务 SDK"]
```

读图结论：用例通过自己拥有的端口调用外部能力；运行时会进入适配器，源码依赖仍朝向内层契约。

## 跨端协作时序图

问题：用户提交任务后，何时算受理，何时真正完成？目标示意；实线消息表示请求/调用，虚线表示响应，开放箭头表示不等待业务完成的异步消息。展示领取冲突和执行失败，鉴权失败、存储失败与连接中断另按实际契约展开。

```mermaid
sequenceDiagram
  actor U as 用户
  participant API as 任务 API
  participant DB as 任务存储
  participant G as 网关
  participant W as Worker
  Note over G,W: 复用 Worker 主动建立的连接
  U->>API: 提交任务
  API->>API: 鉴权与参数校验
  API->>DB: 保存 queued 状态
  DB-->>API: 提交成功，返回任务 ID
  API-->>U: 已受理，返回任务 ID
  API-)G: 请求派发任务
  G-)W: 下发任务
  W->>G: 请求领取任务
  G->>API: 转交领取请求
  API->>DB: 原子条件更新 queued → running
  DB-->>API: 更新结果
  alt 条件更新失败：已取消或被领取
    API-->>G: 拒绝本次领取
    G-->>W: 不执行任务
  else 条件更新成功
    API-->>G: 允许执行
    G-->>W: 确认领取
    W->>W: 执行任务
    alt 执行成功
      W-)G: 上报结果
      G-)API: 转交成功结果
      API->>DB: 保存 succeeded 与结果
    else 执行失败
      W-)G: 上报失败原因
      G-)API: 转交失败结果
      API->>DB: 保存 failed 与原因
    end
    DB-->>API: 终态提交成功
  end
  U->>API: 按任务 ID 查询
  API->>DB: 读取状态与结果
  DB-->>API: 当前持久化状态
  API-->>U: 展示当前状态，终态可查看结果或失败原因
```

读图结论：受理响应只证明排队记录已保存；查询时可能仍未结束，成功需执行完成且结果持久化。图中的异步派发不证明消息可靠交付；若存在可靠投递要求，设计必须补充丢失、重复及恢复机制。

## 条件决策流程图

问题：任务处于不同状态时能否取消？目标示意；菱形表示判断，边注明判断结果，矩形表示动作。这里只表达取消规则，实际参与者之间的调用顺序需另用时序图。

```mermaid
flowchart TD
  start(["请求取消任务"]) --> auth{"身份与权限有效？"}
  auth -->|"否"| denied["拒绝操作，保持原状态"]
  auth -->|"是"| state{"当前任务状态？"}
  state -->|"queued"| save["原子条件更新 queued → cancelled"]
  save --> result{"更新成功？"}
  result -->|"否：并发变化"| reload["重新读取状态并提示冲突"]
  result -->|"是"| cancelled["返回已取消"]
  state -->|"running"| reject["本示例不支持中断，说明原因"]
  state -->|"终态"| unchanged["返回已有终态，不重复变更"]
  denied --> finish(["结束"])
  reload --> finish
  cancelled --> finish
  reject --> finish
  unchanged --> finish
```

读图结论：仅排队任务可取消；并发启动可能使取消失败，条件更新防止覆盖已运行状态。这是示例规则，是否支持运行中取消由实际产品/执行契约决定。

## 生命周期状态图

问题：任务的合法状态转换是什么？与前两图一致的目标示意；框表示持久化状态，转换标注触发事件与条件，黑点表示初始或终止。没有出边的终态不允许原地重试，重试另建任务。

```mermaid
stateDiagram-v2
  state "排队 queued" as queued
  state "执行中 running" as running
  state "成功 succeeded" as succeeded
  state "失败 failed" as failed
  state "已取消 cancelled" as cancelled
  [*] --> queued: 提交并持久化
  queued --> running: Worker 领取 [条件更新成功]
  queued --> cancelled: 取消 [条件更新成功]
  running --> succeeded: 结果持久化成功
  running --> failed: 失败原因持久化成功
  succeeded --> [*]
  failed --> [*]
  cancelled --> [*]
```

读图结论：取消只允许从 queued 进入 cancelled；终态不可回退。此图省略派发中间态与超时政策，真实项目不能据此推导其重试/恢复规则。

## 实体关系图

问题：任务和事件如何关联？目标示意；字段只列关系所需的键，连线注明基数；任务服务拥有这两类数据。完整字段、约束、删除和保留策略以项目 schema 为准。

```mermaid
erDiagram
  TASK ||--o{ TASK_EVENT : "包含"
  TASK {
    string id PK
    string status
  }
  TASK_EVENT {
    string id PK
    string task_id FK
    string event_type
  }
```

读图结论：每个事件属于一个任务，一个任务可暂时没有事件。ER 图不说明事件投递顺序，也不证明采用事件溯源；需要这些保证时另写契约。
