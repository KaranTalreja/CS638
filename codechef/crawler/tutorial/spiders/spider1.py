import scrapy
from selenium import webdriver
from tutorial.items import Question
import sys


class Code_Spider(scrapy.Spider):
    name = "code_spider1"

    start_urls = [
        'https://www.codechef.com/problems/extcontest/?sort_by=SuccessfulSubmission&sorting_order=desc',
        'https://www.codechef.com/problems/easy/',
        'https://www.codechef.com/problems/medium/',
        'https://www.codechef.com/problems/hard/',
        'https://www.codechef.com/problems/challenge/',
        'https://www.codechef.com/problems/school/',
    ]

    error_file = open("spider1_misses", "w")

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)

    # todo: init function

    def parse(self, response):
        rows = response.xpath("//tr[@class='problemrow']")
        i = 0
        print(str(len(rows)) + " in " + response.url)
        for row in rows:
            link = row.xpath("td")[0].xpath("div/a/@href")[0].extract()
            successful = row.xpath("td")[2].xpath("div/text()").extract()[0]
            accuracy = row.xpath("td")[3].xpath("a/text()").extract()[0]
            request = scrapy.Request(
                "https://www.codechef.com" + link, callback=self.parse_question)
            request.meta["link"] = link
            request.meta["successful"] = successful
            request.meta["accuracy"] = accuracy
            request.meta["count"] = i
            i += 1
            yield request

    def spider_closed(self, spider):
        self.driver.close()
        self.error_file.close()

    def parse_question(self, response):
        try:
            question = Question()
            question["link"] = response.url
            self.driver.get(response.url)

            # field
            question["success_count"] = response.meta["successful"]

            # field
            question["accuracy"] = response.meta["accuracy"]

            # print(str(response.meta["count"]))
            # field
            question["index"] = response.meta["count"]

            # field
            question["title"] = self.driver.find_element_by_xpath(
                "//h1[@class='title']").text

            # field
            question["problem_code"] = self.driver.find_element_by_xpath(
                "//span[@id='problem-code']").text

            # field
            try:
                question["submissions_page"] = "https://www.codechef.com/status/{}?sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO".format(question[
                                                                                                                                                                  "problem_code"])
            except:
                question["submissions_page"] = ""

            try:
                contents_p = self.driver.find_element_by_xpath(
                    "//div[@id='problem-left']/div[@class='content']/p[1]")

            # field
                description = ""
                while(contents_p.tag_name != 'h3'):
                    description += contents_p.text
                    contents_p = contents_p.find_element_by_xpath(
                        "following-sibling::*")
                question["description"] = description
            except:
                question["description"] = ""

            try:
                input_element = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Input')]")

                # field
                input_text = ""

                sibling_element = input_element.find_element_by_xpath(
                    "following-sibling::*")
                # todo: check if we need to test for h3 or 'output'
                while(sibling_element.tag_name != "h3"):
                    input_text += sibling_element.text
                    sibling_element = sibling_element.find_element_by_xpath(
                        "following-sibling::*")

                question["input_text"] = input_text
            except:
                question["input_text"] = ""

            try:
                output_element = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Output')]")

                # field
                output_text = ""

                sibling_element = output_element.find_element_by_xpath(
                    "following-sibling::*")

                while(sibling_element.tag_name != "h3"):
                    output_text += sibling_element.text
                    sibling_element = sibling_element.find_element_by_xpath(
                        "following-sibling::*")

                question["output_text"] = output_text
            except:
                question["output_text"] = ""

            # field
            try:
                question["date_added"] = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Date Added:')]").find_element_by_xpath("following-sibling::*").text
            except:
                question["date_added"] = ""

            # field
            try:
                question["source_limit"] = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Source Limit:')]").find_element_by_xpath("following-sibling::*").text
            except:
                question["source_limit"] = ""

            # field
            try:
                question["time_limit"] = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Time Limit:')]").find_element_by_xpath("following-sibling::*").text
            except:
                question["time_limit"] = ""

            # field list
            try:
                question["tags"] = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Tags:')]").find_element_by_xpath("following-sibling::*").text.split()
            except:
                question["tags"] = ""

            # field
            try:
                question["editorial_page"] = self.driver.find_element_by_xpath(
                    "//*[contains(text(),'Editorial:')]").find_element_by_xpath("following-sibling::*").text
            except:
                question["editorial_page"] = ""

        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.error_file.write(response.url + "\n")

        yield question
