# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 14:52:40 2016

@author: karan
"""

import scrapy

class ProblemSpider(scrapy.Spider):
    name = "problems"

    def start_requests(self):
        urls = ['http://www.spoj.com/problems/classical/sort=0,start={}' \
        .format(num) for num in range(0,3500,50)]
        [urls.append(link) for link in \
        ['http://www.spoj.com/problems/challenge/sort=0,start={}' \
        .format(num) for num in range(0,150,50)]]
        [urls.append(link) for link in \
        ['http://www.spoj.com/problems/tutorial/sort=0,start={}' \
        .format(num) for num in range(0,1300,50)]]
        [urls.append(link) for link in \
        ['http://www.spoj.com/problems/basics/sort=0,start={}' \
        .format(num) for num in range(0,100,50)]]
        [urls.append(link) for link in \
        ['http://www.spoj.com/problems/riddle/sort=0,start={}' \
        .format(num) for num in range(0,50,50)]]
        [urls.append(link) for link in \
        ['http://www.spoj.com/problems/partial/sort=0,start={}' \
        .format(num) for num in range(0,200,50)]]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        for row in response.css("table tbody tr"):
            currProblem = {}
            problemUrl = response.urljoin(row.css("td a::attr(href)")[0].extract())           
            problemUsers = row.css("td a::text")[1].extract().strip()
            problemUserRanks = response.urljoin(row.css("td a::attr(href)")[1].extract())
            problemAcc = row.css("td a::text")[2].extract().strip()
            problemId = row.css("td::text")[0].extract().strip()
            problemImpDiff = "NA"
            problemConceptDiff = "NA"
            if 1 < len(row.css("td")[-1].css("span::text").extract()):
                problemImpDiff = row.css("td")[-1].css("span::text").extract()[0]
                problemConceptDiff = row.css("td")[-1].css("span::text").extract()[1]
            elif len(row.css("td")[-1].css("span::text").extract()):
                problemImpDiff = row.css("td")[-1].css("span::text").extract()[0]
            currProblem["id"] = problemId.encode("ascii",'ignore')
            currProblem["url"] = problemUrl.encode("ascii",'ignore')
            currProblem["solved_by"] = problemUsers.encode("ascii",'ignore')
            currProblem["user_ranks"] = problemUserRanks.encode("ascii",'ignore')
            currProblem["accuracy"] = problemAcc.encode("ascii",'ignore')
            currProblem["implementation_difficulty"] = problemImpDiff.encode("ascii",'ignore')
            currProblem["concept_difficulty"] = problemConceptDiff.encode("ascii",'ignore')
            request = scrapy.Request(problemUrl, callback=self.parseProblem) 
            request.meta['currProblem'] = currProblem
            yield request

    def parseProblem(self, response):
        try:
            problemTitle = response.xpath("//h2[@id='problem-name']/text()") \
            .extract_first(default='not-found')
            if problemTitle != 'not-found':
                problemCode = problemTitle.split(" - ")[0].strip()
            response.meta['currProblem']["title"] = problemTitle.strip().encode("ascii",'ignore')
        except:
            print "Error:Problem Name {}".format(response.url)
        try:  
            tags = {}
            problemTags = response.xpath("//div[@id='problem-tags']/a")
            for tag in problemTags:
                tagName = tag.xpath("span/text()").extract_first().strip().encode("ascii",'ignore')
                tagLink = response.urljoin(tag.xpath("@href").extract_first()).encode("ascii",'ignore')
                tags[tagName] = tagLink
            response.meta['currProblem']["tags"] = tags
        except:
            print "Error:Problem Tags {}".format(response.url)
        try:                
            problemBody = response.xpath("//div[@id='problem-body']/descendant-or-self::*/text()").extract()
            problemDesc = {}
            problemDesc["description"] = ""
            problemDesc["inputDesc"] = ""
            problemDesc["outputDesc"] = ""
            key = "description"
            for stmt in problemBody:
                stmt = stmt.strip().encode("ascii",'ignore')                
                if key == "description" and stmt == "Input":
                    key = "inputDesc"
                    continue
                elif key == "inputDesc" and stmt == "Output":
                    key = "outputDesc"
                    continue
                problemDesc[key] = problemDesc[key] + " " + stmt
            response.meta['currProblem']["description"] = problemDesc["description"]
            response.meta['currProblem']["input"] = problemDesc["inputDesc"]
            response.meta['currProblem']["output"] = problemDesc["outputDesc"]
        except:
            print "Error:Problem Description {}".format(response.url)

        problemMeta = response.xpath("//table[@id='problem-meta']/tbody/tr")
        try:
            addedByUser = {}
            userName = problemMeta[0].xpath("td/a/text()").extract_first().encode("ascii",'ignore')
            userLink = response.urljoin(problemMeta[0].xpath("td/a/@href").extract_first())
            addedByUser[userName] = userLink.encode("ascii",'ignore')
            response.meta['currProblem']["added_by"] = addedByUser
        except:
            print "Error:Problem Added By {}".format(response.url)
        
        try:
            response.meta['currProblem']["date_added"] = problemMeta[1].\
            xpath("td/text()")[1].extract().encode("ascii",'ignore')
        except:
            print "Error:Problem Add Date {}".format(response.url)

        try:            
            response.meta['currProblem']["time_limit"] = problemMeta[2].\
            xpath("td/text()")[1].extract().strip().encode("ascii",'ignore')    
            response.meta['currProblem']["source_limit"] = problemMeta[3].\
            xpath("td/text()")[1].extract().strip().encode("ascii",'ignore')
            response.meta['currProblem']["memory_limit"] = problemMeta[4].\
            xpath("td/text()")[1].extract().strip().encode("ascii",'ignore')
            response.meta['currProblem']["languages"] = problemMeta[6].\
            xpath("td/text()")[1].extract().strip().encode("ascii",'ignore')
        except:
            print "Error:Problem Meta {}".format(response.url)
        filename = 'html/Problem_{}.html'.format(problemCode)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        yield {
            response.meta['currProblem']["id"] : response.meta["currProblem"]
        }
