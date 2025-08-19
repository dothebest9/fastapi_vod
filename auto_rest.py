from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://zep.us/play/N3A5q9")


time.sleep(5)

try:
    time.sleep(5)
    nickname_input = driver.find_element(By.NAME, "name")
    print("별명삭제")
    nickname_input.send_keys(Keys.CONTROL + "a")
    nickname_input.send_keys(Keys.DELETE)
    text_to_type = "BE_13_최선구!"
    nickname_input.send_keys(text_to_type)
    print(f"입력 완료: '{text_to_type}'")
    time.sleep(5)
    nickname_input.send_keys(Keys.RETURN)
    chat_input_box = driver.find_element(By.ID, "chat-input")
    #휴식시 메시지
    message = "10분 휴식하겠습니다."
    chat_input_box.send_keys(message)
    # 엔터 키를 눌러 메시지를 전송합니다.
    chat_input_box.send_keys(Keys.RETURN)

    #600초 뒤인 10분
    time.sleep(600)
    message = "복귀하였습니다."

    button_to_click = driver.find_element(By.CSS_SELECTOR, "#floatingContainer > div:nth-child(2) > img")

    print("요소를 성공적으로 클릭했습니다.")
    chat_input_box.send_keys(message)


except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 자동화 작업이 끝난 후 브라우저를 닫습니다.
    # driver.quit()
    pass # 테스트를 위해 브라우저를 열어두려면 이 줄을 주석 처리하거나 pass로 둡니다.