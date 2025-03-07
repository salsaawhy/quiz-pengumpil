import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Sesuaikan dengan path driver
        self.driver.get("http://localhost/quiz-pengupil-main/register.php") 

    def test_valid_registration(self):
        """Test registrasi dengan data valid."""
        driver = self.driver
        driver.find_element(By.NAME, "name").send_keys("User Baru")
        driver.find_element(By.NAME, "email").send_keys("userbaru@example.com")
        driver.find_element(By.NAME, "username").send_keys("userbaru123")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "repassword").send_keys("password123")
        driver.find_element(By.NAME, "submit").click()
        
        time.sleep(2)  # Beri waktu untuk proses redirect
        
        # Pastikan berhasil dengan mengecek apakah halaman berpindah ke index.php
        if "index.php" in driver.current_url:
            print("Registrasi berhasil dengan data valid!")
        else:
            print("Registrasi gagal, cek log untuk detailnya.")

        self.assertIn("index.php", driver.current_url)

    def test_password_mismatch(self):
        """Test registrasi dengan password tidak cocok."""
        driver = self.driver
        driver.find_element(By.NAME, "name").send_keys("User Salah")
        driver.find_element(By.NAME, "email").send_keys("usersalah@example.com")
        driver.find_element(By.NAME, "username").send_keys("usersalah123")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "repassword").send_keys("password456")  # Password berbeda
        driver.find_element(By.NAME, "submit").click()

        time.sleep(2)

        # Cek pesan error "Password tidak sama"
        error_message = ""
        try:
            error_message = driver.find_element(By.CLASS_NAME, "text-danger").text
        except:
            pass

        print(f"Pesan Error yang Ditemukan: '{error_message}'") 

        self.assertIn("Password tidak sama", error_message)

    def test_empty_fields(self):
        """Test registrasi dengan field kosong."""
        driver = self.driver

        # Klik tombol register tanpa mengisi input apa pun
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()

        # Tunggu hingga pesan error muncul
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            error_text = error_message.text
        except:
            error_text = ""

        print(f"Pesan Error yang Ditemukan: '{error_text}'")  # Debugging

        self.assertIn("Data tidak boleh kosong", error_text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
