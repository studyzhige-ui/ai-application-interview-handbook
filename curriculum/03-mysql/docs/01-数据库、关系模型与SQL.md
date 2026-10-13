# 01｜数据库、关系模型与 SQL：数据怎样被 MySQL 管理

> [!TIP]
> **🎯 本章目标**
>
> 建立 MySQL 最基础的一层知识模型：知道关系型数据库怎样表示业务数据，一张表怎样规定记录的身份和基本规则，MySQL Server 与 InnoDB 分别负责什么，以及怎样用 SQL 完成单表数据最常见的增删改查。
>
> 学完后，应该能够把一个简单业务对象落成表结构，读懂常见的 `CREATE TABLE`，并安全地写出基础 `INSERT / SELECT / UPDATE / DELETE`。

## 0. 一份 JSON 数据，什么时候开始需要数据库？

假设任务应用最开始只有几条数据：

```json
[
  {"id": 101, "title": "学习 MySQL", "status": "pending"},
  {"id": 102, "title": "完成项目", "status": "done"}
]
```

直接放进 JSON 文件没有问题。但应用真正开始使用后，很快会出现一系列具体要求：每条任务都必须有标题；两条任务不能使用同一个 `id`；没填写状态时希望自动使用 `pending`；优先级可以暂时未知；只查询 `pending` 的任务；按创建时间找到最新的 20 条；只修改 `id = 101` 的那一条任务。

这时问题已经不只是“把数据存起来”，而是：

> **怎样把业务数据组织成结构明确、有身份、有基本规则，而且能够稳定查询和修改的数据？**

关系型数据库就是在解决这类问题。

> [!IMPORTANT]
> **💡 本章核心认知：数据库不是一个更大的 JSON 文件；数据具备明确的结构和约束规则，应用可以通过 SQL 声明需要哪些数据、要怎样修改，再由 MySQL 负责管理这些数据。**

---

## 🗺️ 本章知识图

```text
业务数据怎样进入 MySQL？
│
├── 1. 关系型数据库到底在管理什么？
│   ├── Database / DBMS / MySQL
│   └── Table / Row / Column
│
├── 2. 一张表怎样规定身份和基本规则？
│   ├── 一行代表什么
│   ├── Column / Data Type
│   ├── Primary Key
│   ├── NULL / NOT NULL
│   └── DEFAULT
│
├── 3. MySQL Server 和 InnoDB 分别负责什么？
│   ├── Client
│   ├── MySQL Server
│   └── Storage Engine
│       └── InnoDB 是其中一种实现
│
└── 4. 单表数据怎样用 SQL 增删改查？
    ├── INSERT
    ├── SELECT
    │   ├── WHERE / AND / OR / IN / LIKE / IS NULL
    │   ├── ORDER BY
    │   └── LIMIT
    ├── UPDATE
    ├── DELETE
    └── 参数绑定
```

---

## 1. 关系型数据库到底在管理什么？

关系型数据库管理的不是一堆没有结构的值，而是**按照明确结构保存的业务事实**。同一类事实放在一张表里：列规定每条记录有哪些属性，一行保存一条具体记录。数据库管理系统负责保存这些数据，并提供统一的查询、修改和规则约束能力。

这里最容易混淆的是 `Database`、`DBMS` 和 `MySQL`：

| 名称 | 它是什么 | 核心职责 |
|---|---|---|
| **Database（数据库）** | 被组织和管理的数据集合 | 数据本身以及它的结构 |
| **DBMS（数据库管理系统）** | 管理数据库的软件 | 负责创建、查询、修改和管理数据 |
| **MySQL** | 一种关系型 DBMS | 本手册核心聚焦的关系型数据库管理系统 |

在日常交流里，人们经常直接说“用了 MySQL 数据库”，这没有问题；但理解原理时要分清：**MySQL 是管理数据的软件，不是某一张表里的数据本身。**

---

### 1.1 “关系型”到底是什么意思？

假设任务系统有这些数据：

