"""
URL 檢查器 - Google Colab 版本（v2.0.0）
支持多格式檔案上傳、URL過濾、連通性檢測、報告導出

版本歷史：
- v1.3.0: GUI版本（本地環境）
- v2.0.0: Colab版本（支援檔案上傳、動態多線程、報告導出）
"""

import requests
import socket
import time
import csv
import json
import xml.etree.ElementTree as ET
import pandas as pd
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from typing import List, Tuple, Dict, Optional
from datetime import datetime
import psutil
import os


class URLValidatorColab:
    """
    Google Colab 版 URL 檢查器
    
    核心功能：
    1. 支持上傳 TXT/CSV/JSON/XML 檔案
    2. 自動提取並過濾 URL
    3. 連通性檢測（DNS 解析 + HTTP 請求）
    4. 多線程並發（動態調整線程數）
    5. 報告顯示 + 導出（CSV/Excel）
    """

    def __init__(self):
        """初始化檢查器配置"""
        self.config = {
            "dns_timeout": 3,
            "http_timeout": 5,
            "max_workers": self._calculate_optimal_workers()
        }
        self.results: List[Dict[str, str]] = []
        self.url_list: List[str] = []

    def _calculate_optimal_workers(self) -> int:
        """
        根據 Colab 可用資源動態計算最優線程數
        
        Returns:
            int: 推薦線程數（2-10之間）
        """
        try:
            # 取得可用 CPU 核心數
            cpu_count = psutil.cpu_count(logical=True) or 4
            # 取得可用記憶體（GB）
            available_memory = psutil.virtual_memory().available / (1024 ** 3)
            
            # 線程數計算邏輯：
            # CPU 核心數 * 0.75（避免完全佔用），但不超過 10
            workers = min(max(int(cpu_count * 0.75), 2), 10)
            
            print(f"[系統資源檢測]")
            print(f"  CPU 核心數: {cpu_count}")
            print(f"  可用記憶體: {available_memory:.2f} GB")
            print(f"  推薦線程數: {workers}\n")
            return workers
        except Exception as e:
            print(f"[警告] 資源檢測失敗，使用默認線程數 5: {str(e)}\n")
            return 5

    def upload_file_from_colab(self) -> Optional[str]:
        """
        從 Google Colab 上傳檔案（支援 TXT/CSV/JSON/XML）
        
        Returns:
            Optional[str]: 檔案路徑，若取消上傳則返回 None
        """
        try:
            from google.colab import files
            print("[檔案上傳]")
            print("支援格式：TXT（每行一個 URL）/ CSV / JSON / XML")
            print("請選擇本地檔案...\n")
            
            uploaded = files.upload()
            if not uploaded:
                print("未選擇檔案")
                return None
            
            filename = list(uploaded.keys())[0]
            filepath = os.path.join("/tmp", filename)
            # 將上傳的檔案移至 /tmp
            with open(filepath, "wb") as f:
                f.write(uploaded[filename])
            
            print(f"✓ 檔案上傳成功: {filename}\n")
            return filepath
        except ImportError:
            print("[錯誤] 此程式碼只能在 Google Colab 中運行")
            return None
        except Exception as e:
            print(f"[上傳失敗] {str(e)}\n")
            return None

    def parse_url_file(self, filepath: str) -> List[str]:
        """
        解析檔案並提取 URL（支援 TXT/CSV/JSON/XML）
        
        Args:
            filepath: 檔案路徑
        
        Returns:
            List[str]: 提取的 URL 列表（已去重、過濾空值）
        """
        urls = []
        try:
            file_ext = os.path.splitext(filepath)[1].lower()
            
            if file_ext == ".txt":
                # TXT 格式：每行一個 URL
                with open(filepath, "r", encoding="utf-8") as f:
                    urls = [line.strip() for line in f if line.strip()]
            
            elif file_ext == ".csv":
                # CSV 格式：自動掃描所有列尋找 URL 格式內容
                df = pd.read_csv(filepath, encoding="utf-8")
                for col in df.columns:
                    for val in df[col].dropna():
                        url_str = str(val).strip()
                        if url_str and self._is_url_like(url_str):
                            urls.append(url_str)
            
            elif file_ext == ".json":
                # JSON 格式：遞迴掃描所有 value 尋找 URL
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                urls = self._extract_urls_from_json(data)
            
            elif file_ext == ".xml":
                # XML 格式：掃描所有文本節點和屬性
                tree = ET.parse(filepath)
                root = tree.getroot()
                urls = self._extract_urls_from_xml(root)
            
            else:
                print(f"[警告] 不支援的檔案格式: {file_ext}")
                return []
            
            # 去重並過濾空值
            urls = list(set([u.strip() for u in urls if u.strip()]))
            print(f"[解析完成] 從檔案中提取 {len(urls)} 個 URL\n")
            return urls
        
        except Exception as e:
            print(f"[解析失敗] {str(e)}\n")
            return []

    def _is_url_like(self, text: str) -> bool:
        """判斷字符串是否像 URL（包含協議或常見域名模式）"""
        text_lower = text.lower()
        return (
            text_lower.startswith(("http://", "https://", "ftp://")) or
            ("." in text and not text.startswith(" ") and len(text) > 5)
        )

    def _extract_urls_from_json(self, obj, urls=None) -> List[str]:
        """遞迴從 JSON 物件中提取 URL"""
        if urls is None:
            urls = []
        
        if isinstance(obj, dict):
            for value in obj.values():
                if isinstance(value, str) and self._is_url_like(value):
                    urls.append(value)
                elif isinstance(value, (dict, list)):
                    self._extract_urls_from_json(value, urls)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, str) and self._is_url_like(item):
                    urls.append(item)
                elif isinstance(item, (dict, list)):
                    self._extract_urls_from_json(item, urls)
        
        return urls

    def _extract_urls_from_xml(self, element) -> List[str]:
        """遞迴從 XML 元素中提取 URL"""
        urls = []
        
        # 掃描文本內容
        if element.text and self._is_url_like(element.text.strip()):
            urls.append(element.text.strip())
        
        # 掃描屬性
        for attr_value in element.attrib.values():
            if isinstance(attr_value, str) and self._is_url_like(attr_value):
                urls.append(attr_value)
        
        # 遞迴子元素
        for child in element:
            urls.extend(self._extract_urls_from_xml(child))
        
        return urls

    def _validate_url_format(self, url: str) -> Tuple[bool, str]:
        """
        驗證 URL 格式合法性
        
        Args:
            url: 待驗證的 URL
        
        Returns:
            Tuple[bool, str]: (是否合法, 補充協議後的URL或錯誤信息)
        """
        # 補充默認協議
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False, "域名格式無效（缺少主機名）"
            return True, url
        except Exception as e:
            return False, f"格式解析失敗：{str(e)}"

    def _check_url_connectivity(self, url: str) -> Tuple[str, str]:
        """
        檢測 URL 連通性（DNS 解析 + HTTP 請求）
        
        Args:
            url: 待檢測的 URL
        
        Returns:
            Tuple[str, str]: (檢測狀態, 結果說明)
        """
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # 1. DNS 解析
        try:
            socket.getaddrinfo(
                domain, 
                parsed.scheme, 
                timeout=self.config["dns_timeout"]
            )
        except socket.timeout:
            return "失敗", f"DNS 解析超時 ({self.config['dns_timeout']}s)"
        except socket.gaierror:
            return "失敗", "域名不存在或 DNS 解析失敗"
        except Exception as e:
            return "失敗", f"DNS 錯誤：{str(e)}"
        
        # 2. HTTP 請求
        try:
            response = requests.head(
                url,
                timeout=self.config["http_timeout"],
                allow_redirects=True,
                verify=False
            )
            response.raise_for_status()
            return "成功", f"HTTP {response.status_code} (正常響應)"
        except requests.Timeout:
            return "失敗", f"HTTP 請求超時 ({self.config['http_timeout']}s)"
        except requests.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else "未知"
            return "失敗", f"HTTP {status_code} 錯誤"
        except requests.ConnectionError:
            return "失敗", "連線失敗（網路問題或伺服器拒絕）"
        except Exception as e:
            return "失敗", f"請求異常：{str(e)}"

    def _check_single_url(self, url: str) -> Dict[str, str]:
        """
        單個 URL 完整檢測流程
        
        Args:
            url: 待檢測的 URL
        
        Returns:
            Dict[str, str]: 檢測結果字典
        """
        check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式驗證
        format_valid, format_msg = self._validate_url_format(url)
        if not format_valid:
            return {
                "url": url,
                "status": "失敗",
                "reason": f"格式錯誤：{format_msg}",
                "check_time": check_time
            }
        
        # 連通性檢測
        validated_url = format_msg
        conn_status, conn_msg = self._check_url_connectivity(validated_url)
        return {
            "url": validated_url,
            "status": conn_status,
            "reason": conn_msg,
            "check_time": check_time
        }

    def validate_urls_batch(self, urls: List[str]) -> pd.DataFrame:
        """
        批量檢測 URL（多線程）
        
        Args:
            urls: URL 列表
        
        Returns:
            pd.DataFrame: 檢測結果表格
        """
        self.url_list = urls
        self.results.clear()
        
        if not urls:
            print("[警告] URL 列表為空")
            return pd.DataFrame()
        
        total_urls = len(urls)
        print(f"[檢測開始] 共 {total_urls} 個 URL，使用 {self.config['max_workers']} 個線程\n")
        
        completed = 0
        try:
            with ThreadPoolExecutor(max_workers=self.config["max_workers"]) as executor:
                future_to_url = {
                    executor.submit(self._check_single_url, url): url 
                    for url in urls
                }
                
                for future in as_completed(future_to_url):
                    result = future.result()
                    self.results.append(result)
                    completed += 1
                    progress = (completed / total_urls) * 100
                    print(f"進度: {completed}/{total_urls} ({progress:.1f}%)")
        
        except Exception as e:
            print(f"[檢測異常] {str(e)}")
        
        # 轉換為 DataFrame
        df = pd.DataFrame(self.results)
        print(f"\n[檢測完成]\n")
        return df

    def display_report(self, df: pd.DataFrame) -> None:
        """
        在 Colab 中顯示檢測報告表格
        
        Args:
            df: 檢測結果 DataFrame
        """
        if df.empty:
            print("[報告] 無結果可顯示")
            return
        
        # 統計信息
        total = len(df)
        success_count = len(df[df["status"] == "成功"])
        fail_count = total - success_count
        
        print("=" * 100)
        print(f"URL 檢測報告")
        print(f"檢測時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"總計: {total} 個 | 成功: {success_count} 個 | 失敗: {fail_count} 個")
        print("=" * 100)
        print()
        
        # 顯示詳細表格
        display(df.to_html(index=False, escape=False))

    def export_report(self, df: pd.DataFrame, export_format: str = "csv") -> Optional[str]:
        """
        導出檢測報告
        
        Args:
            df: 檢測結果 DataFrame
            export_format: 導出格式 ("csv" 或 "excel")
        
        Returns:
            Optional[str]: 導出檔案路徑
        """
        if df.empty:
            print("[導出] 無結果可導出")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_format.lower() == "csv":
                filename = f"url_validation_report_{timestamp}.csv"
                filepath = os.path.join("/tmp", filename)
                df.to_csv(filepath, index=False, encoding="utf-8-sig")
                print(f"✓ CSV 報告已導出: {filename}")
                return filepath
            
            elif export_format.lower() == "excel":
                try:
                    filename = f"url_validation_report_{timestamp}.xlsx"
                    filepath = os.path.join("/tmp", filename)
                    df.to_excel(filepath, index=False, sheet_name="驗證結果")
                    print(f"✓ Excel 報告已導出: {filename}")
                    return filepath
                except ImportError:
                    print("[提示] openpyxl 未安裝，自動轉為 CSV 格式")
                    return self.export_report(df, "csv")
            
            else:
                print(f"[錯誤] 不支援的導出格式: {export_format}")
                return None
        
        except Exception as e:
            print(f"[導出失敗] {str(e)}")
            return None


def main():
    """主函數：完整工作流程"""
    print("\n" + "=" * 100)
    print("URL 檢查器 v2.0.0 (Google Colab 版)")
    print("=" * 100 + "\n")
    
    # 1. 初始化檢查器
    validator = URLValidatorColab()
    
    # 2. 上傳檔案
    filepath = validator.upload_file_from_colab()
    if not filepath:
        print("[程式結束] 未上傳檔案")
        return
    
    # 3. 解析檔案提取 URL
    urls = validator.parse_url_file(filepath)
    if not urls:
        print("[程式結束] 未成功提取 URL")
        return
    
    # 4. 批量驗證 URL
    results_df = validator.validate_urls_batch(urls)
    
    # 5. 顯示報告
    validator.display_report(results_df)
    
    # 6. 導出報告選項
    print("\n[導出選項]")
    print("1. 導出為 CSV")
    print("2. 導出為 Excel")
    print("0. 跳過導出")
    
    choice = input("\n請選擇 (0-2): ").strip()
    if choice == "1":
        validator.export_report(results_df, "csv")
    elif choice == "2":
        validator.export_report(results_df, "excel")
    
    print("\n[程式完成]\n")


if __name__ == "__main__":
    main()
