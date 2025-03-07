import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Sesuaikan dengan path driver
        self.driver.get("http://localhost/quiz-pengupil-main/login.php")  # Sesuaikan dengan URL lokal Anda

    def test_valid_login(self):
        """Test login dengan data valid."""
        driver = self.driver
        driver.find_element(By.NAME, "username").send_keys("salsaawhy")  # Username valid
        driver.find_element(By.NAME, "password").send_keys("helo")  # Password valid
        driver.find_element(By.NAME, "submit").click()

        time.sleep(2)  # Beri waktu untuk proses redirect
        
        # Pastikan berhasil dengan mengecek apakah halaman berpindah ke index.php
        if "index.php" in driver.current_url:
            print("✅ Login berhasil dengan data valid!")
        else:
            print("❌ Login gagal, cek log untuk detailnya.")

        self.assertIn("index.php", driver.current_url)

    def test_invalid_password(self):
        """Test login dengan password salah."""
        driver = self.driver
        driver.find_element(By.NAME, "username").send_keys("salsaawhy")  # Username valid
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")  # Password salah
        driver.find_element(By.NAME, "submit").click()

        time.sleep(2)

        # Cek apakah tetap berada di halaman login setelah gagal login
        self.assertIn("login.php", driver.current_url)

        # Cek jika elemen login masih ada
        login_element = driver.find_element(By.NAME, "submit")
        self.assertTrue(login_element.is_displayed(), "Login form masih ditampilkan, login gagal.")

    def test_empty_fields(self):
        """Test login dengan field kosong."""
        driver = self.driver

        # Klik tombol login tanpa mengisi input apa pun
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