| id | title | status |
|---:|---|---|
| 101 | 学习 MySQL | pending |
| 102 | 完成项目 | done |
| 103 | 修改简历 | pending |

关系型数据库把同一类数据按照固定属性组织起来。这里 `tasks` 是一张 **Table（表）**，代表同一类记录的集合；`id = 101` 这一整条是一个 **Row（行 / Record，记录）**，代表一条具体记录；而 `id`、`title`、`status` 则是 **Column（列）**，代表这类记录都具有的某个属性。

“关系型”这个名字来自 **Relational Model（关系模型）**。在 SQL 数据库里，表是最直接接触到的表示形式。它更基础的一层是：**同一类事实按照一组明确的属性组织起来，每条记录都遵守这套结构。** 例如 `tasks` 表规定每条任务都有 `id, title, status, priority, created_at`，那么新插入的每条任务，都要严格按照这套表结构来表达。

---

### 1.2 表结构和表里的数据不是一回事

必须分清两个概念的边界：
- **Schema（表结构）**：规定数据的形状和规则，回答“一条任务应该长什么样”（如 `id` 是大整数、`title` 是文本、`created_at` 是日期时间）。
- **Row（数据行）**：按照这套结构保存的具体数据事实，回答“某一条具体任务的值是什么”（如 `101 | 学习 MySQL | pending | 2 | 2026-10-01 09:00:00`）。

数据库的核心价值之一，正是**结构和数据被统一管理与强约束，而不是让每条记录随意长成不同样子。**

---

## 2. 一张表怎样把业务对象变成有身份、有基本规则的数据？

设计一张表时，最先考虑的不是 `CREATE TABLE` 怎么写，而是四个业务事实：**一行到底代表什么；这一行需要哪些属性；怎样唯一识别这一行；哪些值必须有，哪些允许暂时缺失，省略时有没有默认值。** 确定这些后，DDL 只是把规则写成数据库可执行的定义。

假设这里规定“一行表示一条任务”，最小需求是：每条任务都有稳定且唯一的 `id`；`title` 必须填写；`status` 必须有值，省略时默认 `pending`；`priority` 可以暂时未知；`created_at` 必须记录。对应的建表语句：

```sql
CREATE TABLE tasks (
    id BIGINT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority INT,
    created_at DATETIME NOT NULL
) ENGINE = InnoDB;
```

---

### 2.1 Column 和 Data Type：一列要保存什么值？

每一列定义由“列名 + 数据类型”组成。例如 `title VARCHAR(100)` 表示创建一个叫 `title` 的列，保存长度可变且最长 100 字符的文本。

初学阶段最常用的基础数据类型：

| 类型 | 常见用途 | 示例 |
|---|---|---|
| `INT` | 普通整数 | 数量、优先级 |
| `BIGINT` | 范围更大的整数 | ID、计数 |
| `VARCHAR(n)` | 长度可变的文本 | 姓名、标题、状态 |
| `DECIMAL(p,s)` | 需要精确小数的数值 | 金额 |
| `DATETIME` | 日期和时间 | 创建时间 |

数据类型在本质上是在规定**这一列允许保存哪一类合法值**。例如涉及精确计算的金额不应滥用浮点数，任务标题也不应定义成整数。

---

### 2.2 Primary Key：怎样稳定地认出“就是这一条记录”？

假设有两条任务的标题都叫 `学习 MySQL`，或者标题后续被用户修改了，`title` 就不能稳定地区分记录。记录的长期身份需要一个全局稳定标识。

`id BIGINT PRIMARY KEY` 定义了 **Primary Key（主键）**：表中用来唯一识别一条记录的一列或一组列。主键值必须唯一且非空。对于当前 `tasks` 表，`id = 101` 表达的就是**“编号 101 的这一条特定任务”**。主键首先解决的是记录的物理与业务身份，后面无论修改、删除还是被其他表引用，都依赖主键确立对象边界。

---

