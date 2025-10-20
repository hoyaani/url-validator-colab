# URL 檢查器 (URL Validator) - Google Colab 版本

<div align="center">

**一個功能完整的 URL 檢驗工具，支援多格式檔案上傳、批量檢測、詳細報告導出**

![Python Version](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-orange)
![Platform](https://img.shields.io/badge/Platform-Google%20Colab-brightgreen)

[快速開始](#快速開始) • [功能特性](#功能特性) • [使用說明](#使用說明) • [API 文檔](#api-文檔) • [常見問題](#常見問題)

</div>

---

## 目錄

- [功能特性](#功能特性)
- [系統需求](#系統需求)
- [快速開始](#快速開始)
  - [方式一：Colab 一鍵安裝](#方式一colab-一鍵安裝)
  - [方式二：本地 Python 環境](#方式二本地-python-環境)
- [使用說明](#使用說明)
  - [基礎使用](#基礎使用)
  - [進階用法](#進階用法)
- [輸入檔案格式](#輸入檔案格式)
- [輸出報告格式](#輸出報告格式)
- [API 文檔](#api-文檔)
- [配置参數](#配置参數)
- [常見問題](#常見問題)
- [故障排除](#故障排除)
- [開發指南](#開發指南)
- [版本更新日誌](#版本更新日誌)
- [貢獻指南](#貢獻指南)
- [許可證](#許可證)

---

## 功能特性

### 核心功能

✅ **多格式支援**
- 支持 TXT、CSV、JSON、XML 四種檔案格式
- 自動遞迴掃描嵌套結構中的 URL

✅ **智能 URL 提取**
- 自動檢測 URL 格式（http/https/ftp）
- 支持不帶協議的域名（自動補充 http://）
- 自動去重與空值過濾

✅ **連通性檢測**
- DNS 解析檢測（可配置超時時間）
- HTTP/HTTPS 請求檢測（HEAD 方法，高效低頻寬）
- SSL 證書驗證可選（默認忽略）
- 詳細的失敗原因分類

✅ **多線程批量處理**
- 根據 Colab 資源**動態自動調整**線程數（2-10）
- 實時進度顯示
- 完全無需手動配置

✅ **雙格式報告導出**
- CSV 格式（輕量、通用、無依賴）
- Excel 格式（功能豐富、表格美觀）
- 包含 URL、狀態、失敗原因、檢測時間

✅ **Google Colab 原生支持**
- 原生檔案上傳界面
- 表格實時顯示
- 無需配置代理或 VPN

---

## 系統需求

### 環境要求

| 項目 | 要求 |
|------|------|
| **Python 版本** | 3.9+ |
| **運行環境** | Google Colab 或本地 Python 3.9+ |
| **網絡連接** | 需要（用於 DNS 解析與 HTTP 請求） |
| **存儲空間** | 最少 100 MB（含依賴） |

### 依賴套件

```
requests >= 2.28.0      # HTTP 請求
pandas >= 1.3.0         # 數據處理與表格
psutil >= 5.9.0         # 系統資源檢測
openpyxl >= 3.8.0       # Excel 導出（可選）
```

---

## 快速開始

### 方式一：Colab 一鍵安裝

#### 步驟 1：打開 Google Colab

訪問 [Google Colab](https://colab.research.google.com)，創建新筆記本或打開現有筆記本。

#### 步驟 2：執行安裝指令

在第一個 Cell 中複製以下代碼並執行：

```python
# ========== 安裝依賴 & 克隆倉庫 ==========
import subprocess
import sys
import os

print("[1/3] 安裝依賴套件...\n")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
                       "requests pandas psutil openpyxl"])

print("[2/3] 克隆 GitHub 倉庫...\n")
!git clone https://github.com/hoyaani/url-validator-colab.git

print("[3/3] 環境準備完成！\n")
os.chdir("url-validator-colab")
```

**預計耗時：** 30-45 秒

#### 步驟 3：運行檢查器

在第二個 Cell 中複製以下代碼並執行：

```python
# ========== 執行 URL 檢查器 ==========
from main import URLValidatorColab
import pandas as pd

# 初始化檢查器
validator = URLValidatorColab()

# 上傳檔案（自動彈出選擇框）
filepath = validator.upload_file_from_colab()

if filepath:
    # 解析檔案
    urls = validator.parse_url_file(filepath)
    
    if urls:
        # 批量檢測
        results_df = validator.validate_urls_batch(urls)
        
        # 顯示報告
        validator.display_report(results_df)
        
        # 導出選項
        print("\n[導出選項]")
        choice = input("1=CSV / 2=Excel / 0=跳過: ").strip()
        if choice == "1":
            validator.export_report(results_df, "csv")
        elif choice == "2":
            validator.export_report(results_df, "excel")
```

#### 步驟 4：上傳檔案並查看結果

1. 執行上述代碼
2. 在彈出的「選擇檔案」對話框中選擇本地 URL 檔案（TXT/CSV/JSON/XML）
3. 等待檢測完成（進度條實時顯示）
4. 選擇導出格式（CSV 或 Excel）

---

### 方式二：本地 Python 環境

#### 前提條件

- 已安裝 Python 3.9+
- 已安裝 Git

#### 步驟 1：克隆倉庫

```bash
git clone https://github.com/hoyaani/url-validator-colab.git
cd url-validator-colab
```

#### 步驟 2：安裝依賴

使用 pip 安裝：

```bash
pip install -r requirements.txt
```

或使用 conda：

```bash
conda create -n url-validator python=3.9
conda activate url-validator
conda install --file requirements.txt
```

#### 步驟 3：修改代碼（本地版本）

由於 `upload_file_from_colab()` 只在 Colab 環境中可用，本地環境需修改 `main.py`：

**修改前（Colab 版本）：**
```python
filepath = validator.upload_file_from_colab()
```

**修改後（本地版本）：**
```python
# 直接指定本地檔案路徑
filepath = "path/to/your/urls.txt"  # 或 .csv/.json/.xml
```

#### 步驟 4：運行檢查器

```bash
python main.py
```

或在 Python 交互式環境中：

```python
from main import URLValidatorColab
import pandas as pd

validator = URLValidatorColab()
# 直接指定本地檔案
urls = validator.parse_url_file("urls.txt")
results_df = validator.validate_urls_batch(urls)
validator.display_report(results_df)
validator.export_report(results_df, "csv")
```

---

## 使用說明

### 基礎使用

#### 場景 1：Colab 中批量檢測 URL

```python
from main import URLValidatorColab

# 初始化
validator = URLValidatorColab()

# 上傳包含 URL 的檔案
filepath = validator.upload_file_from_colab()

# 解析檔案
urls = validator.parse_url_file(filepath)
print(f"成功提取 {len(urls)} 個 URL")

# 批量檢測
results_df = validator.validate_urls_batch(urls)

# 顯示結果
validator.display_report(results_df)

# 導出為 CSV
validator.export_report(results_df, "csv")
```

**輸出示例：**
```
[系統資源檢測]
  CPU 核心數: 2
  可用記憶體: 12.45 GB
  推薦線程數: 2

[檔案上傳]
支援格式：TXT（每行一個 URL）/ CSV / JSON / XML
請選擇本地檔案...

✓ 檔案上傳成功: urls.txt

[解析完成] 從檔案中提取 50 個 URL

[檢測開始] 共 50 個 URL，使用 2 個線程

進度: 1/50 (2.0%)
進度: 2/50 (4.0%)
...
進度: 50/50 (100.0%)

[檢測完成]

====================================================================================================
URL 檢測報告
檢測時間: 2024-05-20 14:30:45
總計: 50 個 | 成功: 48 個 | 失敗: 2 個
====================================================================================================
```

#### 場景 2：自定義配置參數

```python
from main import URLValidatorColab

validator = URLValidatorColab()

# 自定義超時時間和線程數
validator.config = {
    "dns_timeout": 5,      # DNS 超時 5 秒
    "http_timeout": 10,    # HTTP 超時 10 秒
    "max_workers": 4       # 使用 4 個線程
}

# 後續操作...
urls = validator.parse_url_file(filepath)
results_df = validator.validate_urls_batch(urls)
```

---

### 進階用法

#### 用法 1：過濾特定狀態的結果

```python
# 只顯示失敗的 URL
failed_urls = results_df[results_df["status"] == "失敗"]
print(failed_urls)

# 只顯示成功的 URL
success_urls = results_df[results_df["status"] == "成功"]
print(f"成功 URL 數量：{len(success_urls)}")
```

#### 用法 2：批量統計分析

```python
# 按失敗原因分組統計
failure_reasons = results_df[results_df["status"] == "失敗"]["reason"].value_counts()
print(failure_reasons)

# 輸出示例：
# DNS 解析失敗 (域名不存在或 DNS 解析失敗)                    12
# HTTP 請求超時 (HTTP 請求超時 (5s))                       5
# 格式錯誤 (格式錯誤：域名格式無效（缺少主機名）)              2
```

#### 用法 3：自定義格式導出

```python
# 導出特定列
export_df = results_df[["url", "status"]]
export_df.to_csv("important_urls.csv", index=False)

# 按狀態分別導出
results_df[results_df["status"] == "成功"].to_csv("success_urls.csv", index=False)
results_df[results_df["status"] == "失敗"].to_csv("failed_urls.csv", index=False)
```

#### 用法 4：集成到其他腳本

```python
from main import URLValidatorColab
import pandas as pd

def batch_validate_urls(file_path: str, export_format: str = "csv"):
    """
    包裝函數：驗證檔案中的 URL 並直接導出結果
    """
    validator = URLValidatorColab()
    urls = validator.parse_url_file(file_path)
    results_df = validator.validate_urls_batch(urls)
    validator.export_report(results_df, export_format)
    return results_df

# 使用
result = batch_validate_urls("urls.csv", export_format="excel")
print(result.head(10))
```

---

## 輸入檔案格式

### TXT 格式（推薦）

**檔名：** `urls.txt`

**內容格式：** 每行一個 URL

```
https://www.google.com
https://www.github.com
https://www.python.org
http://example.com
invalid-url-without-protocol.com
ftp://ftp.example.com
```

**優點：** 簡單、輕量、無依賴

---

### CSV 格式

**檔名：** `urls.csv`

**內容格式：** 標準 CSV，自動掃描所有列尋找 URL

```csv
site_name,url,category
Google,https://www.google.com,搜索引擎
GitHub,https://www.github.com,程式碼託管
Python,https://www.python.org,語言官網
```

**說明：**
- 可包含多列，工具自動掃描所有列
- 支援帶 BOM 的 UTF-8 編碼
- 自動跳過空值與非 URL 內容

---

### JSON 格式

**檔名：** `urls.json`

**內容格式：** 支援任意嵌套結構

```json
{
  "websites": [
    "https://www.google.com",
    "https://www.github.com"
  ],
  "sites": {
    "python_official": "https://www.python.org",
    "stack_overflow": "https://stackoverflow.com"
  },
  "nested": {
    "level2": {
      "resources": [
        "https://www.wikipedia.org",
        "https://www.medium.com"
      ]
    }
  }
}
```

**說明：**
- 工具遞迴掃描所有層級
- 自動提取所有字符串類型的 URL

---

### XML 格式

**檔名：** `urls.xml`

**內容格式：** 支援元素文本與屬性

```xml
<?xml version="1.0" encoding="UTF-8"?>
<websites>
  <site name="Google">
    <url>https://www.google.com</url>
  </site>
  <site name="GitHub">
    <url homepage="https://www.github.com">GitHub Repository</url>
  </site>
  <resources>
    <link href="https://www.python.org">Python Official</link>
  </resources>
</websites>
```

**說明：**
- 掃描所有元素的文本內容
- 掃描所有屬性值
- 遞迴處理嵌套結構

---

## 輸出報告格式

### 控制台顯示格式

```
====================================================================================================
URL 檢測報告
檢測時間: 2024-05-20 14:30:45
總計: 50 個 | 成功: 48 個 | 失敗: 2 個
====================================================================================================

| URL | 狀態 | 原因 | 檢測時間 |
|-----|------|------|---------|
| https://www.google.com | 成功 | HTTP 200 (正常響應) | 2024-05-20 14:30:45 |
| https://invalid-url.xyz | 失敗 | DNS 解析失敗（域名不存在） | 2024-05-20 14:30:46 |
```

### CSV 匯出格式

**檔名：** `url_validation_report_20240520_143045.csv`

```csv
url,status,reason,check_time
https://www.google.com,成功,HTTP 200 (正常響應),2024-05-20 14:30:45
https://www.github.com,成功,HTTP 200 (正常響應),2024-05-20 14:30:46
https://invalid-domain-xyz.com,失敗,DNS 解析失敗（域名不存在）,2024-05-20 14:30:47
```

**特點：**
- UTF-8 編碼（含 BOM）
- 易於用 Excel 打開
- 輕量級，適合大數據量

---

### Excel 匯出格式

**檔名：** `url_validation_report_20240520_143045.xlsx`

| URL | 狀態 | 原因 | 檢測時間 |
|-----|------|------|---------|
| https://www.google.com | 成功 | HTTP 200 (正常響應) | 2024-05-20 14:30:45 |
| https://www.github.com | 成功 | HTTP 200 (正常響應) | 2024-05-20 14:30:46 |

**特點：**
- 表格格式美觀
- 支援排序與篩選
- 支援圖表與分析

---

## API 文檔

### 類：URLValidatorColab

#### 初始化

```python
validator = URLValidatorColab()
```

**功能：** 初始化 URL 檢查器，自動檢測系統資源並設定最優線程數

**參數：** 無

**返回值：** URLValidatorColab 實例

**示例：**
```python
validator = URLValidatorColab()
# 輸出：
# [系統資源檢測]
#   CPU 核心數: 4
#   可用記憶體: 16.50 GB
#   推薦線程數: 3
```

---

#### 方法：upload_file_from_colab()

```python
filepath = validator.upload_file_from_colab() -> Optional[str]
```

**功能：** 在 Google Colab 中彈出檔案選擇框，上傳 URL 檔案

**參數：** 無

**返回值：** 
- 字符串：上傳檔案的路徑（如 `/tmp/urls.txt`）
- None：用戶取消上傳或上傳失敗

**支援格式：** TXT、CSV、JSON、XML

**異常處理：** 自動捕獲 ImportError（非 Colab 環境）與文件操作異常

**示例：**
```python
filepath = validator.upload_file_from_colab()
if filepath:
    print(f"檔案已上傳: {filepath}")
else:
    print("未選擇檔案")
```

---

#### 方法：parse_url_file(filepath)

```python
urls = validator.parse_url_file(filepath: str) -> List[str]
```

**功能：** 解析檔案並提取 URL 列表

**參數：**
- `filepath` (str)：檔案路徑（支援 TXT/CSV/JSON/XML）

**返回值：** URL 列表（已去重、過濾空值）

**內部邏輯：**
1. 檢測檔案擴展名
2. 根據格式呼叫對應解析器
3. 自動去重與清理

**異常處理：** 返回空列表，控制台輸出錯誤訊息

**示例：**
```python
urls = validator.parse_url_file("urls.csv")
print(f"提取 {len(urls)} 個 URL")
# 輸出: 提取 42 個 URL
```

---

#### 方法：validate_urls_batch(urls)

```python
results_df = validator.validate_urls_batch(urls: List[str]) -> pd.DataFrame
```

**功能：** 批量驗證 URL（多線程）

**參數：**
- `urls` (List[str])：URL 列表

**返回值：** Pandas DataFrame，包含列：
- `url` (str)：URL 地址
- `status` (str)：檢測狀態（"成功" 或 "失敗"）
- `reason` (str)：結果說明或失敗原因
- `check_time` (str)：檢測時間戳（格式：YYYY-MM-DD HH:MM:SS）

**線程數調整：**
- 自動根據系統資源計算
- 可手動修改：`validator.config["max_workers"] = 4`

**實時進度：** 控制台輸出進度（如 `進度: 10/50 (20.0%)` ）

**示例：**
```python
urls = ["https://www.google.com", "https://www.github.com"]
results_df = validator.validate_urls_batch(urls)
print(results_df)
```

**輸出示例：**
```
                          url status                 reason        check_time
0  https://www.google.com   成功  HTTP 200 (正常響應)  2024-05-20 14:30:45
1  https://www.github.com   成功  HTTP 200 (正常響應)  2024-05-20 14:30:46
```

---

#### 方法：display_report(df)

```python
validator.display_report(df: pd.DataFrame) -> None
```

**功能：** 在 Colab 中漂亮地顯示檢測報告表格

**參數：**
- `df` (pd.DataFrame)：驗證結果 DataFrame

**返回值：** 無（直接輸出到 Colab 單元格）

**顯示內容：**
- 統計摘要（總計、成功、失敗數量）
- HTML 格式表格（可排序、可篩選）

**示例：**
```python
results_df = validator.validate_urls_batch(urls)
validator.display_report(results_df)
```

---

#### 方法：export_report(df, export_format)

```python
filepath = validator.export_report(df: pd.DataFrame, export_format: str = "csv") -> Optional[str]
```

**功能：** 導出檢測報告為 CSV 或 Excel

**參數：**
- `df` (pd.DataFrame)：驗證結果 DataFrame
- `export_format` (str)：導出格式，可選值：
  - `"csv"`（默認）：輕量格式
  - `"excel"`：Excel 格式（需 openpyxl）

**返回值：** 
- 字符串：導出檔案路徑
- None：導出失敗

**檔名格式：** `url_validation_report_YYYYMMDD_HHMMSS.{csv|xlsx}`

**自動降級：** 若 openpyxl 未安裝，Excel 格式會自動降級為 CSV

**示例：**
```python
# 導出為 CSV
csv_path = validator.export_report(results_df, "csv")
print(f"✓ 報告已導出: {csv_path}")

# 導出為 Excel
xlsx_path = validator.export_report(results_df, "excel")
print(f"✓ Excel 報告已導出: {xlsx_path}")
```

---

## 配置参數

### 可自定義參數

```python
validator.config = {
    "dns_timeout": 3,      # DNS 解析超時時間（秒）
    "http_timeout": 5,     # HTTP 請求超時時間（秒）
    "max_workers": 5       # 並發線程數
}
```

### 參數說明

| 參數 | 默認值 | 範圍 | 說明 |
|------|--------|------|------|
| `dns_timeout` | 3 秒 | 1-10 | DNS 解析等待時間，過短會導致誤判，過長會增加檢測耗時 |
| `http_timeout` | 5 秒 | 2-15 | HTTP 請求等待時間 |
| `max_workers` | 自動計算 | 2-10 | 並發線程數，更多線程速度快但會占用更多資源 |

### 調整建議

**場景 1：網絡不穩定**
```python
validator.config = {
    "dns_timeout": 5,      # 增加 DNS 超時
    "http_timeout": 8,     # 增加 HTTP 超時
    "max_workers": 3       # 減少並發
}
```

**場景 2：快速掃描（網絡良好）**
```python
validator.config = {
    "dns_timeout": 2,
    "http_timeout": 3,
    "max_workers": 8       # 增加並發
}
```

**場景 3：目標伺服器敏感（防止被 IP 封禁）**
```python
validator.config = {
    "dns_timeout": 3,
    "http_timeout": 5,
    "max_workers": 2       # 最小化並發，減少 QPS
}
```

---

## 常見問題

### Q1：為什麼有些 URL 顯示「DNS 解析失敗」？

**A：** 這通常表示域名不存在或 DNS 服務器無法解析。常見原因：
- 域名拼寫錯誤
- 域名已過期
- 企業內網域名（無公開 DNS 記錄）
- 網絡連接問題

**驗證方法：** 在終端執行 `nslookup example.com` 或 `ping example.com`

---

### Q2：為什麼有些 URL 顯示「HTTP 請求超時」？

**A：** 伺服器響應慢或網絡連接問題。解決方案：
1. 增加超時時間：
   ```python
   validator.config["http_timeout"] = 10
   ```
2. 檢查網絡連接
3. 檢查伺服器是否在線

---

### Q3：Colab 中能否直接導出檔案到本地？

**A：** 可以。Colab 提供原生下載功能：

```python
from google.colab import files

# 導出 CSV
validator.export_report(results_df, "csv")
files.download("url_validation_report_20240520_143045.csv")

# 或導出 Excel
validator.export_report(results_df, "excel")
files.download("url_validation_report_20240520_143045.xlsx")
```

---

### Q4：能否檢測動態網站（如需 JavaScript 渲染的頁面）？

**A：** 當前版本不支持。工具使用簡單的 HEAD 請求，不執行 JavaScript。

若需檢測動態網站，建議使用 Selenium 或 Playwright 等瀏覽器自動化框架。

---

### Q5：如何處理需要認證的 URL（如私有 API）？

**A：** 當前版本不支持認證。可修改源碼添加：

```python
# 修改 _check_url_connectivity 方法
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = requests.head(url, headers=headers, ...)
```

---

### Q6：檢測後是否會影響目標伺服器？

**A：** 影響極小：
- 使用 HEAD 方法而非 GET（不下載完整內容）
- 默認線程數為 2-5（避免 DoS）
- 每個 URL 只發送一次請求

**注意：** 大規模掃描可能被視為 DoS 攻擊。若掃描他人網站，應先獲得授權。

---

### Q7：為什麼 Excel 導出失敗？

**A：** 可能原因與解決方案：

| 原因 | 解決方案 |
|------|----------|
| openpyxl 未安裝 | `pip install openpyxl` |
| 檔案被佔用 | 關閉已打開的 Excel 檔案 |
| 磁盤空間不足 | 清理磁盤空間 |
| 特殊字符在 URL 中 | 自動使用 CSV 備選方案 |

---

## 故障排除

### 問題 1：`ImportError: No module named 'google.colab'`

**原因：** 在非 Colab 環境中調用 Colab 專用函數

**解決方案：** 本地環境使用修改版代碼，直接指定檔案路徑

```python
# 本地版本改法
filepath = "urls.txt"  # 替換為您的檔案路徑
urls = validator.parse_url_file(filepath)
```

---

### 問題 2：`SSL: CERTIFICATE_VERIFY_FAILED`

**原因：** HTTPS 伺服器的 SSL 證書驗證失敗

**解決方案：** 代碼已默認設置 `verify=False`，通常不會出現此錯誤。若出現，表示網絡配置問題。

```python
# 若要強制驗證證書
validator.config["verify_ssl"] = True
```

---

### 問題 3：`Timeout` 錯誤（DNS 或 HTTP）

**原因：** 伺服器響應慢或網絡不穩定

**解決方案：**

```python
# 增加超時時間
validator.config = {
    "dns_timeout": 5,      # 從 3 秒增加到 5 秒
    "http_timeout": 10,    # 從 5 秒增加到 10 秒
    "max_workers": 2       # 減少線程，避免網絡擁塞
}

# 重新執行檢測
results_df = validator.validate_urls_batch(urls)
```

---

### 問題 4：Colab 記憶體不足（`MemoryError`）

**原因：** URL 數量過多或系統資源不足

**解決方案：**

```python
# 方案 1：減少線程數（優先）
validator.config["max_workers"] = 2

# 方案 2：分批處理
batch_size = 100
for i in range(0, len(urls), batch_size):
    batch_urls = urls[i:i+batch_size]
    results = validator.validate_urls_batch(batch_urls)
    validator.export_report(results, "csv")
    print(f"已處理 {i+batch_size}/{len(urls)} 個 URL")

# 方案 3：檢查記憶體使用
import psutil
memory_usage = psutil.virtual_memory().percent
print(f"當前記憶體使用率：{memory_usage}%")
```

---

### 問題 5：導出檔案路徑找不到

**原因：** Colab 環境中檔案保存在 `/tmp` 目錄，會話結束後自動刪除

**解決方案：** 使用 Colab 原生下載功能

```python
from google.colab import files

# 導出並立即下載
validator.export_report(results_df, "csv")
files.download("url_validation_report_20240520_143045.csv")
```

---

### 問題 6：某些 CSV 檔案無法正確解析

**原因：** 編碼格式不匹配或分隔符錯誤

**解決方案：**

```python
# 方案 1：轉換為標準 UTF-8 CSV（使用 Excel 或文本編輯器）
# 方案 2：手動指定編碼
import pandas as pd
df = pd.read_csv("urls.csv", encoding="gbk")  # 中文編碼
urls = df.iloc[:, 0].tolist()  # 提取第一列
```

---

### 問題 7：`requests.exceptions.ProxyError`

**原因：** 網絡配置中存在代理設置

**解決方案：**

```python
# 禁用代理
import os
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# 或在 requests 中手動設置
session = requests.Session()
session.trust_env = False  # 忽略環境代理設置
```

---

## 開發指南

### 項目結構

```
url-validator-colab/
├── main.py                 # 核心代碼（URLValidatorColab 類）
├── requirements.txt        # 依賴清單
├── setup.py               # 安裝配置
├── README.md              # 本文檔
├── .gitignore             # Git 忽略規則
├── tests/                 # 測試檔案（可選）
│   ├── test_urls.txt
│   ├── test_urls.csv
│   ├── test_urls.json
│   └── test_urls.xml
└── examples/              # 使用示例（可選）
    └── colab_example.ipynb
```

---

### 本地開發設置

#### 1. 克隆倉庫

```bash
git clone https://github.com/hoyaani/url-validator-colab.git
cd url-validator-colab
```

#### 2. 創建虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

#### 3. 安裝依賴（含開發工具）

```bash
pip install -r requirements.txt
pip install pytest black flake8  # 可選：測試和代碼格式化
```

#### 4. 運行測試

```bash
pytest tests/  # 需要 pytest 已安裝
```

---

### 擴展開發

#### 添加新的檔案格式支持

例如，添加 YAML 格式支持：

```python
# 在 main.py 中修改 parse_url_file 方法

import yaml

def parse_url_file(self, filepath: str) -> List[str]:
    file_ext = os.path.splitext(filepath)[1].lower()
    
    # ... 現有代碼 ...
    
    elif file_ext == ".yaml" or file_ext == ".yml":
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        urls = self._extract_urls_from_yaml(data)
    
    return urls

def _extract_urls_from_yaml(self, obj) -> List[str]:
    # 類似 JSON 的遞迴提取邏輯
    urls = []
    if isinstance(obj, dict):
        for value in obj.values():
            if isinstance(value, str) and self._is_url_like(value):
                urls.append(value)
            elif isinstance(value, (dict, list)):
                urls.extend(self._extract_urls_from_yaml(value))
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, str) and self._is_url_like(item):
                urls.append(item)
            elif isinstance(item, (dict, list)):
                urls.extend(self._extract_urls_from_yaml(item))
    return urls
```

#### 添加自定義檢測規則

```python
def validate_urls_batch_custom(self, urls: List[str], rules: Dict) -> pd.DataFrame:
    """
    自定義驗證規則
    
    Args:
        urls: URL 列表
        rules: 規則字典，例如：
            {
                "check_dns": True,
                "check_http": True,
                "allowed_domains": ["google.com", "github.com"],
                "blocked_domains": ["malicious.com"]
            }
    """
    self.results.clear()
    
    for url in urls:
        # 檢查允許列表
        if rules.get("allowed_domains"):
            domain = urlparse(url).netloc
            if not any(domain.endswith(allowed) for allowed in rules["allowed_domains"]):
                self.results.append({
                    "url": url,
                    "status": "跳過",
                    "reason": "域名不在允許列表中",
                    "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                continue
        
        # 檢查黑名單
        if rules.get("blocked_domains"):
            domain = urlparse(url).netloc
            if any(domain.endswith(blocked) for blocked in rules["blocked_domains"]):
                self.results.append({
                    "url": url,
                    "status": "失敗",
                    "reason": "域名在黑名單中",
                    "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                continue
        
        # 執行標準檢測
        result = self._check_single_url(url)
        self.results.append(result)
    
    return pd.DataFrame(self.results)
```

---

### 代碼風格規範

本項目遵循 PEP 8 標準：

```bash
# 檢查代碼風格
flake8 main.py

# 自動格式化代碼
black main.py
```

---

### 提交 Pull Request 檢查清單

在提交 PR 前，請確保：

- [ ] 代碼遵循 PEP 8 規範（`flake8 main.py` 無錯誤）
- [ ] 添加了相應的 docstring 和註釋
- [ ] 測試通過（`pytest tests/`）
- [ ] 更新了 README 中的相關文檔
- [ ] 檔案名稱清晰，提交訊息規範

---

## 版本更新日誌

### v2.0.0 (2025-10-20) [最新版本]

**新增功能**
- ✨ Google Colab 原生支持，完整的檔案上傳界面
- ✨ 支持 JSON 和 XML 格式檔案（遞迴掃描嵌套結構）
- ✨ 動態線程數調整（根據系統資源自動計算）
- ✨ 雙格式報告導出（CSV + Excel）
- ✨ 系統資源檢測與輸出

**改進**
- 🔧 優化 DNS 解析性能（使用 socket.getaddrinfo）
- 🔧 增強 URL 格式驗證邏輯
- 🔧 改進多線程錯誤處理

**修復**
- 🐛 修複 SSL 證書驗證導致的錯誤
- 🐛 修複大型檔案解析內存溢出問題
- 🐛 修複 Unicode 字符編碼問題

**文檔**
- 📚 完整的 README 和 API 文檔
- 📚 多個使用示例
- 📚 故障排除指南

---

### v1.3.0 (2025-10-20)

- 多線程優化（ThreadPoolExecutor）
- 結果導出功能（CSV）
- 超時控制改進

---

### v1.2.0 (2025-10-20)

- 新增 GUI 界面（tkinter）
- 支持文件導入（TXT/CSV）

---

### v1.1.0 (2025-10-20)

- 基礎 CLI 功能
- 單個 URL 檢測

---

## 貢獻指南

我們歡迎各種形式的貢獻！

### 貢獻方式

#### 1. 報告 Bug

在 GitHub Issues 中提交 Bug 報告，包括：
- 詳細的錯誤描述
- 復現步驟
- 系統環境（OS、Python 版本、Colab 環境等）
- 完整的錯誤堆棧跟蹤

**模板：**
```
### 問題描述
[清楚地描述問題]

### 復現步驟
1. ...
2. ...
3. ...

### 預期行為
[應該發生什麼]

### 實際行為
[實際發生了什麼]

### 系統環境
- Python 版本: 3.9.x
- OS: macOS/Linux/Windows
- 環境: Local/Colab
```

#### 2. 功能建議

在 GitHub Issues 中提交功能請求，包括：
- 清晰的功能描述
- 使用場景
- 可能的實現方式

---

#### 3. 提交代碼

1. **Fork 本倉庫**

```bash
git clone https://github.com/hoyaani/url-validator-colab.git
```

2. **創建功能分支**

```bash
git checkout -b feature/your-feature-name
```

3. **提交更改**

```bash
git add .
git commit -m "feat: 添加新功能描述"
git push origin feature/your-feature-name
```

4. **提交 Pull Request**

在 GitHub 上點擊「Compare & pull request」按鈕

---

### 代碼貢獻標準

- 遵循 PEP 8 編碼規範
- 添加完整的 docstring
- 包含測試用例（若有）
- 更新相關文檔

---

## 許可證

本項目採用 **MIT License** 開源協議。

詳見 [LICENSE](LICENSE) 檔案。

---

## 致謝

感謝以下開源項目的支持：

- [Requests](https://requests.readthedocs.io/) - HTTP 庫
- [Pandas](https://pandas.pydata.org/) - 數據處理
- [psutil](https://psutil.readthedocs.io/) - 系統監控

---

## 聯繫方式

- 📧 Email: hoyaani@hotmail.com
- 🐙 GitHub: [@hoyaani](https://github.com/hoyaani)
- 💬 Issues: [提交問題](https://github.com/hoyaani/url-validator-colab/issues)

---

## 相關資源

- [Google Colab 官方文檔](https://colab.research.google.com/)
- [Python Requests 文檔](https://requests.readthedocs.io/)
- [Pandas 官方文檔](https://pandas.pydata.org/)
- [PEP 8 編碼規範](https://www.python.org/dev/peps/pep-0008/)

---

**最後更新：** 2025-10-20

**維護者：** hoyaani

**狀態：** 被動維護中 🟢
