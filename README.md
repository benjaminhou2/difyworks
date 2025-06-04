# 股票价格监控工具

一个基于Google Apps Script的自动化股票价格监控系统，可以实时监控纳斯达克上市公司Scienjoy (SJ)的股票价格，并在价格达到设定阈值时通过邮件和语音外呼进行通知。

## 🚀 功能特性

- **实时股票价格监控**: 使用Alpha Vantage API获取实时股票数据
- **双重通知机制**: 
  - 📧 邮件通知：价格超过阈值A时发送邮件警报
  - 📞 语音外呼：价格超过阈值B时通过阿里云语音API拨打电话
- **灵活配置**: 支持自定义价格阈值和通知参数
- **自动化部署**: 基于Google Apps Script，支持定时触发执行

## 📋 配置说明

### 价格阈值配置
```javascript
const PRICE_THRESHOLDS = {
  EMAIL_ALERT: 100,    // A金额：超过此价格时发送邮件通知
  VOICE_CALL: 150,     // B金额：超过此价格时进行语音外呼通知
};
```

### 系统配置
- **股票代码**: SJ (Scienjoy)
- **发送邮箱**: hooufeng@gmail.com
- **接收邮箱**: houfeng@foxmail.com
- **阿里云语音外呼**: 需要配置AccessKey和语音模板

## 🛠 部署步骤

### 1. 准备API密钥
- 申请 [Alpha Vantage API Key](https://www.alphavantage.co/) 用于获取股票数据
- 配置阿里云语音服务AccessKey和语音模板

### 2. 部署到Google Apps Script
1. 访问 [Google Apps Script](https://script.google.com)
2. 创建新项目
3. 复制 `stock_monitor.js` 代码到编辑器
4. 修改配置参数：
   - 替换 `YOUR_ALPHA_VANTAGE_API_KEY` 为您的API密钥
   - 替换阿里云相关配置参数
   - 根据需要调整价格阈值

### 3. 设置触发器
1. 在Google Apps Script编辑器中点击"触发器"
2. 添加新触发器：
   - 函数: `checkStockPriceAndNotify`
   - 事件源: 时间驱动器
   - 时间间隔: 建议每5-15分钟执行一次

### 4. 测试配置
运行 `testConfiguration()` 函数验证所有配置是否正确。

## 📁 项目结构

```
tools/
├── stock_monitor.js    # 主要监控脚本
├── README.md          # 项目说明文档
└── .gitignore         # Git忽略文件配置
```

## ⚠️ 注意事项

1. **API调用限制**: Alpha Vantage免费版每分钟限制5次调用，每天500次
2. **阿里云语音**: 需要先开通阿里云语音服务并创建语音模板
3. **Google Apps Script限制**: 免费版每天执行时间限制90分钟
4. **安全性**: 请妥善保管API密钥，不要在公开代码中暴露

## 🔧 自定义配置

### 修改监控阈值
只需要修改顶部的 `PRICE_THRESHOLDS` 配置：
```javascript
const PRICE_THRESHOLDS = {
  EMAIL_ALERT: 你的邮件通知价格,
  VOICE_CALL: 你的语音外呼价格,
};
```

### 修改监控股票
在 `CONFIG.STOCK.SYMBOL` 中修改股票代码。

## 📝 更新日志

- **v1.0.0**: 初始版本，支持基本的价格监控和通知功能
- **v1.1.0**: 优化配置结构，将阈值参数提取到顶部便于修改

## 📄 许可证

MIT License

## 👨‍💻 作者

开发者: benjamimhou2
GitHub: https://github.com/benjamimhou2/tools 