### 2.3 `NULL`：没有已知值，不等于 0 或空字符串

假设任务 103 暂时还没确定优先级，它的 `priority` 值为 `NULL`。`NULL` 表示**当前没有一个已知的有效值**。

它和具体的值有本质区别：`0` 是已知的数字 0，`''` 是已知长度为 0 的空文本。因此在 SQL 中不能用 `= NULL` 比较（其三值逻辑计算结果不是普通的 `TRUE`），而必须使用专门的操作符：

```sql
WHERE priority IS NULL;     -- 筛选缺失优先级的记录
WHERE priority IS NOT NULL; -- 筛选已有优先级的记录
```

---

### 2.4 `NOT NULL` 与 `DEFAULT`：必填与缺省规则

- **`NOT NULL`（非空约束）**：要求该列必须有已知值。例如 `title VARCHAR(100) NOT NULL` 保证任务不能没有标题。注意：`NOT NULL` 只禁止 `NULL`，不会阻止应用写入空字符串 `''`，更深层的文本有效性需结合业务或 CHECK 约束处理。
- **`DEFAULT`（缺省值）**：规定插入数据时若省略该列，自动使用的替补值。例如 `status VARCHAR(20) NOT NULL DEFAULT 'pending'`。

```sql
INSERT INTO tasks (id, title, priority, created_at)
VALUES (104, '准备面试', 3, '2026-10-01 12:00:00');
```

由于显式省略了 `status`，MySQL 会自动填入默认值 `'pending'`。`DEFAULT` 解决的是缺省填充，而不是合法枚举值范围校验。

---

### 2.5 把 DDL 翻译回业务规则

完整建表定义中的每一行都在严格映射业务规则：

| 定义 | 业务含义 |
|---|---|
| `id BIGINT PRIMARY KEY` | 每条任务都有一个大整数 ID，且 ID 唯一、非空 |
| `title VARCHAR(100) NOT NULL` | 每条任务都必须有标题，最长 100 字符 |
| `status VARCHAR(20) NOT NULL DEFAULT 'pending'` | 每条任务都必须有状态；省略时默认 `pending` |
| `priority INT` | 优先级是整数；当前定义允许暂时缺失（NULL） |
| `created_at DATETIME NOT NULL` | 每条任务都必须有创建时间 |
| `ENGINE = InnoDB` | 这张表交给 InnoDB 存储引擎管理 |

记住：**表结构是业务规则的强约束体现，DDL 只是把规则翻译给数据库。**

---

## 3. SQL 发给 MySQL 后，MySQL Server 和 InnoDB 分别负责什么？

MySQL 整体架构可以清晰地划分为三层：**客户端（Client）** 负责发送请求与接收结果；**MySQL Server** 负责理解 SQL 语义、优化并调度执行；**Storage Engine（存储引擎）** 负责具体表数据和索引的物理存取与事务保障。InnoDB 是 MySQL 9.7 默认的通用存储引擎。

```text
Client
  │ 发送 SQL / 接收结果
  ↓
MySQL Server
  │ 理解 SQL、选择执行方法、组织执行
  ↓
Storage Engine 接口
  ├── InnoDB  ← 默认通用引擎（负责表数据/索引/事务/锁）
  └── 其他引擎（如 MyISAM、Memory 等）
```

理解架构时务必区分层级：**InnoDB 是 MySQL 的一种具体存储引擎，不是 Server 的同义词。**

---

### 3.1 Client、Server 与 Storage Engine 的职责分工

- **Client（客户端）**：命令行 `mysql`、图形化工具 DataGrip、以及应用程序中的连接驱动（Driver）。它们负责建立网络连接、发送 SQL 字符串并展示返回的数据集，本身不执行数据存储与检索。
- **MySQL Server**：负责解析收到的 SQL 文本。它首先进行语法解析与表/列对象校验（如写错关键字报错、列名不存在报错），接着由优化器评估不同的访问路径并生成执行计划，最后由执行器协调调度。
- **Storage Engine（以 InnoDB 为例）**：Server 决定了执行计划后，真正向磁盘或内存缓冲读写行数据与维护索引的工作均由存储引擎完成。InnoDB 同时提供了行级锁、多版本并发控制（MVCC）与崩溃恢复能力。

