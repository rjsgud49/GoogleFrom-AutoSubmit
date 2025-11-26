from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time

# ====== 기본 설정 ======
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf2GKGIfejbWalQNi3eJSCGAuyIZsudgq24V_NYJkvWDgilUQ/viewform"
LOG_FILE = "submission_log.txt"

# ====== 자동 입력 데이터 ======
FORM_DATA = {
    "people": "21박건형 21김채환 21송주영 21장현제 22박창연 22김태호",
    "purpose": "캡스톤 진행",
    "lab": "상관 없음",
    "times": ["야자"],   # 체크박스 여러개 가능
}

# ====== 브라우저 옵션 ======
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # 창 숨기기

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

def log_result(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

try:
    log_result("🚀 자동 제출 시작")
    driver.get(FORM_URL)

    # ===== 1페이지 =====
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@role='radio' and @data-value='대여 신청']")
    )).click()
    log_result("✔ 1페이지 신청 선택")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(),'다음')]")
    )).click()
    log_result("➡️ 2페이지 이동")

    wait.until(EC.presence_of_element_located((By.XPATH, "//form")))
    time.sleep(1)

    # ===== 2페이지 =====
    today = datetime.now()
    log_result("📄 2페이지 로딩 완료")


    # 날짜 입력 (자동으로 들어가면 생략)
    try:
        date_input = driver.find_element(By.XPATH, "//input[@type='date']")
        date_input.send_keys(today.strftime("%Y-%m-%d"))
        log_result(f"📅 날짜 입력 완료: {today.strftime('%Y-%m-%d')}")
    except:
        log_result("ℹ️ 날짜 입력란은 자동입력으로 처리됨")


    # --- 실습실 희망선택 ---
    try:
        lab = FORM_DATA["lab"]
        lab_radio = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//div[@role='radio' and @data-value='{lab}']")
        ))
        driver.execute_script("arguments[0].click();", lab_radio)
        log_result(f"🏫 실습실 선택: {lab}")
    except:
        log_result(f"⚠ 실습실 '{lab}' 선택 실패")

    # --- 사용 인원 입력 (textarea) ---
    try:
        people_area = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@id, 'i7')]//following::textarea[1]")
        ))
        people_area.send_keys(FORM_DATA["people"])
        log_result("👥 인원 입력 완료")
    except:
        log_result("⚠ 인원 입력란 찾기 실패")

    # --- 대여 시간 체크박스 ---
    for label in FORM_DATA["times"]:
        try:
            element = wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//div[@role='checkbox' and @data-answer-value='{label}']")
            ))
            driver.execute_script("arguments[0].click();", element)
            log_result(f"⏰ 체크박스 클릭: {label}")
        except:
            log_result(f"⚠ 체크박스 '{label}' 찾기 실패")

    # --- 대여 목적 (textarea) ---
    try:
        purpose_area = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@id,'i27')]//following::textarea[1]")
        ))
        purpose_area.send_keys(FORM_DATA["purpose"])
        log_result("📝 대여 목적 입력 완료")
    except:
        log_result("⚠ 대여 목적 입력란 찾기 실패")

    # --- 제출 ---
    try:
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='제출']")
        ))
        submit_btn.click()
        log_result("🎯 제출 완료!")
    except:
        log_result("⚠ 제출 버튼 찾기 실패")

    time.sleep(1)
    log_result("✅ 완료!")

except TimeoutException as e:
    log_result(f"⏰ Timeout 오류: {e}")
except Exception as e:
    log_result(f"❌ 기타 오류: {e}")
finally:
    driver.quit()
    log_result("🧹 브라우저 종료")
