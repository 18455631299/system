# 车辆与司机调度系统

一个基于Flask的车辆与司机调度管理系统，使用PostgreSQL数据库存储记录。

## 功能

- 车辆与司机信息提交
- 用车记录管理和查询
- 固定备注显示
- 自定义备注添加与管理

## 技术栈

- 后端: Python + Flask
- 数据库: PostgreSQL
- 前端: HTML + Bootstrap 5 + JavaScript
- 日期选择器: Flatpickr

## 部署说明

1. 安装依赖:
```
pip install -r requirements.txt
```

2. 配置数据库:
在系统中设置环境变量`DATABASE_URL`，格式为:`postgresql://username:password@host:port/database`

3. 启动应用:
```
python main.py
```

## 系统截图

- 主界面
- 记录管理
- 备注管理

## 开发者

- 技术支持: 联系管理员