> [!IMPORTANT]
> **💡 实用的极简心智模型：应用通过 Client 把 SQL 发给 Server；Server 负责理解并决定“怎么做”；底层真正摸到数据行和索引页的操作，全部委托给 InnoDB 完成。**

---

## 4. 单表数据怎样用 SQL 安全地增删改查？

SQL 是一种**声明式语言**：应用只描述“要什么数据、想做何种修改”，而不必自己编写磁盘寻道与遍历算法。单表基础 CRUD 操作包含：`INSERT`（增）、`SELECT`（查）、`UPDATE`（改）、`DELETE`（删）。

掌握基础 SQL 的关键不仅在于语法拼写，更在于树立工程防御习惯：明确列值对应关系、严格用 `WHERE` 控制影响范围、以及始终使用**参数绑定**防止 SQL 注入。

---

### 4.1 `INSERT`：把业务记录写入表中

一次插入可以写入单行或多行，列清单与值清单必须按位置严格一一对应：

```sql
INSERT INTO tasks (id, title, status, priority, created_at)
VALUES
    (101, '学习 MySQL', 'pending', 2,    '2026-10-01 09:00:00'),
    (102, '完成项目',   'done',    1,    '2026-10-01 10:00:00'),
    (103, '修改简历',   'pending', NULL, '2026-10-01 11:00:00');
```

在实际工程中，始终显式声明列名（如 `tasks(id, title...)`），比省略列名直接 `VALUES(...)` 安全得多，能避免因后续表字段顺序调整而导致的脏数据写入。

---

### 4.2 `SELECT`：从表中取出需要的数据

```sql
SELECT id, title
FROM tasks;
```

其语义为：从 `tasks` 表中提取数据，仅返回 `id` 与 `title` 两列。工程实践中应尽量避免无节制的 `SELECT *`，明确写出所需列不仅意图清晰，还能减少不必要的网络传输并为底层索引覆盖创造可能。

---

### 4.3 `WHERE` 与条件组合：行级过滤

`WHERE` 决定哪些行被保留。常用比较运算符包括 `=`、`<>`（不等于）、`>`、`>=`、`<`、`<=`。

```sql
SELECT id, title
FROM tasks
WHERE status = 'pending'
  AND (priority >= 2 OR priority IS NULL);
```

- **`AND / OR` 逻辑组合**：当逻辑复杂时，务必使用**圆括号 `()`** 显式框定优先级，而不是依赖运算符默认结合律，这能让业务意图一眼看懂。
- **`IN` 候选值筛选**：`WHERE id IN (101, 103)` 等价于多组 `OR` 连接，在多值并列时可读性更佳。
- **`LIKE` 模糊匹配**：`%` 匹配零个或多个任意字符，`_` 匹配单个字符。例如 `title LIKE '学习%'` 筛选前缀，`title LIKE '_习%'` 匹配第二个字为“习”的记录。
- **`IS NULL` 缺失值筛选**：筛选未知值必须写 `priority IS NULL` 或 `priority IS NOT NULL`。

---

### 4.4 `ORDER BY` 与 `LIMIT`：结果排序与数量截断

SQL 表在逻辑上是无序集合。如果不显式指定 `ORDER BY`，数据库返回的记录顺序是未定义的，绝不能依赖物理存储碰巧返回的顺序。

```sql
SELECT id, title, created_at
FROM tasks
ORDER BY created_at DESC, id DESC
LIMIT 2;
```

