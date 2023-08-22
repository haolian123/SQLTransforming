# 项目介绍

SQLTransformer是一个用于将SQL字段名和数据类型在不同数据库之间进行转换的工具。支持以下数据库之间的转换：

- Hive SQL 到 Oracle SQL
- Oracle SQL 到 Hive SQL
- Hive SQL 到 PostgreSQL

## 如何使用

1. 打开SQLTransformer应用程序。
2. 在"表名"文本框中输入要创建的表的名称。
3. 在下拉框中选择要执行的转换类型，或选择 "不转化" 以保持原始 SQL 不变。
4. 在文本框中粘贴要转换的SQL字段名和数据类型。确保每个字段都单独一行，并且字段名和数据类型之间用空格分隔。
5. 单击"生成"按钮，将生成转换后的SQL语句，并将其复制到剪切板。

## 示例

以下是一个示例，演示如何在SQLTransformer中执行转换：

### 输入

```python
表名： employees
转化方式： Hive SQL to Oracle SQL

将SQL的字段名和数据类型粘贴(ctrl+v)到此处
name string
age int
salary double
```

### 输出

```python
create table employees(
    name varchar2(500),
    age int,
    salary double
)
```

## 注意事项

- 请确保输入的SQL字段名和数据类型的格式符合要求。
- 当选择转换类型时，程序会根据预定义的映射将字段数据类型进行转换。
- 如果输入的数据类型无法映射到目标数据库，程序将显示错误消息。

