// ==================================================
// 股票价格监控配置 - 请根据您的需求修改以下参数
// ==================================================

// 价格阈值配置 - 这里是您需要经常修改的参数
const PRICE_THRESHOLDS = {
  EMAIL_ALERT: 100,    // A金额：超过此价格时发送邮件通知
  VOICE_CALL: 150,     // B金额：超过此价格时进行语音外呼通知
};

// ==================================================
// 系统配置 - 初次配置后一般不需要频繁修改
// ==================================================

// 全局配置变量
const CONFIG = {
  // 股票相关配置
  STOCK: {
    SYMBOL: "SJ", // 股票代码：Scienjoy
    API_KEY: "YOUR_ALPHA_VANTAGE_API_KEY", // 替换为您的 Alpha Vantage API Key
    PRICE_CHECK_INTERVAL: 5, // 检查间隔（分钟）
  },
  
  // 邮件通知配置
  EMAIL: {
    SENDER: "hooufeng@gmail.com", // 发送邮箱
    RECEIVER: "houfeng@foxmail.com", // 接收邮箱
  },
  
  // 阿里云语音外呼配置
  ALIYUN: {
    ACCESS_KEY_ID: "YOUR_ALIYUN_ACCESS_KEY_ID", // 替换为您的阿里云 AccessKey ID
    ACCESS_KEY_SECRET: "YOUR_ALIYUN_ACCESS_KEY_SECRET", // 替换为您的阿里云 AccessKey Secret
    PHONE_NUMBER: "YOUR_PHONE_NUMBER", // 替换为您的手机号
    TTS_CODE: "YOUR_TTS_CODE", // 替换为您的阿里云语音模板 ID
  },
};

/**
 * 主函数：查询股票价格并根据阈值触发通知
 */
function checkStockPriceAndNotify() {
  console.log("=== 开始检查股票价格 ===");
  console.log(`邮件通知阈值: ${PRICE_THRESHOLDS.EMAIL_ALERT}`);
  console.log(`语音外呼阈值: ${PRICE_THRESHOLDS.VOICE_CALL}`);
  
  const stockPrice = getStockPrice(CONFIG.STOCK.SYMBOL, CONFIG.STOCK.API_KEY);
  if (stockPrice === null) {
    Logger.log("无法获取股票价格");
    return;
  }

  Logger.log(`当前股票价格: $${stockPrice}`);

  // 检查是否超过邮件通知阈值
  if (stockPrice > PRICE_THRESHOLDS.EMAIL_ALERT) {
    Logger.log(`价格 $${stockPrice} 超过邮件通知阈值 $${PRICE_THRESHOLDS.EMAIL_ALERT}，发送邮件通知`);
    sendEmailNotification(stockPrice);
  }

  // 检查是否超过语音外呼通知阈值
  if (stockPrice > PRICE_THRESHOLDS.VOICE_CALL) {
    Logger.log(`价格 $${stockPrice} 超过语音外呼阈值 $${PRICE_THRESHOLDS.VOICE_CALL}，发起语音外呼`);
    makeVoiceCallNotification(stockPrice);
  }
  
  Logger.log("=== 检查完成 ===");
}

/**
 * 获取股票价格
 * @param {string} symbol - 股票代码
 * @param {string} apiKey - Alpha Vantage API Key
 * @returns {number|null} - 股票价格（失败时返回 null）
 */