- **`ORDER BY`**：`ASC` 表示升序（默认），`DESC` 表示降序。当首选排序列（如 `created_at`）可能存在重复值时，追加具有唯一性的次级排序列（如 `id DESC`），可以确保分页与重刷结果集时的绝对稳定性。
- **`LIMIT n`**：限制最终返回的记录行数。注意 `LIMIT` 仅仅截断最终交付给客户端的结果条数，它本身并不直接等同于底层数据库只需扫描很少的数据，实际执行代价取决于访问路径。

理解单表查询语义时，可按逻辑执行顺序串联：  
`FROM (找哪张表) → WHERE (留哪些行) → SELECT (取哪些列) → ORDER BY (按什么排) → LIMIT (最终拿几条)`。

---

### 4.5 `UPDATE` 与 `DELETE`：明确修改边界

- **`UPDATE`**：修改现有行的列值。
  ```sql
  UPDATE tasks
  SET status = 'done', priority = 1
  WHERE id = 101;
  ```
- **`DELETE`**：从表中删除记录。
  ```sql
  DELETE FROM tasks
  WHERE id = 104;
  ```

> [!WARNING]
> **没有 `WHERE` 条件的 `UPDATE` 或 `DELETE` 会直接波及全表所有行！**  
> 在生产或联调执行不熟悉的变更时，先将操作改写为相同条件的 `SELECT` 预览受影响数据集，是每个合格工程师的基本安全本能。

---

### 4.6 程序里的值不要直接拼进 SQL：使用参数绑定

在业务代码中拼接 SQL 字符串是不安全的：

```text
// 极易导致 SQL 注入的危险写法：
"SELECT id, title FROM tasks WHERE status = '" + userInput + "'"
```

工业界标准的防线是**参数绑定（Parameter Binding / Prepared Statement）**：

```text
SQL 模板： SELECT id, title FROM tasks WHERE status = ? AND priority >= ?;
参数列表： ["pending", 2]
```

参数绑定的核心逻辑是：**SQL 语法骨架首先被编译解析，业务输入仅作为纯粹的数据字面量填入占位符，绝不会被误解为 SQL 语法标记。**

> [!IMPORTANT]
> **💡 参数边界法则：**
> - **业务数据值**：一律走参数绑定（`?` 占位符）。
> - **表名、列名、排序方向（ASC/DESC）等语法结构**：不能使用普通参数占位符替代。若必须动态指定，必须由后端代码经过严格的固定白名单校验（Allowlist）后安全组装。

---

## 本章总结

关系型数据库管理的是结构化的业务事实。表（Table）组织同类记录，行（Row）承载具体数据，列（Column）定义数据属性。表结构（Schema）通过主键、类型、`NULL / NOT NULL` 与 `DEFAULT` 确立了数据的身份基准与合法性底线。

MySQL Server 负责连接管理、SQL 解析验证、执行计划选择与流程调度；InnoDB 作为默认存储引擎，具体负责数据行与索引的磁盘/内存管理，并提供事务与高并发底层保障。

SQL 是声明式操作语言。通过 `INSERT / SELECT / UPDATE / DELETE` 表达 CRUD 需求；利用 `WHERE` 精确圈定行范围，`ORDER BY` 确立确定性顺序，`LIMIT` 控制交付条数。在应用交互层面，始终通过参数绑定隔离语法与数据值，是保障数据库安全运行的第一道红线。

<details>
<summary><strong>🗺️ 回看本章完整知识图</strong></summary>

```text
业务数据怎样进入 MySQL？
│
├── 1. 关系型数据库到底在管理什么？
│   ├── Database / DBMS / MySQL
│   └── Table / Row / Column
│
├── 2. 一张表怎样规定身份和基本规则？
│   ├── 一行代表什么
│   ├── Column / Data Type
│   ├── Primary Key
│   ├── NULL / NOT NULL
│   └── DEFAULT
│
├── 3. MySQL Server 和 InnoDB 分别负责什么？
│   ├── Client
│   ├── MySQL Server
│   └── Storage Engine
│       └── InnoDB 是其中一种实现
│
└── 4. 单表数据怎样用 SQL 增删改查？
    ├── INSERT
    ├── SELECT
    │   ├── WHERE / AND / OR / IN / LIKE / IS NULL
    │   ├── ORDER BY
    │   └── LIMIT
    ├── UPDATE
    ├── DELETE
    └── 参数绑定
```

