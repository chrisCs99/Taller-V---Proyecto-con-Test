import time
import unittest

from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utilities import get_driver, take_screenshot

class SkyNet(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver('chrome', 'http://127.0.0.1:5500/')

    def test_register_user(self):
        self.driver.get('http://127.0.0.1:5500/login.html')
        register_name = self.driver.find_element_by_id('reg_nombre')
        register_name.send_keys('Felix')
        register_lastname = self.driver.find_element_by_id('reg_apellido')
        register_lastname.send_keys('Mamani')
        register_username = self.driver.find_element_by_id('reg_username')
        register_username.send_keys('fmamani224')
        register_email = self.driver.find_element_by_id('reg_email')
        register_email.send_keys('fmam22@ex.com')
        register_password = self.driver.find_element_by_id('reg_password')
        register_password.send_keys('Test1234')
        self.assertIsNotNone(register_name, "Debe de tener un nombre")
        self.assertIsNotNone(register_lastname, "Debe de tener un apellido")
        self.assertIsNotNone(register_username, "Debe de tener un nombre de usuario")
        self.assertIsNotNone(register_email, "Debe de tener un correo")
        self.assertIsNotNone(register_password, "Debe de tener una password")
        take_screenshot(self.driver, 'register_user_data')
        self.driver.implicitly_wait(10)
        login_button = self.driver.find_element_by_name('register')
        login_button.click()
        time.sleep(1)
        take_screenshot(self.driver, 'register_user_finished')
        time.sleep(5)
        take_screenshot(self.driver, 'register_user_profile')

    def test_login(self):
        login_button = self.driver.find_element_by_id('cambiarValor')
        login_button.click()
        take_screenshot(self.driver, 'login_redirect')
        self.driver.implicitly_wait(100)
        login_name = self.driver.find_element_by_id('username')
        login_name.send_keys('pmander')
        login_password = self.driver.find_element_by_id('password')
        login_password.send_keys('Test1234')
        take_screenshot(self.driver, 'login_data')
        self.driver.implicitly_wait(1000)
        login_button_click = self.driver.find_element_by_id('accederBtn')
        login_button_click.click()
        time.sleep(3)
        take_screenshot(self.driver, 'login_success')
        time.sleep(3)
        take_screenshot(self.driver, 'login_success_profile')

    def test_logout(self):
        login_button = self.driver.find_element_by_id('cambiarValor')
        login_button.click()
        take_screenshot(self.driver, 'logout_login_redirect')
        self.driver.implicitly_wait(100)
        login_name = self.driver.find_element_by_id('username')
        login_name.send_keys('pmander')
        login_password = self.driver.find_element_by_id('password')
        login_password.send_keys('Test1234')
        take_screenshot(self.driver, 'login_data')
        self.driver.implicitly_wait(1000)
        login_button_click = self.driver.find_element_by_id('accederBtn')
        login_button_click.click()
        time.sleep(3)
        take_screenshot(self.driver, 'logout_login_success')
        time.sleep(3)
        take_screenshot(self.driver, 'logout_login_success_profile')
        time.sleep(1)
        logout_button = self.driver.find_element_by_id('cambiarValor')
        logout_button.click()
        take_screenshot(self.driver, 'logout')
        logout_button_confirmation = self.driver.find_element_by_class_name('swal2-confirm')
        logout_button_confirmation.click()
        take_screenshot(self.driver, 'logout_complete')
        time.sleep(3)
        take_screenshot(self.driver, 'logout_complete_index')


    def test_add_product_to_cart(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        list_cart = self.driver.find_element_by_id('lista-carrito')
        take_screenshot(self.driver, 'cart_with_product')
        self.driver.implicitly_wait(100)

    def test_clean_product_to_cart(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        list_cart = self.driver.find_element_by_id('lista-carrito')
        take_screenshot(self.driver, 'cart_with_product')
        self.driver.implicitly_wait(100)
        clean_cart = self.driver.find_element_by_id('vaciar-carrito')
        clean_cart.click()
        view_cart_liost.click()
        take_screenshot(self.driver, 'clean_cart')



    def test_add_differents_products(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        list_cart = self.driver.find_element_by_id('lista-carrito')
        view_cart_liost.click()
        time.sleep(2)
        take_screenshot(self.driver, 'cart_with_differents_products_1')
        self.driver.implicitly_wait(100)
        time.sleep(1)
        self.driver.get('http://127.0.0.1:5500')
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[2].find_element_by_class_name('btn-info').click()
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        time.sleep(5)
        take_screenshot(self.driver, 'cart_with_differents_products_2')

    def test_cart_required_login(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        list_cart = self.driver.find_element_by_id('lista-carrito')
        view_cart_liost.click()
        time.sleep(2)
        take_screenshot(self.driver, 'cart_required_with_product')
        self.driver.implicitly_wait(100)
        time.sleep(1)
        self.driver.get('http://127.0.0.1:5500')
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[2].find_element_by_class_name('btn-info').click()
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        time.sleep(3)
        take_screenshot(self.driver, 'cart_required_with_differents_products')
        buy_btn = self.driver.find_element_by_id('procesar-pedido')
        buy_btn.click()
        time.sleep(1)
        take_screenshot(self.driver, 'cart_required_login')

    def test_cart_buy(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        list_cart = self.driver.find_element_by_id('lista-carrito')
        view_cart_liost.click()
        time.sleep(2)
        take_screenshot(self.driver, 'cart_buy_with_product')
        self.driver.implicitly_wait(100)
        time.sleep(1)
        self.driver.get('http://127.0.0.1:5500')
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[2].find_element_by_class_name('btn-info').click()
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        time.sleep(3)
        take_screenshot(self.driver, 'cart_buy_with_differents_products')
        buy_btn = self.driver.find_element_by_id('procesar-pedido')
        buy_btn.click()
        time.sleep(1)
        take_screenshot(self.driver, 'cart_buy_login')
        self.driver.implicitly_wait(10)
        login_name = self.driver.find_element_by_id('username')
        login_name.send_keys('pmander')
        login_password = self.driver.find_element_by_id('password')
        login_password.send_keys('Test1234')
        take_screenshot(self.driver, 'cart_buy_login_data')
        login_button_click = self.driver.find_element_by_id('accederBtn')
        login_button_click.click()
        time.sleep(3)
        take_screenshot(self.driver, 'cart_buy_login_success')

    def test_buy_process(self):
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[0].find_element_by_class_name('btn-info').click()
        self.driver.implicitly_wait(100)
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        self.driver.implicitly_wait(100)
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        list_cart = self.driver.find_element_by_id('lista-carrito')
        view_cart_liost.click()
        time.sleep(2)
        take_screenshot(self.driver, 'cart_buy_with_product')
        self.driver.implicitly_wait(100)
        time.sleep(1)
        self.driver.get('http://127.0.0.1:5500')
        product_list = self.driver.find_elements_by_class_name('card-body')
        product_list[2].find_element_by_class_name('btn-info').click()
        shopping_cart_badge = self.driver.find_element_by_id('carritoAdd')
        shopping_cart_badge.click()
        view_cart_liost = self.driver.find_element_by_id('navbarCollapse')
        view_cart_liost.click()
        time.sleep(3)
        take_screenshot(self.driver, 'cart_buy_with_differents_products')
        buy_btn = self.driver.find_element_by_id('procesar-pedido')
        buy_btn.click()
        time.sleep(1)
        take_screenshot(self.driver, 'cart_buy_login')
        self.driver.implicitly_wait(10)
        time.sleep(3)
        login_name = self.driver.find_element_by_id('username')
        login_name.send_keys('pmander')
        login_password = self.driver.find_element_by_id('password')
        login_password.send_keys('Test1234')
        take_screenshot(self.driver, 'cart_buy_login_data')
        login_button_click = self.driver.find_element_by_id('accederBtn')
        login_button_click.click()
        time.sleep(3)
        take_screenshot(self.driver, 'cart_buy_login_success')
        self.driver.implicitly_wait(10)
        form_client = self.driver.find_element_by_id('cliente')
        form_client.send_keys('Papote Malote')
        form_client = self.driver.find_element_by_id('correo')
        form_client.send_keys('ppmalote@example.com')
        form_client = self.driver.find_element_by_id('nitFactura')
        form_client.send_keys('5901239')
        form_client = self.driver.find_element_by_id('dirEntrega')
        form_client.send_keys('Av. Siempre viva')
        form_client = self.driver.find_element_by_id('latEntrega')
        form_client.send_keys('15')
        form_client = self.driver.find_element_by_id('longEntrega')
        form_client.send_keys('-3')
        take_screenshot(self.driver, 'cart_buy_data')
        time.sleep(1)
        finish_buy = self.driver.find_element_by_id('procesar-compra')
        finish_buy.click()
        take_screenshot(self.driver, 'cart_buy_data_finish')
        time.sleep(2)
        self.driver.get('http://127.0.0.1:5500/historial.html')
        take_screenshot(self.driver, 'cart_buy_historial_buy')
        time.sleep(2)
        self.driver.implicitly_wait(10)
        detail_info = self.driver.find_elements_by_class_name('card-body')
        detail_info[0].find_element_by_class_name('btn-info').click()
        take_screenshot(self.driver, 'cart_buy_detail_product')
        time.sleep(2)
        logout_button = self.driver.find_element_by_id('cambiarValor')
        logout_button.click()
        take_screenshot(self.driver, 'cart_buy_logout')
        logout_button_confirmation = self.driver.find_element_by_class_name('swal2-confirm')
        logout_button_confirmation.click()
        take_screenshot(self.driver, 'cart_buy_logout_complete')
        time.sleep(3)
        take_screenshot(self.driver, 'cart_buy_logout_complete_index')

    def test_view_history(self):
        login_button = self.driver.find_element_by_id('cambiarValor')
        login_button.click()
        take_screenshot(self.driver, 'login_redirect')
        self.driver.implicitly_wait(100)
        login_name = self.driver.find_element_by_id('username')
        login_name.send_keys('pmander')
        login_password = self.driver.find_element_by_id('password')
        login_password.send_keys('Test1234')
        self.driver.implicitly_wait(1000)
        login_button_click = self.driver.find_element_by_id('accederBtn')
        login_button_click.click()
        time.sleep(3)
        self.driver.get('http://127.0.0.1:5500/historial.html')
        self.driver.implicitly_wait(1000)
        detail_info = self.driver.find_elements_by_class_name('card-body')
        print(detail_info)
        detail_info[0].find_element_by_class_name('btn-info').click()
        time.sleep(10)


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(testRunner=HTMLTestRunner(output="sauce_demo", report_name="report_saucedemo"))