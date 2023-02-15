import os
import re

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import Page, expect, sync_playwright


class MyViewTests(StaticLiveServerTestCase):
    fixtures = [
        "pizza/fixtures/ingredients.json.gz",
        "pizza/fixtures/pizzas.json.gz",
    ]

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False)
        cls.context = cls.browser.new_context()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self) -> None:
        User.objects.create_superuser(
            "mytestuser",
            "mytestuser@test.com",
            "mytestpassword",
            is_staff=True,
        )
        return super().setUp()

    def new_page_and_login(self) -> Page:
        page = self.context.new_page()
        page.goto(f"{self.live_server_url}/admin/")
        page.get_by_label("Username:").click()
        page.get_by_label("Username:").fill("mytestuser")
        page.get_by_label("Username:").press("Tab")
        page.get_by_label("Password:").fill("mytestpassword")
        page.get_by_label("Password:").press("Tab")
        page.get_by_role("button", name="Log in").press("Enter")
        return page

    def test_add_pizzas(self):
        page = self.new_page_and_login()
        page.get_by_role("row", name="Pizzas Add Change").get_by_role(
            "link", name="Add"
        ).click()
        page.get_by_label("Name:").fill("Custom 1")
        page.get_by_role("listbox", name="Ingredients:").select_option("2")
        page.get_by_role("listbox", name="Ingredients:").select_option(["2", "3"])
        page.get_by_role("listbox", name="Ingredients:").select_option(["2", "3", "4"])
        page.get_by_role("listbox", name="Ingredients:").select_option(
            ["2", "3", "4", "5"]
        )
        page.get_by_role("listbox", name="Ingredients:").select_option(
            ["2", "3", "4", "5", "8"]
        )
        page.get_by_role("button", name="Save", exact=True).click()
        expect(
            page.get_by_text(re.compile("^0 of \\d+ selected$", re.IGNORECASE))
        ).to_have_text("0 of 2 selected")
        page.get_by_role("cell", name="9.0").click()
        page.get_by_role("cell", name="5.0").click()

        margherita_row = page.get_by_role("row", name="Margherita")
        expect(margherita_row).to_contain_text(
            "Base with white flour, Tomato, Mozzarella cheese"
        )
        expect(margherita_row).to_contain_text("5.0")
        custom_row = page.get_by_role("row", name="Custom 1")
        expect(custom_row).to_contain_text(
            "Base with wholemeal flour, Tomato, Mozzarella cheese, Baked ham, Parmesan"
        )
        expect(custom_row).to_contain_text("9.0")

    def test_ingredient_validator(self):
        page = self.new_page_and_login()

        page.get_by_role("row", name="Ingredients Add Change").get_by_role(
            "link", name="Add"
        ).click()
        page.get_by_role("button", name="Save", exact=True).click()
        expect(page.get_by_text("This field is required. Name:")).to_be_visible()
        expect(page.get_by_text("This field is required. Price:")).to_be_visible()
        page.get_by_label("Name:").click()
        page.get_by_label("Name:").fill("pineapple")
        page.get_by_role("button", name="Save", exact=True).click()
        expect(
            page.get_by_text('"pineapple" is not a valid ingredient Name:')
        ).to_be_visible()

    def test_pizza_validator(self):
        page = self.new_page_and_login()

        page.get_by_role("row", name="Pizzas Add Change").get_by_role(
            "link", name="Add"
        ).click()
        page.get_by_role("button", name="Save", exact=True).click()
        expect(page.get_by_text("This field is required. Name:")).to_be_visible()
        expect(page.get_by_text("This field is required. Ingredients:")).to_be_visible()
        page.get_by_label("Name:").click()
        page.get_by_label("Name:").fill("hawaii")
        page.get_by_label("Name:").press("Enter")
        expect(
            page.get_by_text(
                '"hawaii" is not a pizza, it\'s a crime against humanity Name:'
            )
        ).to_be_visible()