</details>

---

## 🎯 面试怎么回答

### Database、DBMS 和 MySQL 是什么关系？

> [!TIP]
> Database 是被组织和管理的数据集合；DBMS 是管理这些数据的系统软件；MySQL 是一种具体的关系型 DBMS 实现。日常交流中说“用 MySQL 数据库”是口语简称，但在原理层面，MySQL 是软件系统，数据库是其管理的数据集合。

### 关系型数据库里的 Table、Row、Column 分别是什么？

> [!TIP]
> Table 用来组织同一类业务事实的集合；Row 代表一条具体的数据记录；Column 定义该类记录共同具备的属性特征。表结构（Schema）规定行的属性框架与约束规则，数据行则为框架填入具体事实。

### 什么是主键？

> [!TIP]
> 主键是一列或一组列，用来唯一标识表中的某一条记录。主键值具备非空且唯一的强制约束。主键最首要的职责是赋予记录稳定的对象身份，而非单纯为了查询加速。

### `NULL` 和空字符串有什么区别？

> [!TIP]
> `NULL` 表示值缺失或未知状态，参与普通比较（如 `= NULL`）遵循三值逻辑，无法得到真假判断，必须使用 `IS NULL / IS NOT NULL`；空字符串 `''` 是一个已经确定的具体字符串对象，其长度为 0。

### MySQL Server 和 InnoDB 是什么关系？

> [!TIP]
> MySQL Server 处于上层，负责 SQL 连接、解析语义、优化器选型和执行器调度；InnoDB 是下层的可插拔存储引擎，负责具体表数据和索引的物理存取，并提供事务、行锁和崩溃恢复等底层能力。

### SQL 为什么叫声明式语言？

> [!TIP]
> SQL 只声明“期望得到什么数据、修改哪些数据”，而不由开发者编写底层的寻道遍历循环。具体的物理访问路径（全表扫描还是走索引）由数据库优化器根据成本模型自主决策。

### 为什么程序里应该使用参数绑定？

> [!TIP]
> 参数绑定将 SQL 语法骨架与业务数据输入彻底分离。SQL 结构先经过语法解析，用户输入仅作为字面数据传入，能从根本上杜绝 SQL 注入风险。注意占位符只能代指数据值，表名和列名等动态语法标识必须通过后端代码白名单控制。

---

## ⚠️ 易错点

> [!WARNING]
> **MySQL 不是数据文件本身。** MySQL 是 DBMS 软件系统，Database 是其组织管理的数据集合。

> [!WARNING]
> **主键首先解决记录身份。** 不要把“为了查询更快”当成主键的核心定义。

> [!WARNING]
> **`NULL` 不是 0 或空字符串。** 判断未知值必须使用 `IS NULL / IS NOT NULL`，`= NULL` 永远无法达成预期。

> [!WARNING]
> **`DEFAULT` 仅处理缺省值填充。** 它不负责合法性取值校验。

> [!WARNING]
> **没有 `ORDER BY` 时，绝对不要信任查询返回的物理顺序。** 若排序列值可能重复且需要确定性结果，应追加唯一排序列（如 `id`）。

> [!WARNING]
> **`UPDATE / DELETE` 缺少 `WHERE` 会修改全表。** 变更前用同条件 `SELECT` 预览是必备习惯。

> [!WARNING]
> **参数占位符只能替代数据值。** 不能在表名、列名或 SQL 关键字上使用占位符。

---

## 🧩 本章自测

<details>
<summary><strong>1. MySQL 和 Database 是同一个概念吗？</strong></summary>

不是。MySQL 是数据库管理系统（DBMS），Database 是被组织和管理的数据集合。

</details>

