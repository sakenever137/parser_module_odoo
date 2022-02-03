# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import random
import json
import asyncio
import csv
import random
import sys
import requests
import aiohttp
from bs4 import BeautifulSoup
from pyppeteer import launch
import time
import csv
import psycopg2

result_list = []
class cron_parser(models.Model):
    _name = 'cron_parser.cron_parser'
    _description = 'cron_parser.cron_parser'
    @api.model
    def _blog_post_update(self):
        asyncio.run(self.gather_data())

        try:
            connection = psycopg2.connect(
                host='localhost',
                user='admin',
                password='admin',
                database='odoo14_base1'
            )
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         'TRUNCATE TABLE blog_post CASCADE'
            #     )
            #     cursor.execute(
            #         'ALTER SEQUENCE blog_post_id_seq RESTART WITH 1'
            #     )
            # connection.commit()
            count = 0
            with connection.cursor() as cursor:
                for content in result_list:
                    full_content = '{0}{1}{2}{3}'.format(content['item_content'].replace("'", ""),
                                                         content['itm_images'], content['istok_href'],
                                                         content['author'])
                    cursor.execute(
                        "INSERT INTO blog_post (message_main_attachment_id, website_meta_title, website_meta_description, website_meta_keywords, website_meta_og_img, seo_name, cover_properties , is_published,name, subtitle, author_id, author_name,active, blog_id, content,teaser_manual,create_date, published_date, post_date, create_uid, write_date, write_uid, visits, website_id) VALUES{}".format
                        ("("'NULL,NULL,NULL,NULL,NULL,NULL,'"'" + content['item_img'] + "'"',true,'"'" + content[
                            'item_header'] + "'"', NULL,3,''NULL'',TRUE,1,'"'" + full_content + "'"',NULL,'"'" +
                         content[
                             'item_time'] + "'"','"'" + content['item_time'] + "'"','"'" + content[
                             'item_time'] + "'"', 2, '"'" + content['item_time'] + "'"',2,0,NULL'");")
                    )
                    full_content = None
                    count += 1
            connection.commit()
        except Exception as _ex:
            return _ex
        finally:
            pass


    async def get_data_urls(self, s, href_url):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }
        async with s.get(url=href_url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                item_header = soup.find("h1", {"class": "entry-title"}).text.strip()
            except Exception as _ex:
                item_header = None
            try:
                item_author = soup.find("div", {"class": "author-header"}).text.strip()
                author = '''<p>''' + item_author + '''</p>'''
            except Exception as _ex:
                author = '''<p>Без Автора</p>'''
            try:
                item_istok = soup.find('div', class_="istok").find("a").get("href")
                href = '''<p>Источник:<a href="''' + item_istok + '''">Ссылка на источник</a></p>'''
            except Exception as _ex:
                href = '''<p>Без источника</p>'''
            try:
                item_time = soup.time.attrs['datetime'].strip()
            except Exception as _ex:
                item_time = None
            try:
                item_img = soup.find('img', class_="attachment-full size-full wp-post-image").get('src').strip()
                header_img = '''{"background-image":"url(''' + item_img + ''')","background_color_class":"o_cc3","background_color_style":"","opacity":"0.2","resize_class":"o_half_screen_height o_record_has_cover","text_align_class":""}'''
            except Exception as _ex:
                header_img = '''{"background_color_class": "o_cc3", "background-image": "none", "opacity": "0.2", "resize_class": "o_half_screen_height"}'''
            try:
                item_content = soup.find("div", class_="post-content").get_text().strip()
                section_of_post = '''<section class="s_text_block pt32 o_colored_level pb0" data-snippet="s_text_block" data-name="Text">
                                                       <div class="container s_allow_columns">
                                                        <p>{}</p>
                                                        </div>
                                                    </section>'''.format(item_content)
            except Exception as _ex:
                section_of_post = None
            links = []
            post_images = []
            try:
                imgs = soup.select('.post-content img')
                for img in imgs:
                    links = '''<section class="s_picture pb24 o_colored_level pt0" data-snippet="s_picture" data-name="Picture" style="">
                                                           <div class="container">
    
                                                           <p style="text-align: center;"></p>
                                                               <div class="row s_nb_column_fixed">
                                                                   <div class="o_colored_level pb0 col-lg-7" style="text-align: center;">
                                                                       <figure class="figure">
                                                                           <img src="{}" class="figure-img img-thumbnail padding-large d-block mx-auto" alt="" loading="lazy" data-original-title="" title="" aria-describedby="tooltip271229" style="">
                                                                           </figure>
                                                                   </div>
                                                               </div>
                                                           </div>
                                                       </section>'''.format(img.get('src').strip('"'))
                    post_images.append(links)
            except Exception as _ex:
                post_images = _ex
            result_list.append(
                {
                    "item_header": item_header,
                    "item_time": item_time,
                    "item_img": header_img,
                    "item_content": section_of_post,
                    "itm_images": '\n'.join(post_images),
                    "istok_href": href,
                    "author": author
                }
            )


    async def gather_data(self):
        start_parm = {
            "handleSIGINT": False,
            "handleSIGTERM": False,
            "handleSIGHUP": False,
            "headless": False,
            "ignoreHTTPSErrors": False,
            "args": [

                '--ignore-certificate-errors',
                '--ignore-certificate-errors-spki-list',
            ]
        }
        browser = await launch(**start_parm)
        page = await browser.newPage()
        tasks = []

        try:
            connection = psycopg2.connect(
                host='localhost',
                user='admin',
                password='admin',
                database='odoo14_base1'
            )
            await page.goto('https://neurohive.io/ru/novosti/')
            while True:
                await page.evaluate("""{window.scrollBy('.post-1889', document.body.scrollHeight);}""")
                await asyncio.sleep(2)
                if await page.querySelector('.post-1889'):
                    page_text = await page.content()
                    soup = BeautifulSoup(page_text, "lxml")
                    articles = soup.find_all("article", class_="has-post-thumbnail")
                    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as s:
                        for article in articles:
                            item_header = article.find("h2", class_="entry-title").find("a").text.strip()
                            header = "'{}'".format(item_header)
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "select not exists(select from blog_post where name=" + header + ")")
                                adam = cursor.fetchone()
                                if adam[0] is True:
                                    href_url = article.find("h2", class_="entry-title").find("a").get("href")
                                    task = asyncio.create_task(self.get_data_urls(s, href_url))
                                    tasks.append(task)
                            connection.commit()
                        await asyncio.gather(*tasks)
                        break


        except Exception as _ex:
            return _ex
        finally:
            await browser.close()

    # class cron_parser(models.Model):
    #     _name = 'cron_parser.cron_parser'
    #     _description = 'cron_parser.cron_parser'

    #     name = fields.Char()
    #     value = fields.Integer()
    #     value2 = fields.Float(compute="_value_pc", store=True)
    #     description = fields.Text()
    #
    #     @api.depends('value')
    #     def _value_pc(self):
    #         for record in self:
    #             record.value2 = float(record.value) / 100
