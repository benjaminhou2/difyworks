#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify工作流自动化测试脚本
用于导入和测试香水短视频分析工作流
"""

import time
import os
import json
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)

class DifyWorkflowTester:
    """Dify工作流测试类"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.workflow_file_path = r"E:\tools\DifyWorks\workflows\香水短视频分析工作流_官方语法修复版.yml"
        self.base_url = "https://dify.xiaooutech.com"
        self.apps_url = f"{self.base_url}/apps"
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "workflow_file": self.workflow_file_path,
            "success": False,
            "errors": [],
            "warnings": [],
            "performance": {},
            "workflow_info": None
        }
    
    def setup_chrome_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            print("🚀 正在设置Chrome浏览器...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # 设置下载目录和文件处理
            prefs = {
                "download.default_directory": os.path.dirname(os.path.abspath(__file__)),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # 尝试自动查找Chrome驱动
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                print(f"⚠️ 自动查找Chrome驱动失败: {e}")
                print("💡 请确保已安装ChromeDriver或使用webdriver-manager")
                raise
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)
            
            print("✅ Chrome浏览器设置完成")
            return True
            
        except Exception as e:
            error_msg = f"Chrome浏览器设置失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["errors"].append({
                "type": "Browser Setup Error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def navigate_to_apps(self):
        """导航到Dify应用页面"""
        try:
            print(f"🌐 正在访问: {self.apps_url}")
            start_time = time.time()
            
            self.driver.get(self.apps_url)
            
            # 等待页面加载完成
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            load_time = time.time() - start_time
            self.test_results["performance"]["page_load_time"] = load_time
            
            print(f"✅ 页面加载完成 (耗时: {load_time:.2f}秒)")
            
            # 检查是否需要登录
            current_url = self.driver.current_url
            if "login" in current_url.lower() or "signin" in current_url.lower():
                self.test_results["warnings"].append({
                    "type": "Login Required",
                    "message": "检测到需要登录，请手动登录后重新运行脚本",
                    "timestamp": datetime.now().isoformat()
                })
                print("⚠️ 需要登录，请手动登录后继续...")
                input("登录完成后按Enter键继续...")
            
            return True
            
        except Exception as e:
            error_msg = f"页面导航失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["errors"].append({
                "type": "Navigation Error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def import_workflow_dsl(self):
        """导入DSL工作流文件"""
        try:
            print("📁 正在导入DSL工作流文件...")
            
            # 检查文件是否存在
            if not os.path.exists(self.workflow_file_path):
                raise FileNotFoundError(f"工作流文件不存在: {self.workflow_file_path}")
            
            # 查找导入按钮或创建按钮
            possible_selectors = [
                "//button[contains(text(), '导入')]",
                "//button[contains(text(), 'Import')]", 
                "//button[contains(text(), '创建')]",
                "//button[contains(text(), 'Create')]",
                "//a[contains(text(), '导入')]",
                "//a[contains(text(), 'Import')]",
                "//*[@data-testid='import-dsl']",
                "//*[@data-testid='create-app']",
                "//button[contains(@class, 'import')]",
                "//button[contains(@class, 'create')]"
            ]
            
            import_button = None
            for selector in possible_selectors:
                try:
                    import_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ 找到导入按钮: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if import_button is None:
                # 尝试通过页面截图进行调试
                self.driver.save_screenshot("debug_apps_page.png")
                print("📸 已保存页面截图: debug_apps_page.png")
                
                raise NoSuchElementException("未找到导入或创建按钮")
            
            # 点击导入按钮
            self.driver.execute_script("arguments[0].click();", import_button)
            time.sleep(2)
            
            # 查找DSL导入选项
            dsl_selectors = [
                "//button[contains(text(), 'DSL')]",
                "//a[contains(text(), 'DSL')]", 
                "//div[contains(text(), 'DSL')]",
                "//*[contains(@class, 'dsl')]",
                "//button[contains(text(), '从DSL文件导入')]",
                "//button[contains(text(), 'Import from DSL')]"
            ]
            
            dsl_option = None
            for selector in dsl_selectors:
                try:
                    dsl_option = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ 找到DSL选项: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if dsl_option:
                self.driver.execute_script("arguments[0].click();", dsl_option)
                time.sleep(2)
            
            # 查找文件上传输入框
            file_input_selectors = [
                "//input[@type='file']",
                "//*[@accept='.yml,.yaml']",
                "//*[contains(@class, 'file-input')]"
            ]
            
            file_input = None
            for selector in file_input_selectors:
                try:
                    file_input = self.driver.find_element(By.XPATH, selector)
                    print(f"✅ 找到文件输入框: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if file_input is None:
                raise NoSuchElementException("未找到文件上传方式")
            
            # 上传文件
            print(f"📤 正在上传文件: {self.workflow_file_path}")
            file_input.send_keys(self.workflow_file_path)
            time.sleep(3)
            
            # 查找确认按钮
            confirm_selectors = [
                "//button[contains(text(), '确认')]",
                "//button[contains(text(), 'Confirm')]",
                "//button[contains(text(), '导入')]", 
                "//button[contains(text(), 'Import')]",
                "//button[contains(text(), '创建')]",
                "//button[contains(text(), 'Create')]",
                "//button[@type='submit']"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ 找到确认按钮: {selector}")
                    self.driver.execute_script("arguments[0].click();", confirm_button)
                    break
                except TimeoutException:
                    continue
            
            # 等待导入完成
            print("⏳ 等待导入完成...")
            time.sleep(5)
            
            print("✅ DSL文件导入完成")
            return True
            
        except Exception as e:
            error_msg = f"DSL导入失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["errors"].append({
                "type": "Import Error",
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def find_and_open_workflow(self):
        """查找并打开新创建的工作流"""
        try:
            print("🔍 正在查找新创建的工作流...")
            
            # 刷新页面
            self.driver.refresh()
            time.sleep(3)
            
            # 查找工作流项目
            workflow_selectors = [
                "//div[contains(text(), '香水短视频分析')]",
                "//a[contains(text(), '香水短视频分析')]",
                "//h3[contains(text(), '香水短视频分析')]",
                "//*[contains(@title, '香水短视频分析')]",
                "//*[contains(@class, 'workflow')]",
                "//*[contains(@class, 'app-card')]"
            ]
            
            workflow_element = None
            for selector in workflow_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if "香水短视频分析" in element.text or "香水短视频分析" in element.get_attribute("title"):
                            workflow_element = element
                            print(f"✅ 找到工作流: {selector}")
                            break
                    if workflow_element:
                        break
                except NoSuchElementException:
                    continue
            
            if workflow_element is None:
                # 尝试找到最新创建的工作流
                print("🔄 尝试查找最新创建的工作流...")
                latest_workflow_selectors = [
                    "(//*[contains(@class, 'app-card')])[1]",
                    "(//*[contains(@class, 'workflow')])[1]",
                    "(//div[contains(@class, 'item')])[1]"
                ]
                
                for selector in latest_workflow_selectors:
                    try:
                        workflow_element = self.driver.find_element(By.XPATH, selector)
                        print(f"✅ 找到最新工作流: {selector}")
                        break
                    except NoSuchElementException:
                        continue
            
            if workflow_element is None:
                raise NoSuchElementException("未找到工作流项目")
            
            # 获取工作流信息
            workflow_title = workflow_element.text or workflow_element.get_attribute("title") or "未知工作流"
            self.test_results["workflow_info"] = {
                "title": workflow_title,
                "found_timestamp": datetime.now().isoformat()
            }
            
            print(f"🎯 准备打开工作流: {workflow_title}")
            
            # 点击打开工作流
            self.driver.execute_script("arguments[0].click();", workflow_element)
            time.sleep(5)
            
            print("✅ 工作流已打开")
            return True
            
        except Exception as e:
            error_msg = f"查找工作流失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["errors"].append({
                "type": "Workflow Search Error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def monitor_rendering_errors(self):
        """监控浏览器渲染异常"""
        try:
            print("🔍 正在监控浏览器渲染状态...")
            
            # 等待页面完全加载
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 检查JavaScript错误
            js_errors = self.driver.get_log('browser')
            if js_errors:
                for error in js_errors:
                    if error['level'] in ['SEVERE', 'WARNING']:
                        self.test_results["errors"].append({
                            "type": "JavaScript Error",
                            "level": error['level'],
                            "message": error['message'],
                            "timestamp": error['timestamp'],
                            "source": error.get('source', 'unknown')
                        })
                        print(f"⚠️ JavaScript {error['level']}: {error['message']}")
            
            # 截图保存当前状态
            screenshot_path = f"workflow_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 已保存页面截图: {screenshot_path}")
            
            return len(js_errors) == 0
            
        except Exception as e:
            error_msg = f"渲染监控失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["errors"].append({
                "type": "Monitoring Error",
                "message": error_msg,
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def analyze_errors(self):
        """分析收集到的错误信息"""
        try:
            print("\n🔍 === 错误分析报告 ===")
            
            if not self.test_results["errors"]:
                print("✅ 未发现任何错误！")
                self.test_results["success"] = True
                return
            
            error_categories = {}
            for error in self.test_results["errors"]:
                error_type = error.get("type", "Unknown")
                if error_type not in error_categories:
                    error_categories[error_type] = []
                error_categories[error_type].append(error)
            
            print(f"📊 总共发现 {len(self.test_results['errors'])} 个问题")
            print(f"📂 错误类型: {len(error_categories)} 种")
            
            for error_type, errors in error_categories.items():
                print(f"\n🔸 {error_type} ({len(errors)}个):")
                for i, error in enumerate(errors, 1):
                    print(f"   {i}. {error.get('message', 'No message')}")
            
        except Exception as e:
            print(f"❌ 错误分析失败: {str(e)}")
    
    def save_test_results(self):
        """保存测试结果"""
        try:
            self.test_results["end_time"] = datetime.now().isoformat()
            duration = datetime.fromisoformat(self.test_results["end_time"]) - datetime.fromisoformat(self.test_results["start_time"])
            self.test_results["duration_seconds"] = duration.total_seconds()
            
            result_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 测试结果已保存: {result_file}")
            return result_file
            
        except Exception as e:
            print(f"⚠️ 保存测试结果失败: {str(e)}")
            return None
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.driver:
                self.driver.quit()
                print("🧹 浏览器已关闭")
        except Exception as e:
            print(f"⚠️ 清理资源时出现问题: {str(e)}")
    
    def run_test(self):
        """运行完整测试流程"""
        print("🚀 === Dify工作流自动化测试开始 ===\n")
        
        try:
            # 1. 设置浏览器
            if not self.setup_chrome_driver():
                return False
            
            # 2. 导航到应用页面
            if not self.navigate_to_apps():
                return False
            
            # 3. 导入DSL工作流
            if not self.import_workflow_dsl():
                return False
            
            # 4. 查找并打开工作流
            if not self.find_and_open_workflow():
                return False
            
            # 5. 监控渲染错误
            rendering_ok = self.monitor_rendering_errors()
            
            # 6. 分析错误
            self.analyze_errors()
            
            # 7. 保存结果
            self.save_test_results()
            
            if rendering_ok and not self.test_results["errors"]:
                print("\n🎉 === 测试完成: 成功 ===")
                self.test_results["success"] = True
                return True
            else:
                print("\n⚠️ === 测试完成: 发现问题 ===")
                return False
                
        except KeyboardInterrupt:
            print("\n⏹️ 用户中断测试")
            return False
        except Exception as e:
            print(f"\n❌ 测试过程中发生未预期错误: {str(e)}")
            print(f"详细错误: {traceback.format_exc()}")
            return False
        finally:
            self.cleanup()

def main():
    """主函数"""
    print("=" * 60)
    print("🌹 Dify香水短视频分析工作流测试脚本")
    print("📅 版本: 1.0")
    print("👨‍💻 功能: 自动导入工作流并检测渲染异常")
    print("=" * 60)
    
    # 检查依赖
    try:
        from selenium import webdriver
        print("✅ Selenium库检查通过")
    except ImportError:
        print("❌ 请安装Selenium: pip install selenium")
        return
    
    # 检查工作流文件
    workflow_file = r"E:\tools\DifyWorks\workflows\香水短视频分析工作流_官方语法修复版.yml"
    if not os.path.exists(workflow_file):
        print(f"❌ 工作流文件不存在: {workflow_file}")
        return
    else:
        print(f"✅ 工作流文件检查通过: {os.path.basename(workflow_file)}")
    
    # 运行测试
    tester = DifyWorkflowTester()
    success = tester.run_test()
    
    if success:
        print("\n🎊 恭喜！工作流测试全部通过！")
    else:
        print("\n📋 测试发现了一些问题，请查看详细报告进行修复。")

if __name__ == "__main__":
    main() 