function getStockPrice(symbol, apiKey) {
  const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${apiKey}`;
  try {
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    
    // 检查 API 响应是否有效
    if (data["Global Quote"] && data["Global Quote"]["05. price"]) {
      return parseFloat(data["Global Quote"]["05. price"]);
    } else {
      Logger.log("API 响应格式错误或无效");
      Logger.log(JSON.stringify(data));
      return null;
    }
  } catch (error) {
    Logger.log(`获取股票价格失败: ${error}`);
    return null;
  }
}

/**
 * 发送邮件通知
 * @param {number} price - 当前股票价格
 */
function sendEmailNotification(price) {
  try {
    const subject = `🚨 股票价格警报: ${CONFIG.STOCK.SYMBOL}`;
    const body = `
您好！

Scienjoy (${CONFIG.STOCK.SYMBOL}) 的股票价格已经达到警报阈值！

📈 当前价格: $${price}
🎯 设定阈值: $${PRICE_THRESHOLDS.EMAIL_ALERT}
⏰ 时间: ${new Date().toLocaleString()}

请及时关注市场动态。

此邮件由股票监控系统自动发送。
    `;
    
    GmailApp.sendEmail(CONFIG.EMAIL.RECEIVER, subject, body, {
      from: CONFIG.EMAIL.SENDER,
    });
    Logger.log("✅ 邮件通知已发送成功");
  } catch (error) {
    Logger.log(`❌ 邮件发送失败: ${error}`);
  }
}

/**
 * 通过阿里云语音外呼 API 发送通知
 * @param {number} price - 当前股票价格
 */
function makeVoiceCallNotification(price) {
  try {
    const timestamp = new Date().toISOString();
    const nonce = Math.random().toString(36).substring(2, 15);
    
    const params = {
      Action: "SingleCallByTts",
      CalledNumber: CONFIG.ALIYUN.PHONE_NUMBER,
      TtsCode: CONFIG.ALIYUN.TTS_CODE,
      TtsParam: JSON.stringify({ 
        price: price, 
        threshold: PRICE_THRESHOLDS.VOICE_CALL,
        stock: CONFIG.STOCK.SYMBOL 
      }),
      AccessKeyId: CONFIG.ALIYUN.ACCESS_KEY_ID,
      Format: "JSON",
      SignatureMethod: "HMAC-SHA1",
      SignatureNonce: nonce,
      SignatureVersion: "1.0",
      Timestamp: timestamp,
      Version: "2017-05-25",
    };

    // 生成签名
    const signature = generateAliyunSignature(params, CONFIG.ALIYUN.ACCESS_KEY_SECRET);
    params.Signature = signature;

    const url = "https://dyvmsapi.aliyuncs.com";
    const response = UrlFetchApp.fetch(url, {
      method: "POST",
      payload: params,
    });
    
    const result = JSON.parse(response.getContentText());
    if (result.Code === "OK") {
      Logger.log("✅ 语音外呼通知已触发成功");
    } else {
      Logger.log(`❌ 语音外呼失败: ${result.Message}`);
    }
  } catch (error) {
    Logger.log(`❌ 语音外呼通知失败: ${error}`);
  }
}

/**
 * 生成阿里云 API 签名
 * @param {object} params - 请求参数
 * @param {string} accessKeySecret - 阿里云 AccessKey Secret
 * @returns {string} - 签名
 */
function generateAliyunSignature(params, accessKeySecret) {
  // 排序参数并构建查询字符串
  const sortedParams = Object.keys(params)
    .sort()
    .map((key) => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join("&");
  
  // 构建待签名字符串
  const stringToSign = `POST&${encodeURIComponent("/")}&${encodeURIComponent(sortedParams)}`;
  
  // 计算签名
  const signature = Utilities.computeHmacSha1Signature(stringToSign, accessKeySecret + "&");
  return Utilities.base64Encode(signature);
}

/**
 * 测试函数：用于验证配置是否正确
 */
function testConfiguration() {
  Logger.log("=== 配置测试 ===");
  Logger.log(`股票代码: ${CONFIG.STOCK.SYMBOL}`);
  Logger.log(`邮件通知阈值: $${PRICE_THRESHOLDS.EMAIL_ALERT}`);
  Logger.log(`语音外呼阈值: $${PRICE_THRESHOLDS.VOICE_CALL}`);
  Logger.log(`发送邮箱: ${CONFIG.EMAIL.SENDER}`);
  Logger.log(`接收邮箱: ${CONFIG.EMAIL.RECEIVER}`);
  Logger.log(`手机号: ${CONFIG.ALIYUN.PHONE_NUMBER}`);
  
  // 测试获取股票价格
  const price = getStockPrice(CONFIG.STOCK.SYMBOL, CONFIG.STOCK.API_KEY);
  if (price !== null) {
    Logger.log(`✅ 成功获取股票价格: $${price}`);
  } else {
    Logger.log("❌ 获取股票价格失败，请检查 API Key 配置");
  }
} 