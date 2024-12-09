
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import os

PUBLIC_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
SELENIUM_URL = os.getenv('SELENIUM_URL', 'http://selenium-hub:4444/wd/hub')


selenium_grid_url = 'http://selenium-hub:4444/wd/hub'

# selenium
option = webdriver.ChromeOptions()
option.set_capability("browserName", "chrome")
option.set_capability("browserVersion", "131.0")
option.set_capability("platformName", "Linux")
option.add_argument('--ignore-gpu-blocklist')
option.add_argument('--enable-features=VaapiVideoDecode')
wd = webdriver.Remote(command_executor=selenium_grid_url, options=option)

wd.implicitly_wait(10)

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('https://earthbucks.com/mine')

try:
    wd.find_element(By.ID, 'public-key').send_keys(PUBLIC_KEY)
    wd.find_element(By.ID, 'private-key').send_keys(PRIVATE_KEY)

    def find_slider():
        return wd.find_elements(
            By.CSS_SELECTOR, 'div.absolute.z-40.m-\\[-8px\\].h-\\[52px\\].w-\\[52px\\].p-\\[8px\\]')

    def find_block():
        return wd.find_elements(
            By.XPATH, '//div[img[@src="/images/compubutton/compute-circle.webp"]]')

    def switch_to_mining_iframe():
        # 切换到挖矿iframe
        mining_iframe = wd.find_element(
            By.CSS_SELECTOR, "iframe[title='Mining Button']")
        wd.switch_to.frame(mining_iframe)

    def switch_to_default():
        # 切回主页面
        wd.switch_to.default_content()

    def find_slider_in_iframe():
        # 在iframe中查找滑块
        return wd.find_elements(
            By.CSS_SELECTOR, 'div.absolute.z-40.m-\\[-8px\\].h-\\[52px\\].w-\\[52px\\].p-\\[8px\\]')

    def find_block_in_iframe():
        # 在iframe中查找目标块
        return wd.find_elements(
            By.XPATH, '//div[img[@src="/images/compubutton/compute-circle.webp"]]')

    def find_all_mining_iframes():
        # Find all mining button iframes
        return wd.find_elements(By.CSS_SELECTOR, "iframe[title='Mining Button']")

    # 获取滑块和目标位置的坐标
    sliders = find_slider()
    blocks = find_block()

    def execute_drag_and_drop(slider, block):
        action = ActionChains(wd)
        action.click_and_hold(slider).perform()
        time.sleep(random.uniform(0.5, 1.0))  # 模拟点击后的停顿

        # 获取滑块和目标位置的坐标
        slider_location = slider.location
        block_location = block.location

        # 计算滑动距离
        distance = block_location['x'] - \
            slider_location['x']+random.randint(20, 40)

        # 分段拖动滑块
        for i in range(10):
            move_distance = distance / 10
            action.move_by_offset(move_distance, 0).perform()
            time.sleep(random.uniform(0.005, 0.01))  # 模拟拖动过程中的停顿
        print('拖动完成')
        action.move_by_offset(1, 0).perform()
        print('松开')
        action.release().perform()
        print('松开完成')
    # 拖拽第一个滑块
    execute_drag_and_drop(sliders[0], blocks[0])

    time.sleep(5)

    # 重新获取
    sliders = find_slider()
    blocks = find_block()

    # 拖拽第二个滑块
    execute_drag_and_drop(sliders[1], blocks[1])

    time.sleep(3)
    # 进入begin页面
    sliders = find_slider()
    blocks = find_block()

    execute_drag_and_drop(sliders[0], blocks[0])

    time.sleep(3)

    # 选择下拉框准备开始挖矿
    dropdown_button = wd.find_element(
        By.XPATH, '/html/body/div/div[3]/div/div/button')
    dropdown_button.click()

    # 等待下拉框选项出现
    time.sleep(1)
    option = wd.find_element(By.XPATH, '//span[contains(text(), "4 Buttons")]')
    option.click()

    time.sleep(10)

    # 开始挖矿
    def slide_all_blocks():
        while True:
            try:

                # Get all iframes
                print("开始查找所有iframe")
                iframes_ = find_all_mining_iframes()
                iframes = [iframes_[1], iframes_[3], iframes_[5], iframes_[7]]
                if len(iframes) != 4:
                    print(
                        f"Warning: Expected 4 iframes, but found {len(iframes)}")
                    time.sleep(2)
                    raise Exception("Incorrect number of iframes")
                for i, iframe in enumerate(iframes):
                    try:
                        # 切换到iframe
                        print(f"开始进入iframe {i+1}")
                        wd.switch_to.frame(iframe)
                        print(f"进入iframe {i+1} 完成")
                        # 获取新的元素
                        # Get first (and only) slider
                        slider = find_slider_in_iframe()[0]
                        # Get first (and only) block
                        block = find_block_in_iframe()[0]

                        # Slide the block in current iframe
                        print(f"开始拖动 iframe{i+1} 的滑块")
                        execute_drag_and_drop(slider, block)

                        # Switch back to main content
                        print(f"开始退出 iframe {i+1}")
                        wd.switch_to.default_content()
                        print(f"退出 iframe {i+1} 完成")
                        # Random delay between iframes
                        time.sleep(random.uniform(0.5, 2.0))

                    except Exception as e:
                        print(f"Error in iframe {i}: {e}")
                        continue

                        # Add delay between iterations
                # time.sleep(random.uniform(1.0, 2.0))
            except Exception as e:
                print(f"Error in slide_all_blocks: {e}")
                raise Exception("Error in slide_all_blocks")

    slide_all_blocks()

except Exception as e:
    print(e)
    wd.quit()
finally:
    print('done')
    wd.quit()