<details>
<summary><strong>2. 一张 tasks 表中，Table、Row、Column 分别对应什么？</strong></summary>

`tasks` 是 Table；某一条具体任务记录是 Row；`id / title / status` 等属性是 Column。

</details>

<details>
<summary><strong>3. 为什么不能直接用 title 当作每条任务的稳定身份？</strong></summary>

因为标题可能重复，也可能在业务中被修改。记录的长期引用需要稳定且唯一的主键标识。

</details>

<details>
<summary><strong>4. `NULL`、`0`、空字符串有什么区别？</strong></summary>

`NULL` 表示当前缺少已知值；`0` 是已知的整数；空字符串是已知的长度为 0 的文本。

</details>

<details>
<summary><strong>5. `DEFAULT 'pending'` 能保证 status 只能填写 pending 吗？</strong></summary>

不能。DEFAULT 仅在插入操作省略该列时触发缺省填充，无法约束显式写入的其他非法字符串。

</details>

<details>
<summary><strong>6. DataGrip、DBeaver 是 MySQL Server 吗？</strong></summary>

不是。它们是客户端工具，负责连接 Server、收发网络包与渲染结果集。

</details>

<details>
<summary><strong>7. 为什么 InnoDB 和 MySQL Server 不能当成同一个东西？</strong></summary>

Server 负责通用层的解析、优化和执行调度；InnoDB 是负责具体数据页/索引管理、事务与行锁的存储引擎实现。

</details>

<details>
<summary><strong>8. 只写 `LIMIT 1` 能稳定表示“最新一条”吗？</strong></summary>

不能。`LIMIT 1` 仅截断最终返回一条，若无 `ORDER BY` 明确定义排序规则，返回内容是不确定的。

</details>

<details>
<summary><strong>9. `UPDATE tasks SET status='done';` 会发生什么？</strong></summary>

由于缺少 `WHERE` 子句限定范围，整张表的所有记录都会被批量更新为 `done`。

</details>

<details>
<summary><strong>10. 为什么程序不能直接把用户输入拼进 SQL？</strong></summary>

直接拼接会导致用户输入改变 SQL 结构，引发 SQL 注入漏洞。应使用参数绑定确保输入始终作为数据字面量解析。

</details>

---

## 📌 本章最终要留下的六句话

1. **关系型数据库把同一类业务事实按照明确的表结构组织起来。**
2. **Table 表示一类记录，Row 是一条具体记录，Column 定义记录的属性。**
3. **表结构不仅规定列和类型，还用 Primary Key、NULL / NOT NULL、DEFAULT 等规则约束数据。**
4. **MySQL 是 DBMS；MySQL Server 负责理解和组织 SQL 执行，InnoDB 是负责具体表数据和索引访问的默认存储引擎。**
5. **SQL 描述“要什么数据、要怎样修改”；`WHERE` 控制范围，`ORDER BY` 定义顺序，`LIMIT` 控制结果数量。**
6. **程序中的外部业务值使用参数绑定；动态表名、列名等 SQL 结构应由程序白名单控制。**

## 📚 权威资料

- [MySQL 9.7：Creating and Using a Database](https://dev.mysql.com/doc/refman/9.7/en/database-use.html)
- [MySQL 9.7：Retrieving Information from a Table](https://dev.mysql.com/doc/refman/9.7/en/retrieving-data.html)
- [MySQL 9.7：Working with NULL Values](https://dev.mysql.com/doc/refman/9.7/en/working-with-null.html)
- [MySQL 9.7：CREATE TABLE Statement](https://dev.mysql.com/doc/refman/9.7/en/create-table.html)
- [MySQL 9.7：Storage Engines](https://dev.mysql.com/doc/refman/9.7/en/storage-engines.html)
- [MySQL 9.7：Introduction to InnoDB](https://dev.mysql.com/doc/refman/9.7/en/innodb-introduction.html)
- [MySQL 9.7：PREPARE Statement](https://dev.mysql.com/doc/refman/9.7/en/prepare.html)
